import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Page config
st.set_page_config(page_title="Equalify CSV Dashboard", layout="wide")


st.title("Equalify Scan Dashboard")

# Load CSV
df = pd.read_csv("input.csv")

# Summary metrics
total_violations = len(df[df["Messages"].str.lower().str.startswith("violation:")])
total_warnings = len(df[df["Messages"].str.lower().str.startswith("warning:")])
total_webpages = df[df["Type"].str.lower() == "web page"]["URL"].nunique()
total_pdfs = df[df["Type"].str.lower() == "pdf"]["URL"].nunique()

# Group by URL and count unique Node IDs
url_summary = df.groupby("URL")["Node ID"].nunique().reset_index()
url_summary.columns = ["URL", "Number of Problems"]
url_summary = url_summary.sort_values(by="Number of Problems", ascending=False)

# Group by Messages and count unique Node IDs
summary = df.groupby("Messages")["Node ID"].nunique().reset_index()
summary.columns = ["Message", "Number of Unique Nodes"]
summary = summary.sort_values(by="Number of Unique Nodes", ascending=False)

# Separate messages into violations and warnings
violations = summary[summary["Message"].str.lower().str.startswith("violation:")]
warnings = summary[summary["Message"].str.lower().str.startswith("warning:")]

# PDF download button
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Equalify Scan Dashboard", styles['Title']))
    elements.append(Paragraph("Source: https://ahs.uic.edu/", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Metrics
    metrics_data = [
        ["Total Violations", str(total_violations)],
        ["Total Warnings", str(total_warnings)],
        ["Scanned Webpages", str(total_webpages)],
        ["Scanned PDFs", str(total_pdfs)]
    ]
    t = Table(metrics_data, colWidths=[doc.width/2]*2)
    t.setStyle(TableStyle([
        # No header row styling for metrics table
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph("Summary Metrics", styles['Heading2']))
    elements.append(t)
    elements.append(Spacer(1, 18))

    # Problem URLs Table
    elements.append(Paragraph("Problem URLs", styles['Heading2']))
    url_summary_data = [url_summary.columns.tolist()] + [
        [Paragraph(str(cell), styles["Normal"]) for cell in row]
        for row in url_summary.values.tolist()
    ]
    t_urls = Table(
        url_summary_data,
        repeatRows=1,
        colWidths=[doc.width/len(url_summary_data[0])]*len(url_summary_data[0])
    )
    t_urls.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t_urls)
    elements.append(Spacer(1, 18))

    # Violations Table
    elements.append(Paragraph("Violations", styles['Heading2']))
    violations_data = [violations.columns.tolist()] + [
        [Paragraph(str(cell), styles["Normal"]) for cell in row]
        for row in violations.values.tolist()
    ]
    t_viol = Table(
        violations_data,
        repeatRows=1,
        colWidths=[doc.width/len(violations_data[0])]*len(violations_data[0])
    )
    t_viol.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t_viol)
    elements.append(Spacer(1, 18))

    # Warnings Table
    elements.append(Paragraph("Warnings", styles['Heading2']))
    warnings_data = [warnings.columns.tolist()] + [
        [Paragraph(str(cell), styles["Normal"]) for cell in row]
        for row in warnings.values.tolist()
    ]
    t_warn = Table(
        warnings_data,
        repeatRows=1,
        colWidths=[doc.width/len(warnings_data[0])]*len(warnings_data[0])
    )
    t_warn.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t_warn)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# PDF download button
st.download_button(
    label="Download Report as PDF",
    data=generate_pdf(),
    file_name="equalify_report.pdf",
    mime="application/pdf"
)

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Violations", total_violations)
col2.metric("Total Warnings", total_warnings)
col3.metric("Scanned Webpages", total_webpages)
col4.metric("Scanned PDFs", total_pdfs)

# Display URL summary table
st.subheader("Problem URLs")
st.dataframe(url_summary)

# Display summary tables
st.subheader("Violations")
st.dataframe(violations)

st.subheader("Warnings")
st.dataframe(warnings)