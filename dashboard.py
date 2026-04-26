import streamlit as st
import plotly.express as px
import pandas as pd
import json
import glob
import os

st.set_page_config(
    page_title="LLM Quality Gate Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 LLM Quality Gate Dashboard")
st.caption("Production-grade LLM evaluation pipeline")

# Load all results files
results_files = glob.glob("results_*.json")

if not results_files:
    st.error("No results files found. Run evalrunner.py first.")
    st.stop()

# Load the most recent file
latest_file = max(results_files)
with open(latest_file) as f:
    output = json.load(f)

summary = output['summary']
results = output['results']

st.caption(f"Latest run: {latest_file}")

# Summary cards
st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tests", summary['total'])

with col2:
    st.metric("Passed", summary['passed'])

with col3:
    st.metric("Failed", summary['failed'])

with col4:
    st.metric(
        "Average Score",
        summary['average_score'],
        delta=None
    )

# Tier comparison chart
st.subheader("Score by Tier")

tier_data = pd.DataFrame({
    "Tier": ["Tier 1 (Simple)", "Tier 2 (Medium)", "Tier 3 (Complex)"],
    "Average Score": [
        summary['tier_averages'].get('1', 0),
        summary['tier_averages'].get('2', 0),
        summary['tier_averages'].get('3', 0)
    ]
})

fig = px.bar(
    tier_data,
    x="Tier",
    y="Average Score",
    color="Average Score",
    color_continuous_scale="RdYlGn",
    range_y=[0, 1],
    title="Average Score by Difficulty Tier"
)

st.plotly_chart(fig, use_container_width=True)

# Detailed results table
st.subheader("Detailed Results")

# Convert results to a dataframe
df = pd.DataFrame([{
    "ID": r['id'],
    "Tier": r['tier'],
    "Question": r['question'],
    "Keyword Score": r['keyword_score'],
    "Final Score": r['final_score'],
    "Status": "✅ Pass" if r['final_score'] >= 0.7 else "❌ Fail"
} for r in results])

# Color code by status
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Score distribution
st.subheader("Score Distribution")

fig2 = px.histogram(
    df,
    x="Final Score",
    nbins=10,
    color="Status",
    color_discrete_map={
        "✅ Pass": "green",
        "❌ Fail": "red"
    },
    title="Distribution of Final Scores"
)

st.plotly_chart(fig2, use_container_width=True)

# Run history
st.subheader("Run History")

all_runs = []
for file in sorted(results_files):
    with open(file) as f:
        data = json.load(f)
    if isinstance(data, dict) and 'summary' in data:
        all_runs.append({
            "Run": file.replace("results_", "").replace(".json", ""),
            "Average Score": data['summary']['average_score'],
            "Passed": data['summary']['passed'],
            "Failed": data['summary']['failed']
        })

if len(all_runs) > 1:
    runs_df = pd.DataFrame(all_runs)
    fig3 = px.line(
        runs_df,
        x="Run",
        y="Average Score",
        title="Average Score Over Time",
        markers=True
    )
    fig3.add_hline(
        y=0.7,
        line_dash="dash",
        line_color="red",
        annotation_text="Threshold"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Run evalrunner.py a few more times to see score trends here.")
