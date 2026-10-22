# Credit Card Fraud Detection & Risk Analytics

## Project Overview
This project analyzes credit card transactions and builds machine-learning models to identify potentially fraudulent transactions.

## Business Problem
Credit card fraud is a highly imbalanced classification problem. The goal is to detect fraudulent transactions while reducing missed fraud cases and unnecessary false alerts.

## Objectives
- Analyze transaction and fraud patterns
- Handle severe class imbalance
- Build Logistic Regression and Random Forest models
- Evaluate models using Precision, Recall, F1-score and ROC-AUC
- Identify important predictive features
- Prepare business metrics for Power BI
- Perform SQL-based fraud analysis

## Dataset
The project uses the Kaggle Credit Card Fraud Detection dataset containing 284,807 transactions and 492 fraud cases.

## Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- SQL
- Power BI
- GitHub

## Project Structure
```text
Credit-Card-Fraud-Detection/
├── data/
│   └── creditcard.csv
├── src/
│   └── fraud_detection.py
├── sql/
│   └── fraud_analysis.sql
├── notebooks/
├── dashboard/
├── images/
├── outputs/
├── requirements.txt
└── README.md
```

## How to Run in VS Code

1. Open this folder in VS Code.
2. Open the VS Code terminal.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it on Windows PowerShell:
   `.env\Scripts\Activate.ps1`
5. Install packages:
   `pip install -r requirements.txt`
6. Run:
   `python src/fraud_detection.py`

The script creates charts in `images/` and analysis files in `outputs/`.

## Important Metrics
For fraud detection, accuracy alone is not sufficient because the dataset is highly imbalanced. The project focuses on:
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

## Resume Project Title
**Credit Card Fraud Detection & Risk Analytics**

## Resume Description
Developed a machine-learning based credit card fraud detection project using Python and Scikit-learn; performed exploratory data analysis, addressed class imbalance, compared Logistic Regression and Random Forest models using Precision, Recall, F1-score and ROC-AUC, and prepared fraud-risk metrics for Power BI.
