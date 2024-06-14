import pandas as pd
import plotly.express as px

def load_data(file_path):
    """Load the dataset from the specified file path."""
    return pd.read_csv(file_path)

def get_state_abbreviations():
    """Return a dictionary mapping full state names to their abbreviations."""
    return {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

def map_state_abbreviations(data, state_abbrev):
    """Map full state names to abbreviations in the dataset."""
    data['state_abbrev'] = data['state'].map(state_abbrev)
    return data

def aggregate_likelihood_data(data):
    """Aggregate the dataset by state to calculate the average likelihood score."""
    likelihood_data = data.groupby('state_abbrev').agg(
        avg_likelihood=('Likelihood Score', 'mean')
    ).reset_index()
    return likelihood_data

def add_full_state_names(data, state_fullname):
    """Add full state names to the dataframe for hover data."""
    data['state_fullname'] = data['state_abbrev'].map(state_fullname)
    return data

def plot_likelihood_map(likelihood_data):
    """Plot the region-wise map of likelihood scores."""
    fig = px.choropleth(
        likelihood_data,
        locations='state_abbrev',
        locationmode='USA-states',
        color='avg_likelihood',
        hover_name='state_fullname',
        hover_data=['avg_likelihood'],
        scope='usa',
        color_continuous_scale='Viridis',
        title='Region-wise Map of Likelihood Scores'
    )
    fig.show()

def main():
    """Main function to run the script."""
    file_path = 'DG_LS_Leadage_LeadIndustry_dataset.csv'  # Replace this with the correct path
    data = load_data(file_path)
    state_abbrev = get_state_abbreviations()
    state_fullname = {v: k for k, v in state_abbrev.items()}

    data = map_state_abbreviations(data, state_abbrev)

    if 'Likelihood Score' in data.columns:
        likelihood_data = aggregate_likelihood_data(data)
        likelihood_data = add_full_state_names(likelihood_data, state_fullname)
        plot_likelihood_map(likelihood_data)
    else:
        print("Column 'Likelihood Score' not found in the data.")

if __name__ == "__main__":
    main()
