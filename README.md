# Compound V2 Wallet Credit Scoring

## Overview
This project implements a rule-based credit scoring system to evaluate Compound V2 Ethereum wallets based on their historical transaction behavior. The goal is to distinguish between trustworthy and risky wallets, promoting protocol health and user engagement.

## Objective
The credit scoring system assigns scores between **0 and 100** for each wallet, based on features like:
- Total deposits
- Frequency of deposits
- Activity span (days)
- Deposit frequency per day

Higher scores indicate responsible behavior, while lower scores indicate risky or exploitative behavior.

## Features
- **Rule-Based Scoring System**: Transparent and explainable scoring logic.
- **Wallet Behavior Analysis**: Compare high-scoring and low-scoring wallets.
- **Output**: A CSV file containing the top 1,000 wallets ranked by score.

## Project Structure
```
project/
│
├── analyze_credit_scores.py      # Main script for scoring wallets and generating outputs
├── data/
│   ├── raw_data.json             # Raw transaction data
│   ├── top_wallets.csv           # Output file with top 1,000 wallets
│
├── documentation/
│   ├── Credit_Scoring_Methodology.md  # Methodology document
│   ├── Wallet_Analysis.md             # Analysis of high/low-scoring wallets
│
├── README.md                     # Project overview
└── requirements.txt              # Python dependencies
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/compound-v2-credit-scoring.git
   cd compound-v2-credit-scoring
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the scoring script:
   ```bash
   python analyze_credit_scores.py
   ```

2. The top 1,000 wallets will be saved in `data/top_wallets.csv`.

3. Review the analysis documents in `documentation/`.

## Methodology
For details on the scoring logic and feature engineering, refer to the [Credit Scoring Methodology](documentation/Credit_Scoring_Methodology.md).

## Results
- The scoring system identifies wallets based on their historical behavior.
- High-scoring wallets demonstrate responsible, protocol-aligned activities.
- Low-scoring wallets exhibit risky or bot-like behavior.

## Contributing
Feel free to open issues or submit pull requests for improvements.

## License
This project is licensed under the MIT License. See `LICENSE` for details.
