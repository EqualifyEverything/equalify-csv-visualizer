import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Equalify CSV Dashboard", layout="wide")


# Title
st.title("Equalify Scan Dashboard")

# Subtitle
st.markdown("## Source: https://ahs.uic.edu/")

# Load CSV
df = pd.read_csv("input.csv")

# Summary metrics
total_violations = len(df[df["Messages"].str.lower().str.startswith("violation:")])
total_warnings = len(df[df["Messages"].str.lower().str.startswith("warning:")])
total_webpages = df[df["Type"].str.lower() == "web page"]["URL"].nunique()
total_pdfs = df[df["Type"].str.lower() == "pdf"]["URL"].nunique()

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Violations", total_violations)
col2.metric("Total Warnings", total_warnings)
col3.metric("Scanned Webpages", total_webpages)
col4.metric("Scanned PDFs", total_pdfs)


# Group by URL and count unique Node IDs
url_summary = df.groupby("URL")["Node ID"].nunique().reset_index()
url_summary.columns = ["URL", "Number of Problems"]
url_summary = url_summary.sort_values(by="Number of Problems", ascending=False)

# Group by Messages and count unique Node IDs
summary = df.groupby("Messages")["Node ID"].nunique().reset_index()
summary.columns = ["Message", "Number of Unique Nodes"]
summary = summary.sort_values(by="Number of Unique Nodes", ascending=False)

# Display URL summary table
st.subheader("Problem URLs")
st.dataframe(url_summary)

# Separate messages into violations and warnings
violations = summary[summary["Message"].str.lower().str.startswith("violation:")]
warnings = summary[summary["Message"].str.lower().str.startswith("warning:")]

# Display summary tables
st.subheader("Violations")
st.dataframe(violations)

st.subheader("Warnings")
st.dataframe(warnings)