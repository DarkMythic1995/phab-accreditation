import pandas as pd
import numpy as np
from datetime import datetime

def load_data(file_path):
    """Load raw public health data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df):
    """Clean and validate data to ensure PHAB compliance."""
    df = df.drop_duplicates()
    print(f"Removed duplicates, {len(df)} records remain.")

    df['client_id'] = df['client_id'].fillna(-1)
    df['name'] = df['name'].fillna('Unknown')
    df['service_date'] = df['service_date'].fillna('1900-01-01')
    df['service_type'] = df['service_type'].fillna('Unknown')
    df['staff_id'] = df['staff_id'].fillna(-1)

    df['client_id'] = df['client_id'].astype(int)
    df['staff_id'] = df['staff_id'].astype(int)
    df['name'] = df['name'].str.strip().str.title()
    df['service_type'] = df['service_type'].str.strip().str.upper()

    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    df['service_date'] = df['service_date'].apply(
        lambda x: x if is_valid_date(x) else '1900-01-01'
    )

    print("Data cleaned and validated.")
    return df

def structure_data(df):
    """Structure data into PHAB-compliant format."""
    phab_df = df[['client_id', 'name', 'service_date', 'service_type', 'staff_id']].copy()
    phab_df.columns = [
        'Client_ID',
        'Client_Name',
        'Service_Date',
        'Service_Type',
        'Assigned_Staff_ID'
    ]

    phab_df = phab_df.sort_values(by=['Client_ID', 'Service_Date'])
    print("Data structured into PHAB-compliant format.")
    return phab_df

def save_data(df, output_path):
    """Save structured data to a CSV file."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    input_file = 'raw_health_data.csv'
    sample_data = {
        'client_id': [1001, 1002, 1001, np.nan, 1003],
        'name': ['john doe', 'Jane Smith', 'John Doe', 'Alice', None],
        'service_date': ['2023-06-15', '2023-06-16', '2023-06-15', 'invalid', '2023-06-17'],
        'service_type': ['Vaccination', 'TB Test', 'vaccination ', None, 'Vaccination'],
        'staff_id': [501, 502, 501, 503, np.nan]
    }
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv(input_file, index=False)

    df = load_data(input_file)
    if df is not None:
        cleaned_df = clean_data(df)
        structured_df = structure_data(cleaned_df)
        save_data(structured_df, 'phab_accreditation_data.csv')

if __name__ == "__main__":
    main()
