import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
def load_data(file_path):
    """
    Load the top wallets CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        print(data.head())
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Plot the distribution of scores
def plot_score_distribution(data):
    """
    Plot the distribution of credit scores.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data['score'], bins=20, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Distribution of Credit Scores', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y')
    plt.show()

# Identify outliers using a boxplot
def identify_outliers(data):
    """
    Identify outliers in credit scores using a boxplot.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data['score'], color='orange')
    plt.title('Boxplot of Credit Scores', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.grid(axis='x')
    plt.show()

# Analyze top and bottom wallets
def analyze_wallets(data):
    """
    Analyze the wallets with the highest and lowest scores.
    """
    print("\nTop 5 Wallets with Highest Scores:")
    print(data.nlargest(5, 'score'))

    print("\nTop 5 Wallets with Lowest Scores:")
    print(data.nsmallest(5, 'score'))

# Perform correlation analysis
def analyze_correlations(processed_file, score_column='score'):
    """
    Analyze correlations between score and other features.
    """
    try:
        processed_data = pd.read_csv(processed_file)
        correlations = processed_data.corr()
        print("\nCorrelations with Score:")
        print(correlations[score_column])

        # Heatmap for correlation matrix
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Matrix', fontsize=16)
        plt.show()
    except Exception as e:
        print(f"Error analyzing correlations: {e}")

# Main execution
if __name__ == "__main__":
    # Path to the top_wallets.csv file
    top_wallets_file = r'C:\Users\Manobhiram\Desktop\New proj scoring,py\top_wallets.csv'

    # Path to the processed_data.csv file (optional for correlation analysis)
    processed_data_file = r'C:\Users\Manobhiram\Desktop\New proj scoring,py\processed_data.csv'

    # Load the data
    data = load_data(top_wallets_file)

    if data is not None:
        # Plot the distribution of scores
        plot_score_distribution(data)

        # Identify outliers
        identify_outliers(data)

        # Analyze top and bottom wallets
        analyze_wallets(data)

        # Perform correlation analysis (if processed_data.csv is available)
        analyze_correlations(processed_data_file)