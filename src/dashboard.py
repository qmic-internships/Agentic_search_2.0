import streamlit as st
import json
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(page_title="Multi-Evaluation Dashboard", layout="wide", page_icon="📊")

# Custom CSS for better styling
st.markdown("""
<style>
    .evaluation-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .comparison-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Data loading functions
def load_jsonl_data(file_path):
    """Load data from JSONL file"""
    if not Path(file_path).exists():
        return []
    
    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return []
    
    return data

def load_json_data(file_path):
    """Load data from JSON file"""
    if not Path(file_path).exists():
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return []

# Load all evaluation data
@st.cache_data
def load_all_evaluation_data():
    """Load data from all three evaluation types"""
    
    # Evaluation.py results (advanced_evaluation_report.jsonl)
    evaluation_py_data = load_jsonl_data("data/results/advanced_evaluation_report.jsonl")
    
    # Evaluation_5.py results (evaluation_report_5.jsonl)
    evaluation_5_data = load_jsonl_data("evaluation_report_5.jsonl")
    
    # New_evaluation.py results (poi_evaluated.jsonl)
    new_evaluation_data = load_jsonl_data("data/processed/poi_evaluated.jsonl")
    
    return evaluation_py_data, evaluation_5_data, new_evaluation_data

# Title and overview
st.title("🔍 Multi-Evaluation Dashboard")
st.markdown("Compare results from all three evaluation approaches")

# Load data
evaluation_py_data, evaluation_5_data, new_evaluation_data = load_all_evaluation_data()

# Sidebar for global filters
st.sidebar.header("🔧 Global Filters")
common_queries = set()

# Get common queries across all evaluations
if evaluation_py_data:
    common_queries.update([item.get("query", "") for item in evaluation_py_data])
if evaluation_5_data:
    common_queries.update([item.get("query", "") for item in evaluation_5_data])
if new_evaluation_data:
    common_queries.update([item.get("query", "") for item in new_evaluation_data])

common_queries = sorted([q for q in common_queries if q])

if common_queries:
    selected_query = st.sidebar.selectbox("Select Query to Compare", [""] + common_queries)
else:
    selected_query = ""
    st.sidebar.warning("No evaluation data found")

# Overview metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Evaluation.py Results", len(evaluation_py_data))
with col2:
    st.metric("Evaluation_5.py Results", len(evaluation_5_data))
with col3:
    st.metric("New_evaluation.py Results", len(new_evaluation_data))
with col4:
    total_unique_queries = len(common_queries)
    st.metric("Total Unique Queries", total_unique_queries)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview Comparison", "🔍 Evaluation.py", "⭐ Evaluation_5.py", "🇶🇦 New_evaluation.py"])

with tab1:
    st.header("📊 Cross-Evaluation Comparison")
    
    if not any([evaluation_py_data, evaluation_5_data, new_evaluation_data]):
        st.warning("No evaluation data available for comparison")
    else:
        # Score distribution comparison
        st.subheader("Score Distribution Comparison")
        
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=["Evaluation.py", "Evaluation_5.py", "New_evaluation.py"],
            specs=[[{"type": "histogram"}, {"type": "histogram"}, {"type": "histogram"}]]
        )
        
        if evaluation_py_data:
            scores_py = [item.get("holistic_ai_score", 0) for item in evaluation_py_data if item.get("holistic_ai_score") is not None]
            fig.add_trace(go.Histogram(x=scores_py, name="Eval.py", nbinsx=20), row=1, col=1)
        
        if evaluation_5_data:
            scores_5 = [item.get("holistic_ai_score", 0) for item in evaluation_5_data if item.get("holistic_ai_score") is not None]
            fig.add_trace(go.Histogram(x=scores_5, name="Eval_5.py", nbinsx=20), row=1, col=2)
        
        if new_evaluation_data:
            scores_new = [item.get("score", 0) for item in new_evaluation_data if item.get("score") is not None]
            fig.add_trace(go.Histogram(x=scores_new, name="New_eval.py", nbinsx=20), row=1, col=3)
        
        fig.update_layout(height=400, showlegend=False, title_text="Score Distribution Across All Evaluations")
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        summary_data = []
        
        if evaluation_py_data:
            scores_py = [item.get("holistic_ai_score", 0) for item in evaluation_py_data if item.get("holistic_ai_score") is not None]
            if scores_py:
                summary_data.append({
                    "Evaluation": "Evaluation.py",
                    "Count": len(scores_py),
                    "Mean Score": round(sum(scores_py) / len(scores_py), 2),
                    "Min Score": min(scores_py),
                    "Max Score": max(scores_py)
                })
        
        if evaluation_5_data:
            scores_5 = [item.get("holistic_ai_score", 0) for item in evaluation_5_data if item.get("holistic_ai_score") is not None]
            if scores_5:
                summary_data.append({
                    "Evaluation": "Evaluation_5.py",
                    "Count": len(scores_5),
                    "Mean Score": round(sum(scores_5) / len(scores_5), 2),
                    "Min Score": min(scores_5),
                    "Max Score": max(scores_5)
                })
        
        if new_evaluation_data:
            scores_new = [item.get("score", 0) for item in new_evaluation_data if item.get("score") is not None]
            if scores_new:
                summary_data.append({
                    "Evaluation": "New_evaluation.py",
                    "Count": len(scores_new),
                    "Mean Score": round(sum(scores_new) / len(scores_new), 2),
                    "Min Score": min(scores_new),
                    "Max Score": max(scores_new)
                })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
        
        # Query-specific comparison
        if selected_query:
            st.subheader(f"Query-Specific Comparison: '{selected_query}'")
            
            comparison_data = []
            
            # Find matching results for the selected query
            for eval_data, eval_name in [(evaluation_py_data, "Evaluation.py"), 
                                       (evaluation_5_data, "Evaluation_5.py"), 
                                       (new_evaluation_data, "New_evaluation.py")]:
                for item in eval_data:
                    if item.get("query") == selected_query:
                        if eval_name == "New_evaluation.py":
                            comparison_data.append({
                                "Evaluation": eval_name,
                                "Score": item.get("score", "N/A"),
                                "Judgment/Reasoning": item.get("reason", "N/A")[:100] + "...",
                                "Raw Data": str(item)[:200] + "..."
                            })
                        else:
                            comparison_data.append({
                                "Evaluation": eval_name,
                                "Score": item.get("holistic_ai_score", "N/A"),
                                "Judgment/Reasoning": item.get("holistic_ai_reasoning", "N/A")[:100] + "...",
                                "Raw Data": str(item)[:200] + "..."
                            })
                        break
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
            else:
                st.info(f"No results found for query: '{selected_query}'")

with tab2:
    st.header("🔍 Evaluation.py Results")
    
    if not evaluation_py_data:
        st.warning("No Evaluation.py data available")
    else:
        # Summary statistics
        scores_py = [item.get("holistic_ai_score", 0) for item in evaluation_py_data if item.get("holistic_ai_score") is not None]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Evaluations", len(evaluation_py_data))
        with col2:
            if scores_py:
                st.metric("Average Score", round(sum(scores_py) / len(scores_py), 2))
        with col3:
            if scores_py:
                st.metric("Score Range", f"{min(scores_py)} - {max(scores_py)}")
        
        # Score distribution
        if scores_py:
            fig = px.histogram(x=scores_py, nbins=20, title="Score Distribution - Evaluation.py")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results
        st.subheader("Detailed Results")
        
        # Filter by score range
        if scores_py:
            min_score, max_score = st.slider("Score Range", 0.0, 10.0, (min(scores_py), max(scores_py)))
            filtered_data = [item for item in evaluation_py_data 
                           if item.get("holistic_ai_score", 0) >= min_score 
                           and item.get("holistic_ai_score", 0) <= max_score]
        else:
            filtered_data = evaluation_py_data
        
        for item in filtered_data:
            with st.expander(f"Query: {item.get('query', 'N/A')} | Score: {item.get('holistic_ai_score', 'N/A')}"):
                st.write("**Query:**", item.get('query', 'N/A'))
                st.write("**Score:**", item.get('holistic_ai_score', 'N/A'))
                st.write("**Reasoning:**", item.get('holistic_ai_reasoning', 'N/A'))
                if 'quantitative_metrics' in item:
                    st.write("**Quantitative Metrics:**", item['quantitative_metrics'])

with tab3:
    st.header("⭐ Evaluation_5.py Results")
    
    if not evaluation_5_data:
        st.warning("No Evaluation_5.py data available")
    else:
        # Summary statistics
        scores_5 = [item.get("holistic_ai_score", 0) for item in evaluation_5_data if item.get("holistic_ai_score") is not None]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Evaluations", len(evaluation_5_data))
        with col2:
            if scores_5:
                st.metric("Average Score", round(sum(scores_5) / len(scores_5), 2))
        with col3:
            if scores_5:
                st.metric("Score Range", f"{min(scores_5)} - {max(scores_5)}")
        
        # Score distribution
        if scores_5:
            fig = px.histogram(x=scores_5, nbins=20, title="Score Distribution - Evaluation_5.py")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results
        st.subheader("Detailed Results")
        
        # Filter by score range
        if scores_5:
            min_score, max_score = st.slider("Score Range", 0.0, 10.0, (min(scores_5), max(scores_5)), key="eval5_slider")
            filtered_data = [item for item in evaluation_5_data 
                           if item.get("holistic_ai_score", 0) >= min_score 
                           and item.get("holistic_ai_score", 0) <= max_score]
        else:
            filtered_data = evaluation_5_data
        
        for item in filtered_data:
            with st.expander(f"Query: {item.get('query', 'N/A')} | Score: {item.get('holistic_ai_score', 'N/A')}"):
                st.write("**Query:**", item.get('query', 'N/A'))
                st.write("**Score:**", item.get('holistic_ai_score', 'N/A'))
                st.write("**Reasoning:**", item.get('holistic_ai_reasoning', 'N/A'))
                if 'quantitative_metrics' in item:
                    st.write("**Quantitative Metrics:**", item['quantitative_metrics'])

with tab4:
    st.header("🇶🇦 New_evaluation.py Results")
    
    if not new_evaluation_data:
        st.warning("No New_evaluation.py data available")
    else:
        # Summary statistics
        scores_new = [item.get("score", 0) for item in new_evaluation_data if item.get("score") is not None]
        judgments = [item.get("judgment", "") for item in new_evaluation_data if item.get("judgment")]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Evaluations", len(new_evaluation_data))
        with col2:
            if scores_new:
                st.metric("Average Score", round(sum(scores_new) / len(scores_new), 2))
        with col3:
            if scores_new:
                st.metric("Score Range", f"{min(scores_new)} - {max(scores_new)}")
        
        # Judgment distribution
        if judgments:
            judgment_counts = pd.Series(judgments).value_counts()
            fig = px.pie(values=judgment_counts.values, names=judgment_counts.index, title="Judgment Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Score distribution
        if scores_new:
            fig = px.histogram(x=scores_new, nbins=20, title="Score Distribution - New_evaluation.py")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results
        st.subheader("Detailed Results")
        
        # Filter by judgment
        if judgments:
            judgment_filter = st.multiselect("Filter by Judgment", options=sorted(set(judgments)), default=sorted(set(judgments)))
            filtered_data = [item for item in new_evaluation_data 
                           if item.get("judgment") in judgment_filter]
        else:
            filtered_data = new_evaluation_data
        
        for item in filtered_data:
            with st.expander(f"Query: {item.get('query', 'N/A')} | Judgment: {item.get('judgment', 'N/A')} | Score: {item.get('score', 'N/A')}"):
                st.write("**Query:**", item.get('query', 'N/A'))
                st.write("**Judgment:**", item.get('judgment', 'N/A'))
                st.write("**Score:**", item.get('score', 'N/A'))
                st.write("**Reason:**", item.get('reason', 'N/A'))
                
                # Show Solr and Google results
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Solr Results:**")
                    solr_results = item.get('solr_results', [])
                    for i, result in enumerate(solr_results[:5]):  # Show top 5
                        st.write(f"{i+1}. {result.get('solr_name', 'N/A')}")
                
                with col2:
                    st.write("**Google Results:**")
                    google_results = item.get('google_autocomplete_results', [])
                    for i, result in enumerate(google_results[:5]):  # Show top 5
                        st.write(f"{i+1}. {result.get('google_place_prediction_text', 'N/A')}")

# Footer
st.markdown("---")
st.markdown("**Multi-Evaluation Dashboard** - Compare results from all three evaluation approaches")