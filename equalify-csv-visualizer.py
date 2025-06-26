import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Equalify CSV Dashboard", layout="wide")

# Title
st.title("Equalify CSV Dashboard")

# Load CSV
df = pd.read_csv("input.csv")

# Group by URL and count unique Node IDs
url_summary = df.groupby("URL")["Node ID"].nunique().reset_index()
url_summary.columns = ["URL", "Number of Unique Nodes"]
url_summary = url_summary.sort_values(by="Number of Unique Nodes", ascending=False)

# Group by Messages and count unique Node IDs
summary = df.groupby("Messages")["Node ID"].nunique().reset_index()
summary.columns = ["Message", "Number of Unique Nodes"]
summary = summary.sort_values(by="Number of Unique Nodes", ascending=False)

# Display URL summary table
st.subheader("Node Counts by URL")
st.dataframe(url_summary)

# Select a URL to view node details
st.subheader("View Node Details by URL")
selected_url = st.selectbox("Select a URL", url_summary["URL"].tolist())

if selected_url:
    filtered_nodes = df[df["URL"] == selected_url][["Node ID", "Messages", "HTML", "Targets"]]
    st.write(f"Nodes for URL: {selected_url}")
    st.dataframe(filtered_nodes)

# Separate messages into violations and warnings
violations = summary[summary["Message"].str.lower().str.startswith("violation:")]
warnings = summary[summary["Message"].str.lower().str.startswith("warning:")]

# Display summary tables
st.subheader("Violations")
st.dataframe(violations)

st.subheader("Warnings")
st.dataframe(warnings)