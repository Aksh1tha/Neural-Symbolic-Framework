"""
Summarizer Module
=================
This module handles text summarization and report generation using
HuggingFace transformers with the BART or T5 models.

The module provides:
- Abstractive text summarization
- Structured report generation
- Text chunking for long documents

Author: FreeMind AI
Version: 1.0.0
"""

from typing import Tuple, List, Optional
import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class Summarizer:
    """
    A class for generating summaries and structured reports from text.
    
    Uses the facebook/bart-large-cnn model for high-quality abstractive
    summarization. Handles long documents by chunking and processing
    in segments.
    
    Attributes:
        model_name: Name of the HuggingFace model to use
        max_input_length: Maximum token length for input text
        max_output_length: Maximum token length for generated summary
    """
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the Summarizer with model configuration.
        
        Args:
            model_name: Name of the HuggingFace model (default: bart-large-cnn)
        """
        self.model_name = model_name
        self.max_input_length = 1024  # BART token limit
        self.max_output_length = 300   # Summary token limit
        self._model = None
        self._tokenizer = None
    
    @st.cache_resource(show_spinner=False)
    def _load_model(self):
        """
        Load the summarization model and tokenizer.
        
        Uses Streamlit's cache_resource to ensure the model is loaded
        only once during the application lifetime.
        
        Returns:
            Tuple of (model pipeline, tokenizer)
        """
        try:
            # Check if CUDA is available for faster processing
            device = 0 if torch.cuda.is_available() else -1
            
            # Load the summarization pipeline
            summarizer = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                device=device
            )
            
            return summarizer
            
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            raise
    
    def summarize(self, text: str, max_length: int = None, min_length: int = None) -> str:
        """
        Generate a summary of the input text.
        
        Handles long texts by chunking them into segments that fit
        within the model's token limit, then combines the results.
        
        Args:
            text: The input text to summarize
            max_length: Maximum length of summary (default: 300 tokens)
            min_length: Minimum length of summary (default: 100 tokens)
            
        Returns:
            Generated summary text
        """
        if not text or not text.strip():
            return ""
        
        # Set default parameters
        max_length = max_length or self.max_output_length
        min_length = min_length or max(50, min(max_length // 3, 100))
        
        try:
            # Get the model pipeline
            summarizer = self._load_model()
            
            # Clean and prepare text
            clean_text = text.strip()
            
            # Estimate token count (rough approximation: 4 chars per token)
            estimated_tokens = len(clean_text) // 4
            
            # If text is short enough, process directly
            if estimated_tokens <= self.max_input_length - 50:
                result = summarizer(
                    clean_text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )
                return result[0]['summary_text']
            
            # For long texts, chunk and process
            return self._summarize_long_text(clean_text, summarizer, max_length, min_length)
            
        except Exception as e:
            st.error(f"Summarization error: {str(e)}")
            return ""
    
    def _summarize_long_text(self, text: str, summarizer, max_length: int, min_length: int) -> str:
        """
        Handle summarization of long texts by chunking.
        
        Splits the text into overlapping segments, summarizes each segment,
        then combines the results.
        
        Args:
            text: The input text
            summarizer: The loaded model pipeline
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Combined summary of all chunks
        """
        # Calculate chunk parameters
        overlap = 100  # Overlap in characters to maintain context
        max_chars = (self.max_input_length - 50) * 4  # Convert tokens to chars
        
        # Split text into sentences for better chunking
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Group sentences into chunks
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence)
            
            # Check if adding this sentence exceeds the limit
            if current_length + sentence_length > max_chars and current_chunk:
                # Save current chunk and start new one
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length + 1  # +1 for space
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Summarize each chunk
        summaries = []
        progress_bar = st.progress(0)
        
        for i, chunk in enumerate(chunks):
            try:
                # Skip very short chunks
                if len(chunk) < 100:
                    continue
                
                result = summarizer(
                    chunk,
                    max_length=max(min_length, min(max_length, len(chunk) // 4)),
                    min_length=min_length // 2,
                    do_sample=False,
                    truncation=True
                )
                
                if result:
                    summaries.append(result[0]['summary_text'])
                    
            except Exception as e:
                st.warning(f"Could not summarize chunk {i+1}: {str(e)}")
                continue
            
            # Update progress
            progress_bar.progress((i + 1) / len(chunks))
        
        progress_bar.empty()
        
        # Combine all summaries
        if not summaries:
            return ""
        
        # If we have multiple summaries, summarize them again
        combined_summary = ' '.join(summaries)
        
        if len(combined_summary) > 5000:
            # Final pass to consolidate
            final_result = summarizer(
                combined_summary,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            return final_result[0]['summary_text']
        
        return combined_summary
    
    def generate_report(self, summary: str, title: str = None) -> dict:
        """
        Generate a structured report from the summary.
        
        Creates a report with the following sections:
        - Title (provided or extracted)
        - Introduction
        - Summary
        - Conclusion
        
        Args:
            summary: The summarized text
            title: Optional title for the report
            
        Returns:
            Dictionary containing report sections
        """
        if not summary or not summary.strip():
            return {
                'title': title or 'Analysis Report',
                'introduction': '',
                'summary': '',
                'conclusion': ''
            }
        
        try:
            # Get the model pipeline
            summarizer = self._load_model()
            
            # Generate Introduction
            intro_prompt = f"Write a brief introduction for this text:\n\n{summary[:1000]}"
            intro_result = summarizer(
                intro_prompt,
                max_length=150,
                min_length=50,
                do_sample=False,
                truncation=True
            )
            introduction = intro_result[0]['summary_text']
            
            # Generate Conclusion
            conclusion_prompt = f"Write a conclusion based on this summary:\n\n{summary}"
            conclusion_result = summarizer(
                conclusion_prompt,
                max_length=150,
                min_length=50,
                do_sample=False,
                truncation=True
            )
            conclusion = conclusion_result[0]['summary_text']
            
            return {
                'title': title or 'Document Analysis Report',
                'introduction': introduction,
                'summary': summary,
                'conclusion': conclusion
            }
            
        except Exception as e:
            st.error(f"Report generation error: {str(e)}")
            return {
                'title': title or 'Analysis Report',
                'introduction': 'Failed to generate introduction',
                'summary': summary,
                'conclusion': 'Failed to generate conclusion'
            }
    
    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Extract key points from the text.
        
        Uses the summarization model to identify and extract
        the most important points from the input text.
        
        Args:
            text: The input text
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        if not text or not text.strip():
            return []
        
        try:
            summarizer = self._load_model()
            
            # Create prompts for extracting key points
            key_points = []
            sentences = text.split('. ')
            
            # For longer texts, sample important sentences
            if len(sentences) > num_points:
                # Get a summary first to identify important sections
                summary = self.summarize(text)
                
                # Extract sentences from summary
                summary_sentences = summary.split('. ')
                key_points = [s.strip() + '.' for s in summary_sentences[:num_points]]
            else:
                # For shorter texts, use all sentences
                key_points = [s.strip() + '.' for s in sentences[:num_points]]
            
            return key_points
            
        except Exception as e:
            st.warning(f"Could not extract key points: {str(e)}")
            return []
