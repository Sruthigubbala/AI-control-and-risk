from fastapi import FastAPI, UploadFile, File
import shutil
import os
from src.ocr.pipeline import process_contract_pdf

app = FastAPI(title="Zalima Contract Intelligence Engine")

@app.get("/")
def home():
    """Root endpoint to verify the server is active."""
    return {
        "status": "Online",
        "project": "Project 1: AI-Powered Contract Intelligence & Risk Scoring (NLP)",
        "timeline_stage": "Week 1: Data Parsing & Baseline Modeling",
        "interactive_docs": "Go to http://127.0.0.1:8000/docs to upload contracts"
    }

@app.post("/upload-contract/")
async def upload_contract(file: UploadFile = File(...)):
    # Create directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)
    
    save_path = f"data/raw/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run Week 1 OCR pipeline task
    extracted_text = process_contract_pdf(save_path)
    
    return {
        "filename": file.filename,
        "status": "Successfully Parsed",
        "extracted_text_preview": extracted_text[:1000]
    }