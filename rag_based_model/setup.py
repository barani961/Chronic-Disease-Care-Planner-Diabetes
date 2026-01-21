"""
Setup script to build FAISS index from guidelines.
Run this once before using the care planner.
"""
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from pathlib import Path
from src.rag.ingest_guidelines import GuidelineIngester
from src.rag.build_faiss_index import build_and_save_index


def setup_system():
    """
    Complete setup process for the care planner.
    1. Ingest guidelines
    2. Build FAISS index
    3. Verify setup
    """
    print("\n" + "="*70)
    print("CHRONIC CARE PLANNER - SETUP")
    print("="*70 + "\n")
    
    # Check if guidelines file exists
    guideline_path = Path("data/guidelines/ada_guidelines.txt")
    if not guideline_path.exists():
        print("❌ Error: Guidelines file not found at data/guidelines/ada_guidelines.txt")
        print("   Please ensure the file exists before running setup.")
        return False
    
    print("✓ Guidelines file found\n")
    
    # Step 1: Ingest guidelines
    print("STEP 1: Ingesting Guidelines")
    print("-" * 70)
    ingester = GuidelineIngester(chunk_size=300, overlap=50)
    chunks = ingester.ingest(str(guideline_path))
    print(f"✓ Ingested {len(chunks)} chunks from guidelines\n")
    
    # Show chunk distribution
    structured_index = ingester.create_structured_index(chunks)
    print("Chunk distribution:")
    for category, category_chunks in structured_index.items():
        print(f"  • {category}: {len(category_chunks)} chunks")
    print()
    
    # Step 2: Build FAISS index
    print("\nSTEP 2: Building FAISS Index")
    print("-" * 70)
    builder = build_and_save_index(
        chunks=chunks,
        output_dir="data/faiss_index",
        model_name="all-MiniLM-L6-v2"
    )
    print()
    
    # Step 3: Verify setup
    print("\nSTEP 3: Verifying Setup")
    print("-" * 70)
    
    # Check if all required files exist
    required_files = [
        "data/faiss_index/faiss.index",
        "data/faiss_index/chunks.pkl",
        "data/faiss_index/config.pkl"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    print()
    
    if all_exist:
        print("="*70)
        print("✓ SETUP COMPLETE - System ready to use!")
        print("="*70)
        print("\nRun 'python main.py' to generate a care plan.")
        return True
    else:
        print("="*70)
        print("❌ SETUP INCOMPLETE - Some files are missing")
        print("="*70)
        return False


if __name__ == "__main__":
    success = setup_system()
    exit(0 if success else 1)