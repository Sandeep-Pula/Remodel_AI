import pandas as pd
import numpy as np

# Load your data
data = pd.read_csv("Remodel_AI.csv")

# Convert date columns to datetime and ensure they are in the correct order
date_columns = ['pre_engaged_date', 'engaged_date', 'warm_date', 'cold_date', 'customer_date']
data[date_columns] = data[date_columns].apply(pd.to_datetime, errors='coerce')

def check_date_order(row):
    dates = row[date_columns].dropna().sort_values()
    if dates.is_monotonic_increasing:
        return row
    return None

# Apply the function to clean up rows with out-of-order dates
valid_data = data.apply(check_date_order, axis=1).dropna()

# Define the scoring functions
def check_pre_engaged(row):
    if pd.notna(row['pre_engaged_date']):
        return 0.1  # Initial interest shown
    return 0

def check_engaged(row):
    if pd.notna(row['engaged_date']) and row['engaged_date'] > row['pre_engaged_date']:
        return 0.2  # Active engagement
    return 0

def check_warm(row):
    if pd.notna(row['warm_date']) and row['warm_date'] > row['engaged_date']:
        return 0.3  # Serious consideration
    return 0

def check_cold_and_customer(row):
    score = 0
    if pd.notna(row['cold_date']):
        if row['cold_date'] > row['warm_date']:
            score -= 0.2  # Decline in interest
            if pd.notna(row['customer_date']) and row['customer_date'] > row['cold_date']:
                score += 0.6  # Recovery and conversion to customer
        else:
            score -= 0.1  # Penalize for lack of clarity in data or process
    elif pd.notna(row['customer_date']) and row['customer_date'] > row['warm_date']:
        score += 0.4  # Smooth conversion without decline
    return score

def decision_tree_scoring(row):
    score = 0
    score += check_pre_engaged(row)
    score += check_engaged(row)
    score += check_warm(row)
    score += check_cold_and_customer(row)
    return max(score, 0)  # Ensure score does not go negative

# Apply the decision tree scoring function to the valid data
valid_data['Likelihood of Conversion'] = valid_data.apply(decision_tree_scoring, axis=1).clip(0, 1)

# Display the final data with likelihood of conversion scores
print(valid_data[['pre_engaged_date', 'engaged_date', 'warm_date', 'cold_date', 'customer_date', 'Likelihood of Conversion']].head())
