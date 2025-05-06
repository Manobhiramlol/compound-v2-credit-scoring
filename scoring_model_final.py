import pandas as pd
import json


# Function to load and normalize nested JSON
def load_data(files):
    """
    Load raw transaction data from multiple JSON files and dynamically handle transaction types.
    """
    dfs = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)

            # Check for all possible transaction keys dynamically
            available_keys = data.keys()  # Get all top-level keys in the JSON

            # Loop through potential transaction types and process those that exist
            all_dataframes = []
            for key, transaction_type in [
                ('deposits', 'deposit'),
                ('borrows', 'borrow'),
                ('repayments', 'repay'),
                ('withdrawals', 'withdraw'),
                ('liquidations', 'liquidation')
            ]:
                if key in available_keys:
                    df = pd.json_normalize(data, record_path=[key], meta=[
                        'liquidator.id',  # Flatten nested liquidator field
                        'liquidatee.id'   # Flatten nested liquidatee field
                    ], errors='ignore')  # Ignore if meta fields are missing
                    df['transaction_type'] = transaction_type  # Add transaction type column
                    all_dataframes.append(df)

            # Combine all transaction data for this file into one DataFrame
            if all_dataframes:
                combined_df = pd.concat(all_dataframes, ignore_index=True)
                dfs.append(combined_df)

    # Concatenate all files into a single DataFrame
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# Function to preprocess data and extract wallet-level features
def preprocess_data(data):
    """
    Preprocess raw data to extract wallet-level behavioral features, including liquidation roles.
    """
    # Ensure amountUSD is numeric
    data['amountUSD'] = pd.to_numeric(data['amountUSD'], errors='coerce')  # Convert to numeric, invalid entries become NaN

    # Drop rows with NaN in amountUSD
    data = data.dropna(subset=['amountUSD'])

    # Fix timestamp conversion
    data['timestamp'] = pd.to_numeric(data['timestamp'], errors='coerce')  # Convert to numeric first
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s', errors='coerce')  # Convert to datetime

    # Group by wallet address and calculate features
    features = data.groupby('account.id').agg({
        'amountUSD': ['sum', 'mean', 'std'],  # Transaction statistics
        'transaction_type': 'count',         # Transaction count
        'asset.symbol': 'nunique',           # Asset diversity
    })
    features.columns = ['_'.join(col) for col in features.columns]  # Flatten column names
    features.reset_index(inplace=True)

    # Calculate liquidation and borrow sums
    liquidation_sum = (
        data[data['transaction_type'] == 'liquidation']
        .groupby('account.id')['amountUSD'].sum()
        .rename('amountUSD_liquidation')  # Rename for clarity
    )
    borrow_sum = (
        data[data['transaction_type'] == 'borrow']
        .groupby('account.id')['amountUSD'].sum()
        .rename('amountUSD_borrow')  # Rename for clarity
    )

    # Merge liquidation and borrow sums into features
    features = features.merge(liquidation_sum, on='account.id', how='left')
    features = features.merge(borrow_sum, on='account.id', how='left')

    # Fill missing values with 0
    features['amountUSD_liquidation'] = features['amountUSD_liquidation'].fillna(0)
    features['amountUSD_borrow'] = features['amountUSD_borrow'].fillna(0)

    # Calculate liquidation to borrow ratio
    features['liquidation_to_borrow_ratio'] = (
        features['amountUSD_liquidation'] / features['amountUSD_borrow']
    ).fillna(0)

    # Count liquidator and liquidatee occurrences
    liquidator_count = (
        data[data['transaction_type'] == 'liquidation']
        .groupby('liquidator.id')['amountUSD'].count()
        .rename('liquidator_count')
    )
    liquidatee_count = (
        data[data['transaction_type'] == 'liquidation']
        .groupby('liquidatee.id')['amountUSD'].count()
        .rename('liquidatee_count')
    )

    # Merge liquidator and liquidatee counts into features
    features = features.merge(liquidator_count, left_on='account.id', right_index=True, how='left')
    features = features.merge(liquidatee_count, left_on='account.id', right_index=True, how='left')

    # Fill missing values with 0
    features['liquidator_count'] = features['liquidator_count'].fillna(0)
    features['liquidatee_count'] = features['liquidatee_count'].fillna(0)

    return features


# Function to calculate credit scores
def calculate_scores(data):
    """
    Calculate credit scores for wallets based on behavioral features, including liquidation roles.
    """
    data['score'] = 50  # Start with a base score

    # Reward good behavior
    data['score'] += (data['amountUSD_sum'] / data['transaction_type_count']).clip(0, 20)  # Normalize
    data['score'] += data['asset.symbol_nunique'] * 2  # Asset diversity

    # Penalize risky behavior
    data['score'] -= data['liquidation_to_borrow_ratio'] * 30  # Defaults

    # Penalize frequent liquidatee behavior
    data['score'] -= data['liquidatee_count'] * 5  # Each liquidation event reduces score

    # Reward frequent liquidator behavior (optional)
    data['score'] += data['liquidator_count'] * 2  # Each liquidation event increases score

    # Ensure scores are within 0-100
    data['score'] = data['score'].clip(0, 100)

    return data


# Main execution
if __name__ == "__main__":
    # File paths for the JSON files
    files = [
        r"C:\Users\Manobhiram\Desktop\New proj scoring,py\compoundV2_transactions_ethereum_chunk_0.json",
        r"C:\Users\Manobhiram\Desktop\New proj scoring,py\compoundV2_transactions_ethereum_chunk_1.json",
        r"C:\Users\Manobhiram\Desktop\New proj scoring,py\compoundV2_transactions_ethereum_chunk_2.json"
    ]

    # Step 1: Load and process the raw data
    raw_data = load_data(files)
    if raw_data.empty:
        print("No data was loaded. Please verify the dataset.")
    else:
        print("Raw data loaded successfully.")
        print(raw_data.head())

        # Step 2: Preprocess the data to extract features
        try:
            processed_data = preprocess_data(raw_data)
            print("Feature engineering completed.")
            print(processed_data.head())
        except Exception as e:
            print(f"Error during feature engineering: {e}")
            exit()

        # Step 3: Calculate credit scores
        try:
            scored_data = calculate_scores(processed_data)
            print("Credit scoring completed.")
            print(scored_data[['account.id', 'score']].head())
        except Exception as e:
            print(f"Error during credit scoring: {e}")
            exit()

        # Step 4: Save the top 1,000 wallets by score
        try:
            top_wallets = scored_data.nlargest(1000, 'score')
            top_wallets[['account.id', 'score']].to_csv('top_wallets.csv', index=False)
            print("Top 1,000 wallets saved to 'top_wallets.csv'.")
        except Exception as e:
            print(f"Error during saving the top wallets: {e}")