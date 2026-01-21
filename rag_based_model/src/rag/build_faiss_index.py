"""
Build FAISS vector index from guideline chunks.
Uses sentence-transformers for embeddings.
"""
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import faiss
import numpy as np
import pickle
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from pathlib import Path


class FAISSIndexBuilder:
    """
    Creates and manages FAISS vector index for guideline retrieval.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize with embedding model.
        
        Args:
            model_name: HuggingFace sentence-transformer model name
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = None
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for text chunks.
        
        Args:
            texts: List of text strings
            
        Returns:
            Numpy array of embeddings (n_texts, embedding_dim)
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings
    
    def build_index(self, chunks: List[Dict[str, str]]) -> faiss.Index:
        """
        Build FAISS index from chunks.
        
        Args:
            chunks: List of chunk dictionaries with 'text' field
            
        Returns:
            FAISS index object
        """
        # Store chunks for later retrieval
        self.chunks = chunks
        
        # Extract texts
        texts = [chunk["text"] for chunk in chunks]
        
        print(f"Creating embeddings for {len(texts)} chunks...")
        embeddings = self.create_embeddings(texts)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index (using IndexFlatIP for inner product = cosine similarity)
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"FAISS index built with {self.index.ntotal} vectors")
        
        return self.index
    
    def save_index(self, index_dir: str):
        """
        Save FAISS index and chunks to disk.
        
        Args:
            index_dir: Directory to save index files
        """
        index_path = Path(index_dir)
        index_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_path / "faiss.index"))
        
        # Save chunks metadata
        with open(index_path / "chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        
        # Save model name for loading later
        with open(index_path / "config.pkl", "wb") as f:
            pickle.dump({"model_name": self.model_name}, f)
        
        print(f"Index saved to {index_dir}")
    
    @classmethod
    def load_index(cls, index_dir: str) -> Tuple[faiss.Index, List[Dict[str, str]], str]:
        """
        Load FAISS index and chunks from disk.
        
        Args:
            index_dir: Directory containing index files
            
        Returns:
            Tuple of (index, chunks, model_name)
        """
        index_path = Path(index_dir)
        
        # Load FAISS index
        index = faiss.read_index(str(index_path / "faiss.index"))
        
        # Load chunks
        with open(index_path / "chunks.pkl", "rb") as f:
            chunks = pickle.load(f)
        
        # Load config
        with open(index_path / "config.pkl", "rb") as f:
            config = pickle.load(f)
        
        print(f"Index loaded from {index_dir}")
        print(f"Index contains {index.ntotal} vectors")
        
        return index, chunks, config["model_name"]


def build_and_save_index(
    chunks: List[Dict[str, str]],
    output_dir: str = "data/faiss_index",
    model_name: str = "all-MiniLM-L6-v2"
):
    """
    Convenience function to build and save index in one step.
    
    Args:
        chunks: Guideline chunks from ingestion
        output_dir: Where to save index
        model_name: Embedding model to use
    """
    builder = FAISSIndexBuilder(model_name=model_name)
    builder.build_index(chunks)
    builder.save_index(output_dir)
    
    return builder


if __name__ == "__main__":
    # Example: Build index from ingested guidelines
    from ingest_guidelines import GuidelineIngester
    
    # Ingest guidelines
    ingester = GuidelineIngester(chunk_size=300, overlap=50)
    chunks = ingester.ingest("data/guidelines/ada_guidelines.txt")
    
    print(f"\n{'='*60}")
    print("Building FAISS Index")
    print(f"{'='*60}\n")
    
    # Build and save index
    builder = build_and_save_index(
        chunks=chunks,
        output_dir="data/faiss_index",
        model_name="all-MiniLM-L6-v2"
    )
    
    print(f"\n{'='*60}")
    print("Index Build Complete")
    print(f"{'='*60}")