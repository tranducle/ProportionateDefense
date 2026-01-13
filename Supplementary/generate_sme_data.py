import pandas as pd
import numpy as np

# Constants
N_SAMPLES = 1000

# Distributions based on Methodology V2
SECTORS = ["FinTech", "Retail", "Manufacturing", "Services"]
SIZES = ["Micro (<10)", "Small (10-50)", "Medium (50-250)"]

# Probabilities
P_SECTOR = [0.20, 0.30, 0.20, 0.30]
P_SIZE = [0.50, 0.35, 0.15]

def generate_dataset():
    """Generates a synthetic SME dataset based on predefined distributions."""
    
    # Create DataFrame
    df = pd.DataFrame(index=range(N_SAMPLES))
    df['id'] = [f"sme_{i:04d}" for i in range(N_SAMPLES)]
    
    # 1. Categorical Data
    df['sector'] = np.random.choice(SECTORS, N_SAMPLES, p=P_SECTOR)
    df['size'] = np.random.choice(SIZES, N_SAMPLES, p=P_SIZE)

    # 2. Correlated Continuous Data (Scores)
    # Assume Human factor is generally lower than Technical
    mean = [70, 55]  # Mean for Tech Score, Human Score
    cov = [[150, 60], [60, 200]]  # Covariance matrix
    tech_scores, human_scores = np.random.multivariate_normal(mean, cov, N_SAMPLES).T
    
    # Governance score independent, skewed high (most orgs have *some* policy)
    gov_scores = np.random.beta(a=5, b=2, size=N_SAMPLES) * 100
    
    # Clip scores to be within [0, 100]
    df['tech_score'] = np.clip(tech_scores, 10, 100)
    df['human_score'] = np.clip(human_scores, 0, 90)
    df['gov_score'] = np.clip(gov_scores, 20, 100)

    # 3. Shadow IT Ratio (LogNormal distribution for long tail)
    shadow_mu = -0.5
    shadow_sigma = 0.7
    df['shadow_it_ratio'] = np.random.lognormal(shadow_mu, shadow_sigma, N_SAMPLES)

    # 4. Critical Failures (as a rare event)
    df['has_critical_failure'] = np.random.choice([True, False], N_SAMPLES, p=[0.05, 0.95])
    
    print(f"Generated {N_SAMPLES} synthetic SME profiles.")
    return df

def save_dataset(df, path):
    """Saves the dataset to a CSV file."""
    try:
        df.to_csv(path, index=False)
        print(f"Dataset successfully saved to {path}")
    except Exception as e:
        print(f"Error saving dataset: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    dataset = generate_dataset()
    # Save in the location specified by the methodology document
    output_path = "PAPER/5_Experiments_Simulations/synthetic_sme_dataset.csv"
    save_dataset(dataset, output_path)
    
    # Display summary
    print("\n--- Dataset Summary ---")
    print(dataset.head())
    print("\n--- Statistical Overview ---")
    print(dataset.describe())
    print("\n-----------------------\n")
