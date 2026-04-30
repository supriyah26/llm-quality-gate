import json
import sys
import glob

# Find the most recent results file
results_files = glob.glob("results_*.json")

if not results_files:
    print("❌ No results file found")
    sys.exit(1)

latest_file = max(results_files)
print(f"Reading results from: {latest_file}")

with open(latest_file) as f:
    output = json.load(f)

# Quality gate threshold
THRESHOLD = 0.7

print("\n" + "="*40)
print("QUALITY GATE CHECK")
print("="*40)

all_passed = True

for model_name, model_data in output.items():
    summary = model_data['summary']
    avg_score = summary['average_score']
    passed = summary['passed']
    total = summary['total']

    print(f"\nModel: {model_name.upper()}")
    print(f"Average Score: {avg_score}")
    print(f"Passed: {passed}/{total}")

    if avg_score < THRESHOLD:
        print(f"❌ FAILED — score {avg_score} below threshold {THRESHOLD}")
        all_passed = False
    else:
        print(f"✅ PASSED — score {avg_score} above threshold {THRESHOLD}")

print("\n" + "="*40)

if not all_passed:
    print("❌ Quality gate FAILED — one or more models below threshold")
    print("Deployment blocked.")
    sys.exit(1)
else:
    print("✅ All models passed quality gate")
    print("Deployment approved.")
    sys.exit(0)