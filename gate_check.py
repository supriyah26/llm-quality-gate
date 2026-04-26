import json
import sys
import os
import glob

# Find the most recent results file
results_files = glob.glob("results_*.json")

if not results_files:
    print("❌ No results file found")
    sys.exit(1)

latest_file = max(results_files)

with open(latest_file) as f:
    output = json.load(f)

# Handle both old format (list) and new format (dict with summary)
if isinstance(output, list):
    print("❌ Old results format detected - run evalrunner.py first")
    sys.exit(1)

summary = output['summary']
avg_score = summary['average_score']
passed = summary['passed']
total = summary['total']

print(f"Average Score: {avg_score}")
print(f"Passed: {passed}/{total}")

# Quality gate threshold
THRESHOLD = 0.7

if avg_score < THRESHOLD:
    print(f"❌ Quality gate FAILED — score {avg_score} below threshold {THRESHOLD}")
    sys.exit(1)
else:
    print(f"✅ Quality gate PASSED — score {avg_score} above threshold {THRESHOLD}")
    sys.exit(0)