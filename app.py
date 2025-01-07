import streamlit as st
import requests
import folium
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_folium import st_folium

# Constants for APIs (use environment variables for better security)
OSRM_API_URL = "http://router.project-osrm.org/route/v1/driving"
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")  # Store your API keys securely
AQICN_API_KEY = os.getenv("AQICN_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Emission Factors (grams per km)
EMISSIONS_FACTORS = {
    'electric': 0,
    'gasoline': 120,  # grams CO2 per km
    'diesel': 150,    # grams CO2 per km
}

# Initialize session state for persisting results
if "results" not in st.session_state:
    st.session_state["results"] = None

st.title("Real-Time Route Optimization with Emission & Weather Visualization")
st.sidebar.header("Vehicle & Route Information")

# Input Fields
start_location = st.sidebar.text_input("Enter starting point (e.g., city name)", "New Delhi")
end_location = st.sidebar.text_input("Enter destination (e.g., city name)", "Bangalore")
vehicle_type = st.sidebar.selectbox("Select Vehicle Type", ['electric', 'gasoline', 'diesel'])

# Function to convert location name to coordinates using Nominatim
def get_coordinates(location_name):
    try:
        location_name = location_name + ", India"  # Adding country for accuracy
        url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json"

        headers = {
            "User-Agent": "MyApp/1.0 (contact@example.com)"
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                lat = float(data[0]['lat'])
                lng = float(data[0]['lon'])
                return lat, lng
            else:
                st.error(f"Could not find the location: {location_name}. Please check the spelling or try a more specific name.")
                return None
        else:
            st.error(f"Error fetching coordinates: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred while fetching coordinates for {location_name}: {str(e)}")
        return None

# Fetch route data from OSRM and extract the directions along with coordinates
def get_route_data(origin_coords, destination_coords):
    origin_lat, origin_lon = origin_coords
    destination_lat, destination_lon = destination_coords

    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{destination_lon},{destination_lat}?overview=full&geometries=geojson&alternatives=true"

    try:
        response = requests.get(osrm_url)
        response.raise_for_status()

        data = response.json()

        if 'routes' in data and data['routes']:
            routes = data['routes']
            all_directions = []
            all_route_coords = []

            for route in routes:
                route_geometry = route['geometry']['coordinates']
                route_coords = [(lat, lon) for lon, lat in route_geometry]
                all_route_coords.append(route_coords)

            return all_route_coords, routes

        else:
            return None, None

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None, None

# Fetch weather data using OpenWeatherMap API
def fetch_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }
        return weather
    else:
        return {"temperature": None, "humidity": None, "description": "N/A"}

# Calculate emissions for a route
def calculate_emissions(distance, vehicle_type):
    distance_km = distance / 1000  # OSRM gives distance in meters
    emissions = EMISSIONS_FACTORS[vehicle_type] * distance_km
    return emissions

# Create a folium map with route details
def create_route_map(routes, origin_coords, destination_coords):
    route_map = folium.Map(location=[(origin_coords[0] + destination_coords[0]) / 2,
                                     (origin_coords[1] + destination_coords[1]) / 2],
                           zoom_start=6)

    folium.Marker(location=origin_coords, popup="Origin", icon=folium.Icon(color='green')).add_to(route_map)
    folium.Marker(location=destination_coords, popup="Destination", icon=folium.Icon(color='red')).add_to(route_map)

    colors = ['blue', 'green', 'purple', 'orange', 'red']
    for idx, route in enumerate(routes):
        color = colors[idx % len(colors)]
        folium.PolyLine(locations=route, color=color, weight=3, opacity=0.6).add_to(route_map)

    return route_map

# Generate and display results
def generate_route_and_emissions():
    origin_coords = get_coordinates(start_location)
    destination_coords = get_coordinates(end_location)

    if origin_coords and destination_coords:
        st.write(f"Origin coordinates: {origin_coords}")
        st.write(f"Destination coordinates: {destination_coords}")
        
        route_coords, routes = get_route_data(origin_coords, destination_coords)
        if not routes:
            st.error("No routes found from OSRM.")
            return

        emissions_data = [calculate_emissions(route['distance'], vehicle_type) for route in routes]

        # Fetch weather data
        weather_data = [fetch_weather_data(*origin_coords), fetch_weather_data(*destination_coords)]

        # Create the map
        route_map = create_route_map(route_coords, origin_coords, destination_coords)

        # Save results to session state
        st.session_state["results"] = {
            "map": route_map,
            "emissions": emissions_data,
            "weather": weather_data,
        }

# Display results
# Display enhanced results with better visuals
def display_results():
    if st.session_state["results"]:
        # Fetch results from session state
        emissions_data = st.session_state["results"]["emissions"]
        weather_data = st.session_state["results"]["weather"]
        route_map = st.session_state["results"]["map"]

        # Emissions Comparison Chart
        st.subheader("Emissions Data (grams of CO2 per route)")
        fig_emissions = go.Figure()
        for idx, emissions in enumerate(emissions_data, start=1):
            fig_emissions.add_trace(
                go.Bar(
                    name=f"Route {idx}",
                    x=[f"Route {idx}"],
                    y=[emissions],
                    text=[f"{emissions:.2f} g"],
                    textposition="auto",
                )
            )
        fig_emissions.update_layout(
            title="Emissions per Route",
            xaxis_title="Routes",
            yaxis_title="Emissions (grams of CO2)",
            barmode="group",
            template="plotly_dark",
        )
        st.plotly_chart(fig_emissions, use_container_width=True)

        # Weather Data Chart
        st.subheader("Weather Data at Origin and Destination")
        weather_labels = ["Origin", "Destination"]
        temperatures = [weather["temperature"] for weather in weather_data]
        humidities = [weather["humidity"] for weather in weather_data]

        fig_weather = go.Figure()

        # Add Temperature
        fig_weather.add_trace(
            go.Bar(
                name="Temperature (°C)",
                x=weather_labels,
                y=temperatures,
                marker_color="orange",
                text=[f"{temp:.1f} °C" if temp is not None else "N/A" for temp in temperatures],
                textposition="auto",
            )
        )

        # Add Humidity
        fig_weather.add_trace(
            go.Scatter(
                name="Humidity (%)",
                x=weather_labels,
                y=humidities,
                mode="lines+markers",
                line=dict(color="blue"),
                text=[f"{hum}% Humidity" if hum is not None else "N/A" for hum in humidities],
            )
        )

        fig_weather.update_layout(
            title="Weather Data at Key Locations",
            xaxis_title="Location",
            yaxis_title="Temperature (°C) / Humidity (%)",
            template="plotly_dark",
        )
        st.plotly_chart(fig_weather, use_container_width=True)

        # Display Map
        st.subheader("Map of Routes")
        st_folium(route_map, width=700, height=500)

        # Display raw weather data
        st.subheader("Detailed Weather Data")
        st.write(f"**Origin Weather:** {weather_data[0]}")
        st.write(f"**Destination Weather:** {weather_data[1]}")

# Run the application
if st.button("Generate Route & Calculate Emissions"):
    generate_route_and_emissions()

display_results()
