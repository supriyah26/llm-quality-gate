import anthropic
from dotenv import load_dotenv

# This reads your API key from the .env file
load_dotenv()

# This creates a connection to Claude
client = anthropic.Anthropic()

# This sends a message to Claude and gets a response
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of France? Answer in one sentence."}
    ]
)

# This prints Claude's response
print("Claude says:", message.content[0].text)