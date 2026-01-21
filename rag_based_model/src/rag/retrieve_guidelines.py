"""
Retrieve relevant guidelines using FAISS semantic search.
Returns structured guideline data with citations.
"""

import faiss
import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from pathlib import Path


class GuidelineRetriever:
    """
    Retrieves relevant clinical guidelines using semantic search.
    """
    
    def __init__(self, index_dir: str = "data/faiss_index"):
        """
        Initialize retriever with pre-built FAISS index.
        
        Args:
            index_dir: Directory containing FAISS index files
        """
        from src.rag.build_faiss_index import FAISSIndexBuilder
        
        self.index, self.chunks, self.model_name = FAISSIndexBuilder.load_index(index_dir)
        self.model = SentenceTransformer(self.model_name)
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant guideline chunks.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with similarity scores
        """
        # Create query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search index
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Prepare results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            chunk = self.chunks[idx].copy()
            chunk["similarity_score"] = float(score)
            results.append(chunk)
        
        return results
    
    def extract_structured_guidelines(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract structured guideline information for care planning.
        
        Args:
            user_profile: User demographic and preference data
            health_data: Current health metrics
            
        Returns:
            Structured guideline dictionary with citations
        """
        # Define retrieval queries for different aspects
        queries = {
            "glycemic_targets": "diabetes glucose targets fasting postprandial HbA1c thresholds",
            "diet_guidelines": "diabetes nutrition diet carbohydrate fiber glycemic index foods",
            "activity_guidelines": "diabetes physical activity exercise aerobic resistance training",
            "safety_thresholds": "diabetes glucose red flag emergency hypoglycemia hyperglycemia"
        }
        
        # Retrieve for each query
        all_retrieved = {}
        for category, query in queries.items():
            results = self.retrieve(query, top_k=3)
            all_retrieved[category] = results
        
        # Structure the guidelines
        structured = {
            "diet_guidelines": self._extract_diet_guidelines(all_retrieved["diet_guidelines"]),
            "activity_guidelines": self._extract_activity_guidelines(all_retrieved["activity_guidelines"]),
            "safety_thresholds": self._extract_safety_thresholds(all_retrieved["safety_thresholds"]),
            "glycemic_targets": self._extract_glycemic_targets(all_retrieved["glycemic_targets"]),
            "citations": self._extract_citations(all_retrieved)
        }
        
        return structured
    
    def _extract_diet_guidelines(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract diet-related guidelines from retrieved chunks."""
        # Parse common patterns from chunks
        diet_info = {
            "carbs": "Emphasize low glycemic index foods",
            "fiber": "Minimum 25-30g per day",
            "avoid": ["refined carbohydrates", "sugary beverages", "added sugars"],
            "emphasize": [
                "non-starchy vegetables",
                "whole grains",
                "legumes",
                "lean proteins",
                "healthy fats"
            ],
            "recommendations": []
        }
        
        # Extract specific recommendations from chunks
        for chunk in chunks:
            text = chunk["text"]
            if "fiber" in text.lower():
                diet_info["recommendations"].append("Increase fiber intake from whole grains and vegetables")
            if "glycemic index" in text.lower():
                diet_info["recommendations"].append("Choose low glycemic index carbohydrates")
        
        return diet_info
    
    def _extract_activity_guidelines(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract physical activity guidelines from retrieved chunks."""
        activity_info = {
            "aerobic": "150 minutes per week of moderate-intensity activity",
            "strength": "2-3 sessions per week on non-consecutive days",
            "frequency": "At least 3 days per week with no more than 2 consecutive days without activity",
            "progression": "Start slowly if sedentary and progress gradually",
            "safety": [
                "Check glucose before and after exercise",
                "Carry fast-acting carbohydrate",
                "Stay hydrated"
            ]
        }
        
        return activity_info
    
    def _extract_safety_thresholds(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract safety thresholds from retrieved chunks."""
        thresholds = {
            "fasting_glucose": {
                "target_min": 80,
                "target_max": 130,
                "unit": "mg/dL"
            },
            "post_meal_glucose": {
                "target": 180,
                "unit": "mg/dL"
            },
            "red_flag_high": {
                "value": 250,
                "action": "Contact healthcare provider immediately",
                "unit": "mg/dL"
            },
            "red_flag_low": {
                "value": 70,
                "action": "Risk of hypoglycemia - contact healthcare provider",
                "unit": "mg/dL"
            }
        }
        
        return thresholds
    
    def _extract_glycemic_targets(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract glycemic target information."""
        targets = {
            "fasting": "80-130 mg/dL",
            "post_meal": "<180 mg/dL",
            "hba1c": "<7.0%",
            "population": "Most nonpregnant adults with diabetes"
        }
        
        return targets
    
    def _extract_citations(self, all_retrieved: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Extract unique citations from all retrieved chunks."""
        citations = set()
        
        for category_results in all_retrieved.values():
            for chunk in category_results:
                if "source" in chunk:
                    citations.add(chunk["source"])
        
        return sorted(list(citations))


if __name__ == "__main__":
    # Example usage
    retriever = GuidelineRetriever(index_dir="data/faiss_index")
    
    # Test retrieval
    print("Testing semantic search:")
    print("="*60)
    
    query = "What are the glucose targets for diabetes?"
    results = retriever.retrieve(query, top_k=3)
    
    print(f"\nQuery: {query}")
    print(f"\nTop {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. Section: {result['section']}")
        print(f"   Similarity: {result['similarity_score']:.3f}")
        print(f"   Text: {result['text'][:150]}...")
        print()
    
    # Test structured extraction
    print("\n" + "="*60)
    print("Testing structured guideline extraction:")
    print("="*60)
    
    user_profile = {"age": 45, "diet_type": "vegetarian"}
    health_data = {"avg_fasting_glucose": 160}
    
    guidelines = retriever.extract_structured_guidelines(user_profile, health_data)
    
    print("\nExtracted Guidelines:")
    print(f"\nDiet: {guidelines['diet_guidelines']['carbs']}")
    print(f"Fiber: {guidelines['diet_guidelines']['fiber']}")
    print(f"\nActivity: {guidelines['activity_guidelines']['aerobic']}")
    print(f"\nSafety Thresholds:")
    print(f"  Fasting glucose: {guidelines['safety_thresholds']['fasting_glucose']['target_min']}-{guidelines['safety_thresholds']['fasting_glucose']['target_max']} mg/dL")
    print(f"\nCitations: {', '.join(guidelines['citations'])}")