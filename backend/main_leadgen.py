import pandas as pd
from backend.preprocess_utils import preprocess_and_score
from backend.lead_utils import enrich_lead
from tqdm import tqdm
import os

def run_full_leadgen_batch(input_csv: str, output_csv: str, chunksize: int = 100):

    if os.path.exists(output_csv):
        os.remove(output_csv)
    
    chunk_iter = pd.read_csv(input_csv, chunksize=chunksize)
    
    for i, chunk in enumerate(chunk_iter):
        print(f"Processing chunk {i + 1} ...")
        
        chunk_scored = preprocess_and_score(chunk)
        
        insights_list = []
        for _, row in tqdm(chunk_scored.iterrows(), total=len(chunk_scored), desc=f"GPT enrichment chunk {i+1}"):
            entry = row.to_dict()
            if "lead_score" not in entry or pd.isna(entry["lead_score"]):
                entry["lead_score"] = "N/A"
            insights = enrich_lead(entry)
            insights_list.append(insights.get("insights", ""))
        
        chunk_scored["insights"] = insights_list

        chunk_scored = chunk_scored.sort_values(by="lead_score", ascending=False, na_position="last")
        
        write_header = (i == 0)
        chunk_scored.to_csv(output_csv, mode='a', index=False, header=write_header)
    
    print(f"All chunks processed. Final output saved to {output_csv}")

if __name__ == "__main__":
    input_csv = "../data/input.csv"
    output_csv = "../data/final_enriched_leads.csv"
    run_full_leadgen_batch(input_csv, output_csv, chunksize=100)
