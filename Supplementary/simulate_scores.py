import pandas as pd
import numpy as np
import math

# --- Model Parameters (from math_model_v2_comprehensive.md) ---
W_TECH = 0.40
W_HUMAN = 0.35
W_GOV = 0.25
SHADOW_LAMBDA = 0.5
# -------------------------------------------------------------

def calculate_score(row):
    """
    Calculates the final risk score for a single SME profile (row).
    """
    # 1. Critical Failure Constraint (Omega)
    if row['has_critical_failure']:
        return 0.0
    
    # 2. Base Score Calculation
    base_score = (W_TECH * row['tech_score']) + \
                 (W_HUMAN * row['human_score']) + \
                 (W_GOV * row['gov_score'])
    
    # 3. Shadow IT Decay (Psi)
    shadow_ratio = row['shadow_it_ratio']
    decay = math.exp(-SHADOW_LAMBDA * shadow_ratio)
    
    final_score = base_score * decay
    return final_score

def run_simulation(input_path, output_path):
    """
    Loads the synthetic dataset, runs the scoring simulation,
    and saves the results.
    """
    try:
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} profiles from {input_path}")
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_path}. Please run generate_sme_data.py first.")
        return

    # Apply the scoring model to each row
    df['final_risk_score'] = df.apply(calculate_score, axis=1)
    
    # Add a qualitative rating
    def get_rating(score):
        if score >= 90: return "Resilient"
        if score >= 70: return "Good"
        if score >= 50: return "At Risk"
        return "Critical"
        
    df['rating'] = df['final_risk_score'].apply(get_rating)

    try:
        df.to_csv(output_path, index=False)
        print(f"Simulation results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results: {e}")
        
    return df

# --- EXECUTION ---
if __name__ == "__main__":
    input_dataset_path = "PAPER/5_Experiments_Simulations/synthetic_sme_dataset.csv"
    output_results_path = "PAPER/6_Analysis_Results/simulation_results.csv"
    
    results_df = run_simulation(input_dataset_path, output_results_path)
    
    if results_df is not None:
        print("\n--- Simulation Results Summary ---")
        print(results_df[['id', 'final_risk_score', 'rating']].head())
        print("\n--- Score Distribution ---")
        print(results_df['final_risk_score'].describe())
        print("\n--- Rating Distribution ---")
        print(results_df['rating'].value_counts())
        print("\n-------------------------------\n")
