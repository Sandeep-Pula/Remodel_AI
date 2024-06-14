import pandas as pd

def load_data(file_path):
    """ Load data from a CSV file """
    return pd.read_csv(file_path)

def categorize_age(data):
    """ Categorize lead age into groups """
    age_bins = [18, 30, 45, 60, float('inf')]
    age_labels = ['18-30', '31-45', '46-60', '60+']
    data['Age Group'] = pd.cut(data['lead_age'], bins=age_bins, labels=age_labels, right=False)
    return data

def get_base_score(lead_status):
    """ Assign a base score based on the lead status """
    if lead_status == 'Active':
        return 0.7
    elif lead_status == 'Inactive':
        return 0.3
    elif lead_status == 'Closed':
        return 0.1
    else:
        return 0.5  # Default score for other statuses

def get_interaction_score(interactions):
    """ Calculate additional score based on the number of interactions """
    if interactions > 20:
        return 0.3
    elif interactions > 10:
        return 0.2
    elif interactions > 5:
        return 0.1
    else:
        return 0.0

def get_profession_scores(data):
    """ Calculate average conversion rate for each profession """
    profession_conversion_rates = data.groupby('lead_profession')['is_converted'].mean()
    return profession_conversion_rates

def get_profession_score(profession, profession_scores):
    """ Assign a score based on the lead profession """
    return profession_scores.get(profession, 0.5)  # Default score if profession not found

def calculate_score(lead_status, interactions, profession, profession_scores):
    """ Calculate the total likelihood score combining base, interaction, and profession scores """
    base_score = get_base_score(lead_status)
    interaction_score = get_interaction_score(interactions)
    profession_score = get_profession_score(profession, profession_scores)
    total_score = (base_score + interaction_score + profession_score) / 3  # Average the scores
    return min(total_score, 1.0)  # Ensure the total does not exceed 1

def calculate_likelihood_scores(data, profession_scores):
    """ Apply scoring to each record in the dataset """
    data['Likelihood Score'] = data.apply(
        lambda x: calculate_score(x['lead_status'], x['number_of_interactions'], x['lead_profession'], profession_scores),
        axis=1
    )
    return data

def save_data(data, output_path):
    """ Save the data to a CSV file """
    data.to_csv(output_path, index=False)

def display_data(data, num_records=20):
    """ Display specified number of records from the data """
    result = data[['lead_profession', 'lead_age', 'Age Group', 'number_of_interactions', 'lead_status', 'Likelihood Score']].head(num_records)
    print(result)

# Main execution
file_path = 'Remodel_AI.csv'
output_path = 'DG_LS_Leadage_LeadIndustry_dataset.csv'

data = load_data(file_path)

# Preprocess the data
data['is_converted'] = ~data['customer_date'].isna()
data = categorize_age(data)

# Calculate profession scores
profession_scores = get_profession_scores(data)

# Calculate likelihood scores
data = calculate_likelihood_scores(data, profession_scores)

# Save and display the data
save_data(data, output_path)
display_data(data)
