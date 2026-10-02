import sys
import os
import csv
import json
import importlib.util
from pathlib import Path

def main():
    CURRENT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = CURRENT_DIR.parent
    SRC_DIR = PROJECT_ROOT / "src" / "application_contract_erview"
    
    sys.path.insert(0, str(SRC_DIR))
    
    inferance_path = SRC_DIR / "Core" / "Risk-assisment" / "inferance.py"
    spec = importlib.util.spec_from_file_location("inferance", inferance_path)
    inferance = importlib.util.module_from_spec(spec)
    sys.modules["inferance"] = inferance
    spec.loader.exec_module(inferance)
    
    execute_risk_inference = inferance.execute_risk_inference
    
    output_file = CURRENT_DIR / "benchmark_results.json"
    test_clauses = [
        {
            "category": "Indemnification",
            "text": "The Customer agrees to assume full responsibility and pay for all legal claims, losses, and liabilities arising out of this contract, including any claims caused solely by the Provider's own active negligence or willful misconduct."
        },
        {
            "category": "Termination",
            "text": "The Company may terminate this agreement at any time immediately without cause, without written notice, and without giving the breaching party any reasonable opportunity to cure or correct the breach."
        },
        {
            "category": "Limitation of Liability",
            "text": "The Provider's total monetary liability under this agreement shall be strictly capped at a maximum of $100, while the Customer's financial liability for any damage remains entirely unlimited."
        }
    ]
            
    results = []
    
    for i, row in enumerate(test_clauses):
        clause_text = row["text"]
        category_name = row["category"]
        
        print(f"Processing row {i+1}: Category='{category_name}'")
        print(f"Clause: {clause_text}")
        
        try:
            metrics = execute_risk_inference(clause_text, category_name)
            results.append({
                "row_index": i + 1,
                "clause_text": clause_text,
                "category": category_name,
                "metrics": metrics
            })
            print(f"  -> Result: {metrics.get('assessment_status')} - Violation: {metrics.get('has_violation')}")
            print(f"  -> Rule: {metrics.get('correct_rule_from_book')}")
            print(f"  -> Tier: {metrics.get('risk_tier')}")
        except Exception as e:
            print(f"  -> Error: {e}")
                
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nSuccessfully processed {len(results)} rows. Results saved to {output_file}")

if __name__ == "__main__":
    main()

