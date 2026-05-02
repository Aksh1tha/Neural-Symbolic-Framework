# app.py
# FreeMind AI - Full Working Version + Better Mind Map

import streamlit as st
import requests
import PyPDF2
import math
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="FreeMind AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------
# UI STYLE
# ---------------------------------------------------
st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
section[data-testid="stSidebar"]{
    background:#111827;
    width:320px !important;
}
section[data-testid="stSidebar"] *{
    color:white !important;
}
.title{
    font-size:42px;
    font-weight:800;
    text-align:center;
}
.sub{
    text-align:center;
    color:#9CA3AF;
    margin-bottom:25px;
}
.stButton>button{
    width:100%;
    height:46px;
    border-radius:12px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧠 FreeMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">AI Workspace • Better UI • Better Mind Map</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def summarize_text(text):
    words = text.split()
    return " ".join(words[:120])

def extract_url(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.text if soup.title else "Web Article"
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        return text, title
    except:
        return "", "Invalid URL"

def extract_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for p in reader.pages:
            t = p.extract_text()
            if t:
                text += t + " "
        return text, file.name
    except:
        return "", "PDF"

def get_input():
    source = st.selectbox("Choose Input", ["Text", "URL", "PDF"])
    value = None

    if source == "Text":
        value = st.text_area("Paste Text", height=250)

    elif source == "URL":
        value = st.text_input("Enter URL")

    elif source == "PDF":
        value = st.file_uploader("Upload PDF", type=["pdf"])

    return source, value

def get_text(source, value):
    if source == "Text":
        return value, "Text Document"
    elif source == "URL":
        return extract_url(value)
    elif source == "PDF":
        return extract_pdf(value)
    return "", ""

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    page = st.radio(
        "Select Tool",
        [
            "Summarization",
            "Report Generator",
            "Mind Map",
            "Document Analysis",
            "Mathematical Solver"
        ]
    )

# ===================================================
# SUMMARIZATION
# ===================================================
if page == "Summarization":

    st.subheader("Summarization")

    source, value = get_input()

    if st.button("Generate Summary"):

        text, title = get_text(source, value)

        if text:
            summary = summarize_text(text)
            st.success("Summary Generated")
            st.write(summary)
        else:
            st.error("No text found")

# ===================================================
# REPORT GENERATOR
# ===================================================
elif page == "Report Generator":

    st.subheader("Report Generator")

    source, value = get_input()

    if st.button("Generate Report"):

        text, title = get_text(source, value)

        if text:
            summary = summarize_text(text)

            st.markdown(f"# {title}")
            st.markdown("## Introduction")
            st.write("This document was analyzed using FreeMind AI.")

            st.markdown("## Summary")
            st.write(summary)

            st.markdown("## Conclusion")
            st.write("This concludes the generated report.")
        else:
            st.error("No text found")

# ===================================================
# BETTER MIND MAP
# ===================================================
elif page == "Mind Map":

    st.subheader("Mind Map")

    source, value = get_input()

    if st.button("Generate Mind Map"):

        text, title = get_text(source, value)

        if text:
            summary = summarize_text(text)
            words = summary.split()[:8]

            fig, ax = plt.subplots(figsize=(9,9))
            ax.set_xlim(-10,10)
            ax.set_ylim(-10,10)
            ax.axis("off")

            center = plt.Circle((0,0), 1.8, fill=False, linewidth=2)
            ax.add_patch(center)

            ax.text(
                0,0,title[:18],
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold"
            )

            angles = np.linspace(0, 2*np.pi, len(words), endpoint=False)

            for i, word in enumerate(words):

                x = 6*np.cos(angles[i])
                y = 6*np.sin(angles[i])

                ax.plot([0,x],[0,y], linewidth=1.5)

                node = plt.Circle((x,y), 1.2, fill=False)
                ax.add_patch(node)

                ax.text(
                    x,y,
                    word[:12],
                    ha="center",
                    va="center",
                    fontsize=10
                )

            st.pyplot(fig)

        else:
            st.error("No text found")

# ===================================================
# DOCUMENT ANALYSIS
# ===================================================
elif page == "Document Analysis":

    st.subheader("Document Analysis")

    source, value = get_input()

    if st.button("Analyze Document"):

        text, title = get_text(source, value)

        if text:
            summary = summarize_text(text)

            tab1, tab2, tab3 = st.tabs(
                ["Summary", "Report", "Mind Map"]
            )

            with tab1:
                st.write(summary)

            with tab2:
                st.markdown(f"# {title}")
                st.write(summary)

            with tab3:
                words = summary.split()[:8]

                fig, ax = plt.subplots(figsize=(9,9))
                ax.set_xlim(-10,10)
                ax.set_ylim(-10,10)
                ax.axis("off")

                center = plt.Circle((0,0), 1.8, fill=False)
                ax.add_patch(center)
                ax.text(0,0,title[:18],ha="center",va="center")

                angles = np.linspace(0,2*np.pi,len(words),endpoint=False)

                for i,w in enumerate(words):
                    x = 6*np.cos(angles[i])
                    y = 6*np.sin(angles[i])

                    ax.plot([0,x],[0,y])

                    node = plt.Circle((x,y),1.1,fill=False)
                    ax.add_patch(node)

                    ax.text(x,y,w[:10],ha="center",va="center")

                st.pyplot(fig)

        else:
            st.error("No text found")

# ===================================================
# MATH SOLVER
# ===================================================
elif page == "Mathematical Solver":

    st.subheader("Mathematical Solver")

    mode = st.radio(
        "Choose Mode",
        ["Calculator", "Quadratic", "Graph"]
    )

    if mode == "Calculator":

        expr = st.text_input("Expression")

        if st.button("Solve"):
            try:
                ans = eval(expr)
                st.success(ans)
            except:
                st.error("Invalid Expression")

    elif mode == "Quadratic":

        a = st.number_input("a", value=1.0)
        b = st.number_input("b", value=0.0)
        c = st.number_input("c", value=0.0)

        if st.button("Find Roots"):

            d = b*b - 4*a*c

            if d >= 0:
                r1 = (-b + math.sqrt(d))/(2*a)
                r2 = (-b - math.sqrt(d))/(2*a)

                st.success(f"Root 1 = {r1}")
                st.success(f"Root 2 = {r2}")
            else:
                st.error("Complex roots")

    elif mode == "Graph":

        expr = st.text_input("Use x variable", "x**2")

        if st.button("Plot"):

            try:
                x = np.linspace(-10,10,400)
                y = eval(expr)

                fig, ax = plt.subplots()
                ax.plot(x,y)
                ax.grid(True)

                st.pyplot(fig)

            except:
                st.error("Invalid Function")