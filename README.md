# FreeMind AI - Intelligent Document Analysis

<div align="center">

![FreeMind AI Logo](https://img.shields.io/badge/FreeMind-AI-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/python-3.8+-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-Free-yellow?style=for-the-badge)

**An intelligent document analysis tool with summarization, report generation, and mind map visualization.**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

FreeMind AI is a comprehensive web application that provides intelligent document analysis capabilities. It accepts various types of input including raw text, web article URLs, and PDF documents, then uses state-of-the-art AI models to generate concise summaries, structured reports, and visual mind maps.

The application runs entirely locally, ensuring your data never leaves your computer. It leverages open-source technologies including HuggingFace transformers for natural language processing, NetworkX for graph visualization, and Streamlit for the web interface.

This project is ideal for students, researchers, and professionals who need to quickly analyze and understand large documents without relying on cloud-based services or paid APIs.

## Features

### Text Input Methods

FreeMind AI supports three input methods to accommodate different document types and sources. You can paste raw text directly into the application for immediate analysis, provide a URL to extract and analyze web articles automatically, or upload PDF documents for processing. This flexibility makes the tool suitable for various use cases from academic research to business document analysis.

### AI-Powered Summarization

The application uses the facebook/bart-large-cnn model from HuggingFace to generate high-quality abstractive summaries. This model is specifically designed for document summarization and produces coherent, contextually accurate summaries that capture the main points of the original text. The summarization handles documents of varying lengths through intelligent chunking and merging strategies.

### Structured Report Generation

Beyond simple summaries, FreeMind AI generates complete structured reports with introduction, summary, and conclusion sections. These reports provide a formal framework for understanding the document content and can be downloaded as Markdown files for further use or integration into other workflows.

### Mind Map Visualization

The application creates visual mind maps that represent the key concepts and their relationships within the document. Using NetworkX for graph construction and Matplotlib for rendering, these visualizations help users quickly grasp the structure and main topics of complex documents. The mind maps use a color-coded hierarchical system to distinguish between central topics, main concepts, sub-concepts, and details.

### Privacy-First Design

All processing happens locally on your machine. The application downloads the AI model on first use and caches it for subsequent runs. Your documents are never sent to external servers, making FreeMind AI suitable for analyzing sensitive or confidential materials.

## Tech Stack

The application uses a carefully selected stack of open-source technologies to provide powerful AI capabilities while maintaining complete privacy and local operation.

**Frontend and Backend:** Streamlit serves as both the frontend interface and the web server. Streamlit's reactive programming model makes it easy to create interactive data applications with minimal code. The application runs in wide mode for better visualization of results.

**Natural Language Processing:** HuggingFace Transformers provides the core AI capabilities through the facebook/bart-large-cnn model. This model uses a sequence-to-sequence architecture trained specifically for summarization tasks. PyTorch serves as the backend framework for model inference.

**Document Processing:** PyPDF2 handles PDF text extraction, supporting standard text-based PDFs with automatic handling of encrypted documents. Newspaper3k provides robust web article extraction with proper encoding and content parsing.

**Visualization:** NetworkX creates the graph structure for mind maps, while Matplotlib renders the final visualizations. This combination provides publication-quality output that can be saved and shared.

## Installation

### Prerequisites

Before installing FreeMind AI, ensure you have Python 3.8 or higher installed on your system. You can verify your Python version by running:

```bash
python --version
# or
python3 --version
```

You will also need pip or conda for package management. For best performance, ensure you have at least 4GB of available RAM, as the AI model requires memory to load and run.

### Step 1: Clone or Download the Project

Download the FreeMind AI project files and navigate to the project directory:

```bash
cd freemind_ai
```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment helps isolate the project dependencies from your system Python installation. This is especially important as some packages may have specific version requirements.

Using venv:

```bash
python -m venv freemind_env
source freemind_env/bin/activate  # On Linux/Mac
# or
freemind_env\Scripts\activate     # On Windows
```

Using conda:

```bash
conda create -n freemind python=3.10
conda activate freemind
```

### Step 3: Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This will install all necessary packages including Streamlit, transformers, torch, PyPDF2, newspaper3k, networkx, and matplotlib. The installation may take several minutes on first run as it downloads the AI model weights.

**Note:** If you encounter any installation issues, try updating pip first:

```bash
pip install --upgrade pip
```

### Step 4: Verify Installation

Verify that all dependencies are correctly installed:

```bash
python -c "import streamlit; import transformers; import torch; print('All dependencies installed successfully!')"
```

## Quick Start

### Running the Application

Navigate to the project directory and launch the application using Streamlit:

```bash
cd freemind_ai
streamlit run app.py
```

The application will start and open automatically in your default web browser at `http://localhost:8501`. If it does not open automatically, you can manually navigate to this URL.

**First Run:** On the first run, the application will download the BART model (approximately 1.6GB) from HuggingFace. This may take several minutes depending on your internet connection. Subsequent runs will use the cached model and start much faster.

### Basic Usage

1. **Select Input Type:** Use the sidebar to choose how you want to provide content (Text, URL, or PDF).

2. **Provide Content:**
   - For Text: Paste or type your content into the text area
   - For URL: Enter the web address of an article
   - For PDF: Upload a PDF file using the file uploader

3. **Analyze:** Click the "Analyze Document" button in the sidebar to start processing.

4. **View Results:** After analysis completes, view the generated summary, report, and mind map in the main area using the tabs.

## Usage Guide

### Text Input Mode

When using text input, paste your content into the large text area. For best results, provide at least 200 characters of meaningful text. The application will preserve paragraph structure and formatting to maintain context for the summarization model.

### URL Extraction Mode

Enter the full URL of a web article including the protocol (http:// or https://). The application uses newspaper3k to extract the main article content, ignoring navigation, ads, and other page elements. Some websites may have protections that prevent extraction; in such cases, try copying the article text manually.

### PDF Upload Mode

Upload a PDF document using the file uploader. The application supports standard text-based PDFs. Scanned PDFs or image-only PDFs cannot be processed as they lack extractable text. Encrypted PDFs are detected and reported with an appropriate error message.

### Understanding Results

The Summary tab provides a concise overview of the document content. The Report tab offers a structured view with formal introduction, body, and conclusion sections. The Mind Map tab displays a visual representation of key concepts and their relationships, with the central topic in blue and related concepts in other colors.

## Project Structure

The FreeMind AI project is organized into a clean, modular structure that separates concerns and makes the code easy to understand and maintain.

```
freemind_ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
└── utils/
    ├── __init__.py          # Package initialization
    ├── extractor.py         # Text extraction from various sources
    ├── summarizer.py        # AI summarization and report generation
    └── mindmap.py          # Mind map visualization
```

**app.py** serves as the main application entry point, handling the web interface, user input, and coordination of all components. It manages the Streamlit page configuration, displays the sidebar and main content areas, and orchestrates the analysis workflow.

**utils/extractor.py** contains the TextExtractor class that handles text extraction from different input sources. It provides methods for processing raw text, downloading and parsing web articles from URLs, and reading PDF files with PyPDF2. The module includes robust error handling and text cleaning functions.

**utils/summarizer.py** implements the Summarizer class that interfaces with the HuggingFace transformers library. It loads and caches the BART model, handles text chunking for long documents, generates summaries, and creates structured reports with introduction, summary, and conclusion sections.

**utils/mindmap.py** provides the MindMapGenerator class for creating visual representations of document content. It analyzes text to extract key concepts, constructs a hierarchical graph using NetworkX, and renders the visualization using Matplotlib with color-coded node levels.

## Technical Details

### Model Architecture

The application uses BART (Bidirectional and Auto-Regressive Transformers) for sequence-to-sequence tasks, specifically the facebook/bart-large-cnn variant. This model was trained on the CNN/DailyMail dataset for summarization and excels at producing coherent, fluent summaries that capture the essential information from source documents.

BART combines a bidirectional encoder (like BERT) with an autoregressive decoder (like GPT), making it particularly effective for abstractive summarization where the model generates new text rather than simply extracting sentences.

### Text Chunking Strategy

For documents longer than the model's token limit (1024 tokens for BART), the application implements a sophisticated chunking strategy. Text is split at sentence boundaries to preserve meaning, and overlapping segments ensure no information is lost at chunk boundaries. Each chunk is summarized individually, and the resulting summaries are combined and optionally re-summarized for coherence.

### Graph Construction

The mind map generator uses a hierarchical approach to graph construction. The central topic forms the root node, and extracted key concepts are organized into levels based on their importance and frequency in the text. The spring layout algorithm positions nodes to minimize edge crossings while maintaining the hierarchical structure.

### Performance Considerations

Model loading is cached using Streamlit's @st.cache_resource decorator, ensuring the model is loaded only once per session. For long documents, progress indicators show the chunk processing status. The application limits PDF processing to 100 pages and total text to 100,000 characters to prevent memory issues.

## Troubleshooting

### Model Download Failures

If the model fails to download on first run, check your internet connection and try again. The application downloads from HuggingFace's model hub, which may experience temporary issues. You can manually download the model by running:

```python
from transformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
```

### Memory Issues

If you experience memory errors, try reducing the max_nodes parameter in MindMapGenerator or processing shorter documents. For systems with limited RAM, consider using the t5-small model instead of bart-large-cnn by changing the model_name parameter in the Summarizer class.

### PDF Reading Errors

PDF extraction requires text-based PDFs. If you receive an error reading a PDF, verify that it is not a scanned image or password-protected. You can test PDF text extraction using the following Python code:

```python
from PyPDF2 import PdfReader
reader = PdfReader("your_file.pdf")
text = page.extract_text() for page in reader.pages
```

### Web URL Extraction Failures

Some websites block automated access or use complex JavaScript rendering that newspaper3k cannot handle. In such cases, copy the article text manually and use the text input mode instead. Ensure the URL is complete and includes the protocol (https://).

## Contributing

Contributions are welcome! If you would like to improve FreeMind AI, please feel free to submit pull requests or open issues for discussion. Areas of particular interest include support for additional document formats, improved summarization models, and enhanced visualization options.

## License

FreeMind AI is released under the MIT License. This means you are free to use, modify, and distribute the software for personal and commercial purposes. The application uses open-source libraries including Streamlit, HuggingFace Transformers, PyTorch, NetworkX, and Matplotlib, each with their own licenses that permit free use.

---

<div align="center">

**FreeMind AI - Making Document Analysis Accessible to Everyone**

*Built with ❤️ using open-source technology*

</div>
