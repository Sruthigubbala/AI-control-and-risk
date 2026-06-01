import torch
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

def apply_legal_heuristics(text: str, model_confidence: float) -> float:
    """
    Post-processing heuristic: Boosts confidence score if highly aggressive
    legal trigger keywords are present in the text segment.
    """
    trigger_words = ["shall", "terminate", "indemnity", "liability", "breach", "bankruptcy"]
    text_lower = text.lower()
    
    # If a critical word is present, boost the confidence score by 15%
    boost = 0.0
    if any(word in text_lower for word in trigger_words):
        boost = 0.15
        
    final_score = min(model_confidence + boost, 1.0) # Cap at maximum 1.0
    return final_score

def calculate_metrics(y_true, y_pred):
    """Calculates precision, recall, and f1 score for Week 2 evaluation."""
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    return {
        "Precision": f"{(precision * 100):.2f}%",
        "Recall": f"{(recall * 100):.2f}%",
        "F1-Score": f"{(f1 * 100):.2f}%"
    }

if __name__ == "__main__":
    print("Initializing Post-Processing Heuristics & Metrics evaluation...")
    
    # Simulated validation targets (ground truth labels)
    true_labels = [1, 0, 1, 0, 1]
    
    # Simulated raw model output probabilities
    raw_model_confidences = [0.42, 0.12, 0.88, 0.35, 0.48]
    
    # Validation sentences corresponding to predictions
    validation_texts = [
        "The agreement shall terminate upon written notice.",
        "The office has blue chairs and nice desks.",
        "Total liability caps shall not exceed fifty thousand dollars.",
        "We look forward to working on mutual projects.",
        "Either party may file for bankruptcy if liquidation occurs."
    ]
    
    # Apply post-processing heuristics
    final_predictions = []
    print("\n--- Applying Post-Processing Heuristics ---")
    for i, text in enumerate(validation_texts):
        raw_conf = raw_model_confidences[i]
        adjusted_conf = apply_legal_heuristics(text, raw_conf)
        
        # Binary Classification threshold: 0.50
        binary_pred = 1 if adjusted_conf >= 0.50 else 0
        final_predictions.append(binary_pred)
        
        print(f"Txt Preview: '{text[:35]}...' | Raw: {raw_conf:.2f} -> Adjusted: {adjusted_conf:.2f} | Pred: {binary_pred}")
        
    # Calculate performance
    scores = calculate_metrics(true_labels, final_predictions)
    print("\n--- Final Week 2 Performance Metrics ---")
    for metric, val in scores.items():
        print(f"{metric}: {val}")