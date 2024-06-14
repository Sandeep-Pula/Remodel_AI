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

def aggregate_state_data(data):
    """Aggregate the dataset by state to get total interactions."""
    state_data = data.groupby('state_abbrev').agg(
        total_interactions=('number_of_interactions', 'sum')
    ).reset_index()
    return state_data

def add_full_state_names(state_data, state_fullname):
    """Add full state names to the dataframe for hover data."""
    state_data['state_fullname'] = state_data['state_abbrev'].map(state_fullname)
    return state_data

def plot_interactions_map(state_data):
    """Plot the region-wise map of interactions."""
    fig = px.choropleth(
        state_data,
        locations='state_abbrev',
        locationmode='USA-states',
        color='total_interactions',
        hover_name='state_fullname',
        hover_data=['total_interactions'],
        scope='usa',
        color_continuous_scale='Viridis',
        title='Region-wise Map of Interactions'
    )
    fig.show()

# Main script
file_path = 'Remodel_AI.csv'
data = load_data(file_path)
state_abbrev = get_state_abbreviations()
state_fullname = {v: k for k, v in state_abbrev.items()}

data = map_state_abbreviations(data, state_abbrev)
state_data = aggregate_state_data(data)
state_data = add_full_state_names(state_data, state_fullname)

plot_interactions_map(state_data)
