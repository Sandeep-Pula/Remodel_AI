import pandas as pd

# Load the data from the provided CSV file
file_path = 'Remodel_AI.csv'
data = pd.read_csv(file_path)

# Identify conversion by checking non-null entries in 'customer_date'
data['is_converted'] = ~data['customer_date'].isna()

# Calculate conversion rates by Zip Code, Country, and State
conversion_rates_zip = data.groupby('zip_code')['is_converted'].mean()
conversion_rates_country = data.groupby('country')['is_converted'].mean()
conversion_rates_state = data.groupby('state')['is_converted'].mean()

# Define the functions to score each geographical segment based on the actual conversion rates in the provided dataset

def score_zip_code(zip_code):
    if zip_code in conversion_rates_zip.index:
        rate = conversion_rates_zip.loc[zip_code]
        # High conversion likelihood if rate > 70%
        if rate > 0.7:
            return 0.5
        # Medium conversion likelihood if rate is between 40% and 70%
        elif 0.4 < rate <= 0.7:
            return 0.3
        # Low conversion likelihood if rate < 40%
        else:
            return 0.1
    # Default score if zip code not found
    return 0  

def score_country(country):
    if country in conversion_rates_country.index:
        rate = conversion_rates_country.loc[country]
        # High conversion likelihood if rate > 70%
        if rate > 0.7:
            return 0.3
        # Medium conversion likelihood if rate is between 40% and 70%
        elif 0.4 < rate <= 0.7:
            return 0.2
        # Low conversion likelihood if rate < 40%
        else:
            return 0.05
    # Default score if country not found
    return 0  

def score_state(state):
    if state in conversion_rates_state.index:
        rate = conversion_rates_state.loc[state]
        # High conversion likelihood if rate > 70%
        if rate > 0.7:
            return 0.2
        # Medium conversion likelihood if rate is between 40% and 70%
        elif 0.4 < rate <= 0.7:
            return 0.1
        # Low conversion likelihood if rate < 40%
        else:
            return 0.05
    # Default score if state not found
    return 0  

# Applying these functions to the dataset to get scores for each lead
data['zip_score'] = data['zip_code'].apply(score_zip_code)
data['country_score'] = data['country'].apply(score_country)
data['state_score'] = data['state'].apply(score_state)

# Aggregate the zip, country, and state scores to create a final likelihood score
data['likelihood_score'] = (data['zip_score'] + data['country_score'] + data['state_score']) / 3

# Display some of the results including the aggregated score
print(data[['zip_code', 'country', 'state', 'zip_score', 'country_score', 'state_score', 'likelihood_score']].head())
