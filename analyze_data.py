import pandas as pd
import os
import matplotlib.pyplot as plt

# Define paths
base_path = r"C:\Users\Admin\Desktop\UIDAI\master assets"
files = {
    "biometric": os.path.join(base_path, "master_biometric_data.csv"),
    "demographic": os.path.join(base_path, "master_demographic_data.csv"),
    "enrolment": os.path.join(base_path, "master_enrolment_data.csv")
}

def load_data():
    dfs = {}
    
    # Load Biometric
    print("Loading Biometric Data...")
    try:
        # Format appears to be DD-MM-YYYY based on '01-03-2025'
        dfs['biometric'] = pd.read_csv(files['biometric'], parse_dates=['date'], dayfirst=True)
        print(f"Biometric: {dfs['biometric'].shape}")
    except Exception as e:
        print(f"Error loading biometric: {e}")

    # Load Demographic
    print("Loading Demographic Data...")
    try:
        # Format appears to be DD-MM-YYYY
        dfs['demographic'] = pd.read_csv(files['demographic'], parse_dates=['date'], dayfirst=True)
        print(f"Demographic: {dfs['demographic'].shape}")
    except Exception as e:
        print(f"Error loading demographic: {e}")

    # Load Enrolment
    print("Loading Enrolment Data...")
    try:
        # Format appears to be YYYY-MM-DD based on '2025-03-02'
        dfs['enrolment'] = pd.read_csv(files['enrolment'], parse_dates=['date'])
        print(f"Enrolment: {dfs['enrolment'].shape}")
    except Exception as e:
        print(f"Error loading enrolment: {e}")
        
    return dfs

def clean_and_summarize(dfs):
    summaries = {}
    
    for name, df in dfs.items():
        print(f"\n--- {name.upper()} SUMMARY ---")
        print(df.info())
        print("Missing Values:\n", df.isnull().sum())
        
        # Basic Stats for numeric columns
        print("numeric stats:\n", df.describe())
        
        # State-wise counts
        if 'state' in df.columns:
            print("\nTop 5 States by Row Count:")
            print(df['state'].value_counts().head())
            
            # Aggregate numeric columns by state
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            numeric_cols = [c for c in numeric_cols if c != 'pincode'] # Exclude pincode from summation
            
            if numeric_cols:
                state_stats = df.groupby('state')[numeric_cols].sum()
                print("\nTop 5 States by Total Activity:")
                # Sum across all numeric columns to get total 'activity' for identifying biggest contributors
                state_stats['total_activity'] = state_stats.sum(axis=1)
                print(state_stats.sort_values('total_activity', ascending=False)['total_activity'].head())

    return dfs

def analyze_temporal_trends(dfs):
    print("\n--- TEMPORAL TRENDS ---")
    for name, df in dfs.items():
        if 'date' in df.columns:
            # Group by date and sum numeric columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            numeric_cols = [c for c in numeric_cols if c != 'pincode']
            
            daily_stats = df.groupby('date')[numeric_cols].sum()
            print(f"\n{name} - Date Range: {df['date'].min()} to {df['date'].max()}")
            print(f"{name} - Days of data: {daily_stats.shape[0]}")
            print(f"{name} - Peak Day:\n", daily_stats.idxmax())

if __name__ == "__main__":
    dfs = load_data()
    if dfs:
        dfs = clean_and_summarize(dfs)
        analyze_temporal_trends(dfs)
