import sys
import os
import pytest
from fastapi.testclient import TestClient

# Resolve project path root mapping
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app
from src.nlp.evaluate import apply_legal_heuristics, calculate_metrics

client = TestClient(app)

def test_api_health_endpoint():
    """Verifies that the root API node responds correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["engine_status"] == "Online"

def test_legal_heuristics_booster():
    """Ensures legal trigger keywords properly adjust risk scores."""
    base_score = 0.50
    # Text with a trigger word should get a 15% boost (0.50 + 0.15 = 0.65)
    boosted_score = apply_legal_heuristics("This clause shall terminate the contract.", base_score)
    assert boosted_score == 0.65

    # Text without trigger words should remain unchanged
    neutral_score = apply_legal_heuristics("The office walls are painted white.", base_score)
    assert neutral_score == 0.50

def test_evaluation_metrics_calculation():
    """Validates the precision, recall, and F1 calculation utility."""
    y_true = [1, 0, 1, 0]
    y_pred = [1, 0, 0, 0] # 1 True Positive, 1 False Negative
    
    metrics = calculate_metrics(y_true, y_pred)
    assert "Precision" in metrics
    assert "Recall" in metrics
    assert "F1-Score" in metrics

def test_invalid_file_upload_rejection():
    """Verifies that the API blocks non-PDF uploads."""
    # Attempting to upload a plain text file instead of a PDF
    files = {"file": ("test.txt", b"dummy text content", "text/plain")}
    response = client.post("/api/v1/analyze", files=files)
    assert response.status_code == 400
    assert "PDF files required" in response.json()["detail"]