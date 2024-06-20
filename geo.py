import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the datasets
data_path = 'Expanded_Remodel_AI.csv'
data = pd.read_csv(data_path)

zip_data_path = 'uszips.xlsx'
zip_data = pd.read_excel(zip_data_path)

# Create a base map
map_center = [37.0902, -95.7129]  # Center of the US
base_map = folium.Map(location=map_center, zoom_start=4)

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(base_map)

# Aggregate the data by city, state, and country
city_data = data.groupby(['city', 'state', 'country'], as_index=False)['number_of_interactions'].sum()

# Merge the city data with the zip code data
merged_data = pd.merge(city_data, zip_data, left_on='city', right_on='city')

# Plot the interactions on the map
for _, row in merged_data.iterrows():
    location = [row['lat'], row['lon']]
    folium.Marker(
        location=location,
        popup=f"{row['city']}, {row['state']}: {row['number_of_interactions']} interactions",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Save the map to an HTML file
output_map_path = 'interaction_map.html'
base_map.save(output_map_path)

print(f"Map has been saved to {output_map_path}")
