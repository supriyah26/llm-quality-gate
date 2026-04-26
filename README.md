# LLM Quality Gate System

> The reliability infrastructure that makes AI systems 
> trustworthy in production — not just in demos.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-orange)
![MLflow](https://img.shields.io/badge/MLflow-3.11-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red)

## The Problem

Most companies deploying LLMs have no reliable way 
to know when their model starts failing.

- No automated testing
- No regression detection  
- No audit trail of model changes
- Failures discovered by users, not engineers

Research shows **40% of LLM outputs fail** when they 
hit production reality. Even Andrej Karpathy calls it 
an *"evaluation crisis."*

## The Solution

An automated quality gate system that sits between 
your model and your users — catching failures before 
they cause damage.

Every code change triggers an automatic eval pipeline.
If quality drops below threshold — the deployment 
is blocked automatically.

No manual testing. No gut feelings. 
Just data-backed deployment decisions.

## Architecture
┌─────────────────────────────────────────────────┐
│                  LLM Quality Gate                │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Golden  │    │   Eval   │    │  Scoring │  │
│  │ Dataset  │───▶│  Runner  │───▶│  Engine  │  │
│  │ 3 Tiers  │    │          │    │ 2 Layers │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│                        │                │        │
│                        ▼                ▼        │
│                  ┌──────────┐    ┌──────────┐  │
│                  │  MLflow  │    │ Quality  │  │
│                  │ Tracking │    │   Gate   │  │
│                  └──────────┘    └──────────┘  │
│                        │                │        │
│                        ▼                ▼        │
│                  ┌──────────┐    ┌──────────┐  │
│                  │Streamlit │    │  GitHub  │  │
│                  │Dashboard │    │ Actions  │  │
│                  └──────────┘    └──────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘

## Scoring Engine — Two Layers

| Layer | Method | Weight | Strength |
|---|---|---|---|
| Layer 1 | Keyword Heuristics | 40% | Fast, catches obvious failures |
| Layer 2 | LLM as a Judge | 60% | Semantic understanding |

**Final Score = (Keyword Score × 40%) + (LLM Score × 60%)**

## Key Findings

### Finding 1 — Single Layer Scoring Is Dangerous
Keyword scoring flagged correct answers as 67% accurate.
LLM judge scored the same answers 4/5 and 5/5.

A system that only uses keyword matching would have 
triggered false alarms and sent engineers chasing 
problems that didn't exist.

### Finding 2 — Non-Determinism Is Real
Running the same eval twice with zero code changes 
produced a 13 point swing in Tier 2 scores:

This proves you cannot trust a single eval run 
to measure model performance. Statistical analysis 
across multiple runs is essential.

### Finding 3 — Medium Questions Are Most Unstable
Simple and complex questions produced consistent 
scores across runs. Medium difficulty questions 
showed the highest variance — they sit in a zone 
where the model is neither confident nor lost.

## How To Run It

### Prerequisites
- Python 3.11
- Anthropic API key

### Installation

```bash
# Clone the repository
git clone https://github.com/YOURUSERNAME/llm-quality-gate.git
cd llm-quality-gate

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install anthropic python-dotenv mlflow streamlit plotly pandas
```

### Setup

Create a `.env` file in the root folder:

### Run The Eval Pipeline

```bash
python3 evalrunner.py
```

### View The Dashboard

```bash
streamlit run dashboard.py
```

### Run The Quality Gate Check

```bash
python3 gate_check.py
```

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Anthropic Claude API | LLM evaluation |
| MLflow | Experiment tracking |
| Streamlit | Dashboard |
| Plotly | Charts |
| GitHub Actions | CI/CD quality gate |

## Project Structure

llm-quality-gate/
├── evalrunner.py      # Main eval pipeline
├── dataset.py         # Golden dataset — 7 test cases
├── dashboard.py       # Streamlit dashboard
├── gate_check.py      # Quality gate threshold checker
├── .github/
│   └── workflows/
│       └── eval.yml   # GitHub Actions workflow
├── .env               # API keys (not committed)
└── .gitignore

## Author

**Supriya Hinge**
AI Engineer | 7+ years building production ML systems

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/https://www.linkedin.com/in/supriya-hinge-82335311b/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/supriyah26)