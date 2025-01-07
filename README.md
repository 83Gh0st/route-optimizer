# Real-Time Route Optimization with Emission & Weather Visualization

This project provides an interactive web application that optimizes routes based on various factors such as emissions and weather conditions. It helps users visualize the optimal routes for different vehicle types and view environmental data like emissions and weather forecasts at both the origin and destination.

The application uses real-time data for route calculations, emissions estimations, and weather information, helping individuals or organizations make informed decisions on their travel. The platform is powered by **Streamlit**, **Folium**, and other APIs, making it highly interactive and capable of processing various real-time data points.

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [How It Works](#how-it-works)
3. [Emissions Calculation](#emissions-calculation)
4. [Weather Data Integration](#weather-data-integration)
5. [API Integration](#api-integration)
6. [Route Calculation Process](#route-calculation-process)
7. [How to Use](#how-to-use)
8. [GitHub Repository Structure](#github-repository-structure)
9. [Contributing](#contributing)
10. [License](#license)

---

## Technologies Used

- **Streamlit**: A framework used to build the web interface, allowing users to interact with the application and visualize the results.
- **Folium**: A library used for generating maps that visualize the routes and geospatial data.
- **Plotly**: A library for creating interactive charts to visualize emissions and weather data.
- **OSRM (Open Source Routing Machine)**: An API for real-time route calculations based on driving data.
- **OpenWeatherMap**: A weather API that provides temperature, humidity, and weather descriptions for different locations.
- **Python**: Used to implement the backend of the application, integrating with the APIs and performing calculations.

---

## How It Works

1. **User Input**: 
    - Users provide the starting point, destination, and vehicle type (electric, gasoline, or diesel) via the sidebar.
  
2. **Route Calculation**:
    - Using the OSRM API, the application fetches multiple possible routes from the starting point to the destination and calculates the distances.

3. **Emissions Calculation**:
    - The application calculates emissions based on the vehicle type chosen by the user and the total distance traveled. The emissions are computed in grams of CO2 per kilometer using predefined emission factors for electric, gasoline, and diesel vehicles.

4. **Weather Data**:
    - The OpenWeatherMap API provides real-time weather data (temperature, humidity, and description) for both the origin and destination.

5. **Visualization**:
    - The application generates an interactive map that shows the calculated routes on a Folium map, with markers for the origin and destination.
    - The emission data is visualized using a bar chart to compare emissions for each route.
    - The weather data is displayed using a bar chart and line graph to show the temperature and humidity for both locations.

---

## Emissions Calculation

The emissions are calculated based on the type of vehicle selected. Emission factors for different vehicle types are predefined as follows:

- **Electric Vehicle**: 0 grams of CO2 per km (since electric vehicles do not emit CO2 directly while driving).
- **Gasoline Vehicle**: 120 grams of CO2 per km.
- **Diesel Vehicle**: 150 grams of CO2 per km.

### Formula for Emissions:
\[ \text{Emissions} = \text{Distance (km)} \times \text{Emission Factor (grams per km)} \]

- The application converts the distance provided by the OSRM API (in meters) to kilometers and multiplies it by the corresponding emission factor for the vehicle type.

---

## Weather Data Integration

The application integrates real-time weather data using the **OpenWeatherMap API**. The weather information includes:

- **Temperature** (in Celsius)
- **Humidity** (in percentage)
- **Description** (e.g., clear sky, clouds)

Weather data is fetched for both the origin and destination and is visualized using Plotly for comparison.

---

## API Integration

### 1. **OSRM API** (Route Calculation)

The OSRM API is used to fetch routes for the user's origin and destination coordinates. The URL for the API looks like this:
```
http://router.project-osrm.org/route/v1/driving/{longitude},{latitude};{destination_longitude},{destination_latitude}?overview=full&geometries=geojson&alternatives=true
```
- The API returns multiple possible routes, and the application extracts the route geometries and distances for further calculations.

### 2. **OpenWeatherMap API** (Weather Data)

The OpenWeatherMap API is used to get real-time weather data for the origin and destination. The request URL is structured like this:
```
http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric
```
- The API provides temperature, humidity, and description for each location.

---
![image](https://github.com/user-attachments/assets/9b8c1e72-a948-485c-b2c4-d144939f48c6)

## Route Calculation Process

1. **Geocoding**:
    - The application uses the Nominatim API from OpenStreetMap to convert the city names into geographical coordinates (latitude and longitude).

2. **Fetching Routes**:
    - After obtaining the coordinates, the OSRM API is called to calculate possible routes and their distances.

3. **Emissions Calculation**:
    - For each route, emissions are calculated using the emission factor for the selected vehicle type.

4. **Weather Fetching**:
    - The weather data for both the origin and destination is fetched from the OpenWeatherMap API.

5. **Map Generation**:
    - A Folium map is generated that displays all the routes with markers for the origin and destination.

6. **Visualization**:
    - The emissions and weather data are visualized using Plotly charts.

---

## How to Use

1. **Install Dependencies**:
    ```bash
    pip install streamlit requests folium matplotlib plotly streamlit-folium
    ```

2. **Set Up API Keys**:
    - Create accounts for the APIs used in the project (OSRM, OpenWeatherMap).
    - Store your API keys securely in environment variables (`TOMTOM_API_KEY`, `AQICN_API_KEY`, `OPENWEATHERMAP_API_KEY`).

3. **Run the App**:
    ```bash
    streamlit run app.py
    ```

4. **User Input**:
    - In the sidebar, input the starting point, destination, and vehicle type.

5. **Generate Results**:
    - Click on the "Generate Route & Calculate Emissions" button to calculate the route, emissions, and weather data.

---

## GitHub Repository Structure

```
/Real-Time-Route-Optimization
    ├── app.py                 # Main application file
    ├── requirements.txt       # List of dependencies
    ├── assets/                # Folder for static assets (e.g., images)
    ├── .env                   # Environment variables (API keys)
    ├── README.md              # Documentation file (this file)
```

---

## Contributing

Contributions are welcome! If you'd like to improve or extend the functionality of this project, feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

