import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def load_data(file_path):
    """Load the dataset from the specified file path."""
    return pd.read_csv(file_path)

def aggregate_data(data, group_by_column, agg_column='number_of_interactions'):
    """Aggregate the dataset by a specific column and calculate total interactions."""
    aggregated_data = data.groupby(group_by_column).agg(
        total_interactions=(agg_column, 'sum')
    ).reset_index()
    return aggregated_data

def create_subplot_figure():
    """Create a subplot figure with specified vertical spacing."""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            'Total Interactions by Lead Source',
            'Total Interactions by Lead Industry',
            'Total Interactions by Preferred Communication Method'
        ),
        vertical_spacing=0.2  # Increase vertical spacing
    )
    return fig

def add_bar_trace(fig, data, x_col, y_col, row, col, color=None, coloraxis=None):
    """Add a bar trace to the subplot figure."""
    trace = go.Bar(
        x=data[x_col],
        y=data[y_col],
        marker=dict(color=color if color else data[y_col], coloraxis=coloraxis)
    )
    fig.add_trace(trace, row=row, col=col)

def update_layout(fig):
    """Update the layout of the figure."""
    fig.update_layout(
        height=1200,
        showlegend=False,
        title_text='Total Interactions by Different Categories',
        coloraxis=dict(colorscale='Viridis', colorbar=dict(title="Total Interactions"))
    )

def update_xaxes(fig):
    """Update the x-axis labels with a slight angle for better readability."""
    fig.update_xaxes(tickangle=0, row=1, col=1)
    fig.update_xaxes(tickangle=90, row=2, col=1)
    fig.update_xaxes(tickangle=0, row=3, col=1)

def main():
    file_path = 'Remodel_AI.csv'  # Replace this with the correct path
    data = load_data(file_path)

    source_data = aggregate_data(data, 'lead_source')
    industry_data = aggregate_data(data, 'lead_industry')
    communication_data = aggregate_data(data, 'preferred_communication')

    fig = create_subplot_figure()

    add_bar_trace(fig, source_data, 'lead_source', 'total_interactions', row=1, col=1, color='blue')
    add_bar_trace(fig, industry_data, 'lead_industry', 'total_interactions', row=2, col=1, coloraxis="coloraxis")
    add_bar_trace(fig, communication_data, 'preferred_communication', 'total_interactions', row=3, col=1, color='green')

    update_layout(fig)
    update_xaxes(fig)

    fig.show()

if __name__ == "__main__":
    main()
