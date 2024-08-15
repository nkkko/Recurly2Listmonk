import os
import pandas as pd
import json
from tqdm import tqdm
import argparse
import numpy as np

def clean_name(first_name, last_name):
    if pd.isna(first_name) and pd.isna(last_name):
        return ""
    return f"{first_name} {last_name}".strip()

def generate_attributes(row):
    attributes = {
        "account_code": row.get('account_code', np.nan),
        "account_username": row.get('account_username', np.nan),
        "account_company_name": row.get('account_company_name', np.nan),
        "account_has_billing_info": row.get('account_has_billing_info', np.nan),
        "account_created_at": row.get('account_created_at', np.nan),
        "account_address1": row.get('account_address1', np.nan),
        "account_address2": row.get('account_address2', np.nan),
        "account_city": row.get('account_city', np.nan),
        "account_state": row.get('account_state', np.nan),
        "account_postal_code": row.get('account_postal_code', np.nan),
        "account_country": row.get('account_country', np.nan),
        "account_phone": row.get('account_phone', np.nan),
        "account_vat_number": row.get('account_vat_number', np.nan),
        "account_tax_exempt": row.get('account_tax_exempt', np.nan),
        "modified_at": row.get('modified_at', np.nan),
        "account_closed_at": row.get('account_closed_at', np.nan),
        "account_acquisition_cost": row.get('account_acquisition_cost', np.nan),
        "account_acquisition_currency": row.get('account_acquisition_currency', np.nan),
        "account_acquisition_channel": row.get('account_acquisition_channel', np.nan),
        "account_acquisition_subchannel": row.get('account_acquisition_subchannel', np.nan),
        "account_acquisition_campaign": row.get('account_acquisition_campaign', np.nan),
        "account_acquisition_created_at": row.get('account_acquisition_created_at', np.nan),
        "account_acquisition_modified_at": row.get('account_acquisition_modified_at', np.nan),
        "parent_account_code": row.get('parent_account_code', np.nan),
        "primary_payment_method": row.get('primary_payment_method', np.nan),
        "billing_info_id": row.get('billing_info_id', np.nan),
        "dunning_campaign_code": row.get('dunning_campaign_code', np.nan),
        "dunning_campaign_id": row.get('dunning_campaign_id', np.nan),
        "preferred_locale": row.get('preferred_locale', np.nan)
    }
    # Remove keys with NaN values
    attributes = {k: v for k, v in attributes.items() if not pd.isna(v)}
    return json.dumps(attributes)

def split_dataframe(df, num_splits):
    chunk_size = int(np.ceil(len(df) / num_splits))
    return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

def save_splitted_files(dfs, base_filename):
    for i, df in enumerate(dfs):
        df.to_csv(f"{base_filename}_part_{i + 1}.csv", index=False)

def process_files(directory, split=None):
    combined_data = []

    files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    for filename in tqdm(files, desc="Processing files"):
        file_path = os.path.join(directory, filename)

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        for _, row in df.iterrows():
            email = row['account_email']
            if pd.isna(email) or email == "":
                continue  # Skip rows with missing or empty emails

            name = clean_name(row['account_first_name'], row['account_last_name'])
            attributes_json = generate_attributes(row)

            combined_data.append([email, name, attributes_json])

    combined_df = pd.DataFrame(combined_data, columns=['email', 'name', 'attributes'])

    if split and split > 0:
        split_dfs = split_dataframe(combined_df, split)
        save_splitted_files(split_dfs, "combined-recurly-export")
    else:
        combined_df.to_csv("combined-recurly-export.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and combine Recurly CSV files.")
    parser.add_argument("--split", type=int, default=None,
                        help="Number of files to split the combined CSV into.")
    args = parser.parse_args()
    export_directory = "export"
    process_files(export_directory, args.split)