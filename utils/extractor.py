"""
Text Extractor Module
=====================
This module handles text extraction from various input sources:
- Raw text input
- URLs (using newspaper3k)
- PDF files (using PyPDF2)

Author: FreeMind AI
Version: 1.0.0
"""

import io
import re
from typing import Tuple, Optional
from urllib.parse import urlparse

import streamlit as st
from PyPDF2 import PdfReader
import newspaper
from newspaper import Article


class TextExtractor:
    """
    A class to extract and clean text from multiple input sources.
    
    This class provides methods to:
    - Extract text from raw input
    - Download and parse articles from URLs
    - Read and extract text from PDF files
    - Clean and normalize extracted text
    """
    
    def __init__(self):
        """Initialize the TextExtractor with necessary configurations."""
        self.min_text_length = 50  # Minimum characters to consider valid text
        self.max_text_length = 100000  # Maximum characters to process
        
    def extract_from_text(self, text: str) -> Tuple[str, Optional[str]]:
        """
        Process raw text input.
        
        Args:
            text: Raw text input from the user
            
        Returns:
            Tuple of (cleaned_text, None) since text input has no source title
        """
        if not text or not text.strip():
            return "", None
        
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < self.min_text_length:
            return "", None
            
        return cleaned_text, None
    
    def extract_from_url(self, url: str) -> Tuple[str, Optional[str]]:
        """
        Download and extract article content from a URL.
        
        Uses newspaper3k library to parse web articles and extract
        the main text content along with metadata like title and authors.
        
        Args:
            url: The URL of the article to extract
            
        Returns:
            Tuple of (article_text, article_title) or error message
            
        Raises:
            ValueError: If URL is invalid or inaccessible
        """
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
        
        # Validate URL format
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")
        
        try:
            # Create article object and configure
            article = Article(url)
            article.download()
            
            # Check if download was successful
            if not article.html:
                raise ValueError("Failed to download article content")
            
            article.parse()
            
            # Extract title (fallback to URL if not available)
            title = article.title if article.title else url
            
            # Get the main text content
            text = article.text
            
            if not text or len(text.strip()) < self.min_text_length:
                raise ValueError("Could not extract meaningful content from the URL")
            
            # Clean the extracted text
            cleaned_text = self._clean_text(text)
            
            return cleaned_text, title
            
        except newspaper.ArticleException as e:
            raise ValueError(f"Failed to parse article: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error accessing URL: {str(e)}")
    
    def extract_from_pdf(self, uploaded_file) -> Tuple[str, Optional[str]]:
        """
        Extract text content from an uploaded PDF file.
        
        Uses PyPDF2 to read PDF files page by page and extract
        the text content. Handles common PDF reading errors gracefully.
        
        Args:
            uploaded_file: Streamlit uploaded file object (PDF format)
            
        Returns:
            Tuple of (extracted_text, filename) or error message
            
        Raises:
            ValueError: If file is not a valid PDF or cannot be read
        """
        if uploaded_file is None:
            raise ValueError("No file uploaded")
        
        # Validate file type
        file_name = uploaded_file.name.lower()
        if not file_name.endswith('.pdf'):
            raise ValueError("File must be a PDF document")
        
        try:
            # Create PDF reader object
            pdf_reader = PdfReader(uploaded_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                raise ValueError("PDF is encrypted and cannot be read")
            
            # Extract text from all pages
            full_text = []
            num_pages = len(pdf_reader.pages)
            
            # Limit to first 100 pages to prevent memory issues
            max_pages = min(num_pages, 100)
            
            for i, page in enumerate(pdf_reader.pages[:max_pages]):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        full_text.append(page_text)
                except Exception as e:
                    st.warning(f"Could not extract text from page {i+1}")
                    continue
            
            if not full_text:
                raise ValueError("Could not extract any text from the PDF")
            
            # Combine all page texts
            combined_text = "\n".join(full_text)
            
            # Clean the extracted text
            cleaned_text = self._clean_text(combined_text)
            
            if len(cleaned_text) < self.min_text_length:
                raise ValueError("Extracted text is too short to analyze")
            
            # Use filename as title (without extension)
            title = file_name.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
            
            return cleaned_text, title
            
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Performs the following operations:
        - Removes excessive whitespace
        - Normalizes line breaks
        - Removes special characters (optional)
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and normalized text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
        text = re.sub(r' {2,}', ' ', text)       # Max 2 consecutive spaces
        text = re.sub(r'\t{2,}', '\t', text)     # Max 2 consecutive tabs
        
        # Remove page numbers and headers/footers patterns
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)  # Single line numbers
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def get_input_type_name(self, input_type: str) -> str:
        """
        Get a human-readable name for the input type.
        
        Args:
            input_type: The input type identifier
            
        Returns:
            Human-readable name
        """
        type_names = {
            'text': 'Text Input',
            'url': 'URL',
            'pdf': 'PDF Document'
        }
        return type_names.get(input_type, input_type)
