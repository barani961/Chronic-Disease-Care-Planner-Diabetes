"""
Ingest clinical guidelines and prepare them for RAG.
Chunks text into manageable segments for embedding.
"""

import re
from typing import List, Dict
from pathlib import Path


class GuidelineIngester:
    """
    Processes clinical guideline documents into structured chunks.
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize ingester.
        
        Args:
            chunk_size: Target token count per chunk (approximate)
            overlap: Token overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def load_document(self, filepath: str) -> str:
        """
        Load guideline document from file.
        
        Args:
            filepath: Path to guideline text file
            
        Returns:
            Document content as string
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    def extract_sections(self, content: str) -> List[Dict[str, str]]:
        """
        Extract sections from structured guideline document.
        
        Args:
            content: Full document content
            
        Returns:
            List of section dictionaries
        """
        sections = []
        
        # Split by section headers (SECTION X:)
        section_pattern = r'SECTION \d+: (.+?)(?=SECTION \d+:|$)'
        matches = re.finditer(section_pattern, content, re.DOTALL)
        
        for match in matches:
            section_title = match.group(1).split('\n')[0].strip()
            section_content = match.group(1).strip()
            
            sections.append({
                "title": section_title,
                "content": section_content,
                "source": "ADA Standards of Care"
            })
        
        return sections
    
    def chunk_section(self, section: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Break a section into smaller chunks with overlap.
        
        Args:
            section: Section dictionary
            
        Returns:
            List of chunk dictionaries
        """
        content = section["content"]
        words = content.split()
        
        chunks = []
        start = 0
        
        while start < len(words):
            # Take chunk_size words
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "section": section["title"],
                "source": section["source"],
                "chunk_id": len(chunks)
            })
            
            # Move forward with overlap
            start += (self.chunk_size - self.overlap)
        
        return chunks
    
    def ingest(self, filepath: str) -> List[Dict[str, str]]:
        """
        Full ingestion pipeline.
        
        Args:
            filepath: Path to guideline document
            
        Returns:
            List of all chunks with metadata
        """
        # Load document
        content = self.load_document(filepath)
        
        # Extract sections
        sections = self.extract_sections(content)
        
        # Chunk each section
        all_chunks = []
        for section in sections:
            chunks = self.chunk_section(section)
            all_chunks.extend(chunks)
        
        # Add global IDs
        for idx, chunk in enumerate(all_chunks):
            chunk["global_id"] = idx
        
        return all_chunks
    
    def create_structured_index(self, chunks: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Organize chunks by topic for structured retrieval.
        
        Args:
            chunks: List of all chunks
            
        Returns:
            Dictionary mapping topics to relevant chunks
        """
        index = {
            "glycemic_targets": [],
            "nutrition": [],
            "physical_activity": [],
            "monitoring": [],
            "other": []
        }
        
        # Categorize chunks by keywords
        for chunk in chunks:
            text_lower = chunk["text"].lower()
            section_lower = chunk["section"].lower()
            
            if any(keyword in text_lower or keyword in section_lower 
                   for keyword in ["glucose", "glycemic", "hba1c", "target"]):
                index["glycemic_targets"].append(chunk)
            
            if any(keyword in text_lower or keyword in section_lower 
                   for keyword in ["nutrition", "diet", "food", "carbohydrate", "fiber"]):
                index["nutrition"].append(chunk)
            
            if any(keyword in text_lower or keyword in section_lower 
                   for keyword in ["activity", "exercise", "aerobic", "resistance"]):
                index["physical_activity"].append(chunk)
            
            if any(keyword in text_lower or keyword in section_lower 
                   for keyword in ["monitoring", "smbg", "glucose monitoring"]):
                index["monitoring"].append(chunk)
            
            # Check if already categorized
            categorized = any(chunk in index[key] for key in ["glycemic_targets", "nutrition", "physical_activity", "monitoring"])
            if not categorized:
                index["other"].append(chunk)
        
        return index


if __name__ == "__main__":
    # Example usage
    ingester = GuidelineIngester(chunk_size=300, overlap=50)
    
    # Ingest guidelines
    guideline_path = "data/guidelines/ada_guidelines.txt"
    chunks = ingester.ingest(guideline_path)
    
    print(f"Ingested {len(chunks)} chunks from guidelines")
    print(f"\nFirst chunk example:")
    print(f"Section: {chunks[0]['section']}")
    print(f"Text preview: {chunks[0]['text'][:200]}...")
    
    # Create structured index
    structured_index = ingester.create_structured_index(chunks)
    print(f"\nStructured index created:")
    for category, category_chunks in structured_index.items():
        print(f"  {category}: {len(category_chunks)} chunks")