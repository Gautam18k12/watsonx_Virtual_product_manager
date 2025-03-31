import pandas as pd
import os

def load_datasets():
    """
    Loads and preprocesses all datasets located in the data folder.
    Returns a dictionary of DataFrames keyed by a friendly name.
    """
    # Define the file mapping. Update paths/names as necessary.
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    file_map = {
        'teams': 'Teams_data.csv',
        'team_performance': 'TeamPerformance_data.csv',
        'sales': 'sales_data.csv',
        'ratings': 'ratings.csv',
        'products': 'Products_data.csv',
        'marketing': 'Marketing_data.csv',
        'complaints': 'Complaints_Data.csv',
        'campaigns': 'Campaigns_data.csv'
    }

    datasets = {}
    for key, file_name in file_map.items():
        file_path = os.path.join(base_path, file_name)
        try:
            df = pd.read_csv(file_path)
            # Standardize column names: trim, lowercase, replace non-alphanumeric chars with underscores.
            df.columns = df.columns.str.strip().str.lower().str.replace('[^a-z0-9_]', '_', regex=True)
            
            # Convert columns with "date" in their name to datetime objects.
            for col in df.columns:
                if 'date' in col:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Try converting object columns to numeric where possible, otherwise standardize strings.
            for col in df.select_dtypes(include=['object']).columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except Exception:
                    df[col] = df[col].astype(str).str.strip().str.upper()
                    
            datasets[key] = df
        except Exception as e:
            print(f"Failed to load {file_name}: {e}")
    return datasets

if __name__ == "__main__":
    # For quick local testing of the module.
    datasets = load_datasets()
    for key, df in datasets.items():
        print(f"{key}: {df.shape}")
