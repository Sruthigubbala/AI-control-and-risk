import sys
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
import shutil

# Root alignment mapping injection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api.app_gateway import ContractIntelligenceEngine

app = FastAPI(
    title="Zaalima Development Contract Intelligence API Node",
    description="Production-Level Legal Document NLP Extraction Platform Node.",
    version="1.0.0"
)

# Instantiate our core pipeline worker engine
engine = ContractIntelligenceEngine()

@app.get("/")
def system_status():
    return {
        "engine_status": "Online",
        "active_project": "Project 1: AI-Powered Contract Intelligence & Risk Scoring (NLP)",
        "docs_url": "http://127.0.0.1:8000/docs"
    }

@app.post("/api/v1/analyze")
async def analyze_document_endpoint(file: UploadFile = File(...)):
    """
    Ingests raw PDF contracts, triggers asynchronous OCR processing, 
    and handles downstream evaluation modeling blocks.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid extension asset. PDF files required.")
        
    # Generate local path storage layouts
    cache_directory = "data/raw"
    os.makedirs(cache_directory, exist_ok=True)
    destination_file_path = os.path.join(cache_directory, file.filename)
    
    # Save the upload stream to the local file layout securely
    try:
        with open(destination_file_path, "wb") as storage_buffer:
            shutil.copyfileobj(file.file, storage_buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disk I/O caching failure: {str(e)}")
        
    # Trigger the asynchronous pipeline block
    analysis_payload = await engine.run_pipeline_async(destination_file_path)
    
    return {
        "status": "Success",
        "payload": analysis_payload
    }