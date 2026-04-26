import anthropic
import json
import mlflow
from datetime import datetime
from dotenv import load_dotenv
from dataset import dataset

# Load API key from .env file
load_dotenv()
mlflow.set_experiment("Customer Support Eval")
print("Script is running...v2")

# Create connection to Claude
client = anthropic.Anthropic()

# This is the system prompt — it tells Claude who it is
# and how it should behave for every question
SYSTEM_PROMPT = """You are a helpful customer support assistant 
for an e-commerce store. Answer questions clearly and concisely.
Use these facts:
- Return policy: 30 days from purchase
- Shipping: 5-7 business days
- Payment: credit cards, debit cards, PayPal
- For damaged or missing items: contact support with photos"""

def ask_claude(question):
    """
    Send one question to Claude and returns its answer. 
    """
    message = client.messages.create(
        model = "claude-sonnet-4-5",
        max_tokens=500,
        system=SYSTEM_PROMPT, 
        messages=[
            {"role":"user", "content": question}
        ]
    )
    return message.content[0].text



def keyword_score(response, expected):
    """
    Layer 1 — Checks if key words from the 
    expected answer appear in Claude's response.
    Returns a score between 0 and 1.
    """
    # Convert both to lowercase so 
    # "Return" and "return" count as the same word
    response_lower = response.lower()
    expected_lower = expected.lower()

    # Split expected answer into individual words
    expected_words = expected_lower.split()

    # Filter out short common words like 
    # "the", "a", "is", "in" — they don't add meaning
    keywords = [
        word for word in expected_words
        if len(word) > 3 or word.isdigit()
    ]

    # Count how many keywords appear in the response
    matches = sum(
        1 for keyword in keywords 
        if keyword in response_lower
    )

    # Calculate score — what percentage of 
    # keywords were found?
    if len(keywords) == 0:
        return 0.0

    score = matches / len(keywords)
    return round(score, 2)



def llm_judge(question, response, expected):
    judge_prompt = f"""You are an expert evaluator.
Your job is to judge whether a response correctly answers a question.

Question: {question}
Expected Answer: {expected}
Actual Response: {response}

Score the response from 0 to 5 where:
0 = Completely wrong
1 = Mostly wrong
2 = Partially correct
3 = Mostly correct
4 = Correct with minor differences
5 = Perfect

Respond in this exact format:
SCORE: [number]
REASON: [one sentence]"""

    judgment = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=150,
        messages=[
            {"role": "user", "content": judge_prompt}
        ]
    )
    judgment_text = judgment.content[0].text.strip()
    #print("Raw judgment:", judgment_text)
    return judgment_text

def parse_llm_score(judgment_text):
    """
    Extracts the number from the LLM judgment string
    and converts it to a 0-1 scale.
    """
    try:
        lines = judgment_text.split("\n")
        score_line = [
            line for line in lines 
            if line.startswith("SCORE:")
        ][0]
        raw_score = int(score_line.replace("SCORE:", "").strip())
        return round(raw_score / 5, 2)
    except:
        return 0.0

def final_score(keyword_score, judgment_text):
    """
    Combines Layer 1 and Layer 2 into one final score.
    Keyword score weighted 40%, LLM judge weighted 60%.
    """
    llm_score = parse_llm_score(judgment_text)
    combined = (keyword_score * 0.4) + (llm_score * 0.6)
    return round(combined, 2)

def run_summary(results):
    """
    Summarizes the entire eval run in one clean block.
    """
    total = len(results)
    passed = sum(1 for r in results if r['final_score'] >= 0.7)
    failed = total - passed
    avg_score = round(
        sum(r['final_score'] for r in results) / total, 2
    )

    # Calculate average score by tier
    tiers = {1: [], 2: [], 3: []}
    for r in results:
        tiers[r['tier']].append(r['final_score'])

    tier_averages = {
        tier: round(sum(scores) / len(scores), 2)
        for tier, scores in tiers.items()
        if len(scores) > 0
    }

    print("\n" + "="*40)
    print("EVAL RUN SUMMARY")
    print("="*40)
    print(f"Total tests:     {total}")
    print(f"Passed (≥0.7):   {passed}")
    print(f"Failed (<0.7):   {failed}")
    print(f"Average score:   {avg_score}")
    print("\nBy tier:")
    for tier, avg in tier_averages.items():
        print(f"  Tier {tier} avg:   {avg}")
    print("="*40)

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "average_score": avg_score,
        "tier_averages": tier_averages
    }



results = []
with mlflow.start_run():
    for test_case in dataset:
        print(f"\nTesting: {test_case['question']}")

        response = ask_claude(test_case['question'])
        print(f"Claude's answer: {response}")

    #Step 2 - Keywors match score with Layer 1

        kw_score = keyword_score(response, test_case['expected'])
        print(f"Keyword Score: {kw_score}")

        judgment = llm_judge(
            test_case['question'], 
            response, 
            test_case['expected']
    )

        print(f"LLM Judgment: {judgment}") 
        score = final_score(kw_score, judgment)
        print(f"Final Score: {score}")

    #Step 4 - Collect results 
        results.append({
            "id": test_case['id'],
            "tier": test_case['tier'],
            "question": test_case['question'],
            "expected": test_case['expected'],
            "response": response,
            "keyword_score": kw_score,
            "llm_judgment": judgment,
            "final_score": final_score(kw_score, judgment),
            "timestamp": datetime.now().isoformat()
        })

    summary = run_summary(results)
    mlflow.log_metric("average_score", summary['average_score'])
    mlflow.log_metric("total_passed", summary['passed'])
    mlflow.log_metric("total_failed", summary['failed'])
    mlflow.log_metric("tier1_avg", summary['tier_averages'][1])
    mlflow.log_metric("tier2_avg", summary['tier_averages'][2])
    mlflow.log_metric("tier3_avg", summary['tier_averages'][3])
    mlflow.log_param("model", "claude-sonnet-4-5")
    mlflow.log_param("total_test_cases", len(dataset))

    filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output = {
    "summary": summary, 
    "results": results
    }


    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n Results saved to {filename}")
    print(f"Total test cases: {len(results)}")



