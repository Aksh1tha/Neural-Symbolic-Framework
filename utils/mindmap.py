"""
Mind Map Generator Module
=========================
This module generates visual mind maps from text content using
NetworkX for graph construction and Matplotlib for rendering.

The module provides:
- Text analysis and key phrase extraction
- Graph construction with NetworkX
- Visual mind map generation with Matplotlib

Author: FreeMind AI
Version: 1.0.0
"""

import re
from typing import List, Optional, Tuple
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


class MindMapGenerator:
    """
    A class for generating visual mind maps from text content.
    
    Uses NetworkX to create directed graphs and Matplotlib to
    render them as visual mind maps. The generator extracts
    key concepts and relationships from text to build the graph.
    
    Attributes:
        max_nodes: Maximum number of nodes to display
        layout_algo: Graph layout algorithm to use
    """
    
    def __init__(self, max_nodes: int = 15):
        """
        Initialize the MindMapGenerator.
        
        Args:
            max_nodes: Maximum number of nodes to include in the mind map
        """
        self.max_nodes = max_nodes
        self.layout_algo = 'spring'  # Can be 'spring', 'kamada_kawai', 'circular'
    
    def generate_mindmap(self, text: str, title: str = "Main Topic") -> plt.Figure:
        """
        Generate a mind map visualization from text.
        
        Analyzes the input text to extract key concepts and relationships,
        then creates a visual representation using NetworkX and Matplotlib.
        
        Args:
            text: The text content to visualize
            title: Title for the central node
            
        Returns:
            Matplotlib figure object containing the mind map
        """
        if not text or not text.strip():
            # Return empty mind map
            return self._create_empty_figure(title)
        
        try:
            # Extract key concepts from text
            key_concepts = self._extract_key_concepts(text)
            
            # Create the graph
            G = nx.DiGraph()
            
            # Add central node
            G.add_node(title, level=0)
            
            # Add concept nodes and edges
            if key_concepts:
                self._add_concepts_to_graph(G, key_concepts, title)
            
            # Create and return the visualization
            return self._create_visualization(G, title)
            
        except Exception as e:
            st.error(f"Mind map generation error: {str(e)}")
            return self._create_empty_figure(title)
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts from the text.
        
        Uses frequency analysis and pattern matching to identify
        important terms and phrases in the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of key concepts
        """
        if not text:
            return []
        
        # Clean text
        clean_text = text.lower()
        
        # Extract potential key terms
        # Pattern for important noun phrases (simplified)
        patterns = [
            r'\b([a-z]{4,}\s+[a-z]{4,})\b',  # Multi-word terms
            r'\b([a-z]{5,})\b',               # Single longer words
        ]
        
        all_matches = []
        for pattern in patterns:
            matches = re.findall(pattern, clean_text)
            all_matches.extend(matches)
        
        # Filter and rank by frequency
        word_freq = {}
        for word in all_matches:
            word = word.strip()
            if len(word) > 3:  # Skip very short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and get top concepts
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Extract top concepts
        concepts = []
        seen = set()
        
        for word, freq in sorted_words:
            if len(concepts) >= self.max_nodes:
                break
            
            # Skip duplicates and very common words
            if word in seen:
                continue
            
            # Skip if word appears only once (likely not significant)
            if freq < 2 and len(sorted_words) > 10:
                continue
            
            seen.add(word)
            concepts.append(word.title())
        
        return concepts
    
    def _add_concepts_to_graph(self, G: nx.DiGraph, concepts: List[str], central_node: str):
        """
        Add concept nodes and edges to the graph.
        
        Creates a hierarchical structure with the central topic
        connected to main concepts, and sub-concepts connected
        to their parent concepts.
        
        Args:
            G: NetworkX graph to modify
            concepts: List of concepts to add
            central_node: Name of the central node
        """
        num_concepts = len(concepts)
        
        # Calculate how many levels we need
        if num_concepts <= 5:
            # All concepts connected directly to center
            for i, concept in enumerate(concepts):
                G.add_node(concept, level=1)
                G.add_edge(central_node, concept)
        elif num_concepts <= 10:
            # Some concepts have sub-concepts
            mid = num_concepts // 2
            main_concepts = concepts[:mid]
            sub_concepts = concepts[mid:]
            
            for i, concept in enumerate(main_concepts):
                G.add_node(concept, level=1)
                G.add_edge(central_node, concept)
            
            for i, concept in enumerate(sub_concepts):
                parent_idx = i % mid
                parent = main_concepts[parent_idx]
                G.add_node(concept, level=2)
                G.add_edge(parent, concept)
        else:
            # Create a more complex hierarchy
            # Level 1: Main categories (first 3)
            # Level 2: Sub-categories (next 6)
            # Level 3: Details (rest)
            
            main_concepts = concepts[:3]
            sub_concepts = concepts[3:9]
            detail_concepts = concepts[9:]
            
            # Add main concepts
            for concept in main_concepts:
                G.add_node(concept, level=1)
                G.add_edge(central_node, concept)
            
            # Add sub-concepts
            for i, concept in enumerate(sub_concepts):
                parent_idx = i % len(main_concepts)
                parent = main_concepts[parent_idx]
                G.add_node(concept, level=2)
                G.add_edge(parent, concept)
            
            # Add detail concepts
            for i, concept in enumerate(detail_concepts):
                parent_idx = i % len(sub_concepts)
                parent = sub_concepts[parent_idx]
                G.add_node(concept, level=3)
                G.add_edge(parent, concept)
    
    def _create_visualization(self, G: nx.DiGraph, title: str) -> plt.Figure:
        """
        Create a matplotlib visualization of the graph.
        
        Generates a styled mind map with the central topic in
        the center and related concepts radiating outward.
        
        Args:
            G: NetworkX graph to visualize
            title: Title of the mind map
            
        Returns:
            Matplotlib figure object
        """
        # Create figure with appropriate size
        if len(G.nodes()) <= 5:
            fig_size = (10, 8)
        elif len(G.nodes()) <= 10:
            fig_size = (12, 10)
        else:
            fig_size = (14, 12)
        
        fig, ax = plt.subplots(figsize=fig_size, dpi=100)
        
        if len(G.nodes()) == 1:
            # Only central node
            ax.text(0.5, 0.5, title, ha='center', va='center', 
                   fontsize=16, fontweight='bold', color='#2E86AB',
                   transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        # Choose layout based on graph size
        if self.layout_algo == 'spring':
            try:
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            except:
                pos = nx.kamada_kawai_layout(G)
        elif self.layout_algo == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)
        
        # Get node levels for coloring
        node_levels = nx.get_node_attributes(G, 'level')
        level_colors = {0: '#2E86AB', 1: '#28A745', 2: '#FFC107', 3: '#DC3545'}
        node_colors = [level_colors.get(node_levels.get(node, 1), '#6C757D') 
                      for node in G.nodes()]
        
        # Get node sizes
        node_sizes = []
        for node in G.nodes():
            level = node_levels.get(node, 1)
            if level == 0:
                node_sizes.append(4000)
            elif level == 1:
                node_sizes.append(2000)
            elif level == 2:
                node_sizes.append(1500)
            else:
                node_sizes.append(1000)
        
        # Draw edges with styling
        nx.draw_networkx_edges(
            G, pos,
            edge_color='#495057',
            width=2,
            alpha=0.6,
            arrows=True,
            arrowsize=20,
            arrowstyle='-|>',
            connectionstyle='arc3,rad=0.1',
            ax=ax
        )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.9,
            ax=ax
        )
        
        # Draw labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(
            G, pos,
            labels,
            font_size=9,
            font_weight='bold',
            font_color='white',
            ax=ax
        )
        
        # Set title
        ax.set_title(f"Mind Map: {title}", fontsize=14, fontweight='bold', 
                    pad=20, color='#343A40')
        
        # Remove axes
        ax.axis('off')
        
        # Add legend
        self._add_legend(ax, node_levels)
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
    
    def _add_legend(self, ax, node_levels):
        """
        Add a legend to the visualization.
        
        Shows the meaning of different node colors based on
        their level in the hierarchy.
        
        Args:
            ax: Matplotlib axes object
            node_levels: Dictionary mapping nodes to their levels
        """
        legend_elements = []
        level_labels = {0: 'Central Topic', 1: 'Main Concepts', 
                       2: 'Sub-Concepts', 3: 'Details'}
        level_colors = {0: '#2E86AB', 1: '#28A745', 2: '#FFC107', 3: '#DC3545'}
        
        from matplotlib.patches import Patch
        
        unique_levels = sorted(set(node_levels.values()))
        for level in unique_levels:
            if level in level_labels:
                legend_elements.append(
                    Patch(facecolor=level_colors.get(level, '#6C757D'),
                         label=level_labels.get(level, f'Level {level}'))
                )
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc='upper left', 
                     fontsize=8, framealpha=0.9)
    
    def _create_empty_figure(self, title: str) -> plt.Figure:
        """
        Create an empty figure when no valid data is available.
        
        Args:
            title: Title to display
            
        Returns:
            Empty Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
        ax.text(0.5, 0.5, f"No content available\nfor: {title}", 
               ha='center', va='center', fontsize=14, color='#6C757D',
               transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig
    
    def save_mindmap(self, fig: plt.Figure, output_path: str):
        """
        Save the mind map figure to a file.
        
        Args:
            fig: Matplotlib figure to save
            output_path: Path where to save the image
        """
        try:
            fig.savefig(output_path, format='png', dpi=300, 
                       bbox_inches='tight', facecolor='white')
        except Exception as e:
            st.warning(f"Could not save mind map: {str(e)}")
