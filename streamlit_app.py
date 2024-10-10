import streamlit as st
import geocoder
from geopy.distance import geodesic

# Coordinates for the library (replace with actual values)
LIBRARY_LATITUDE = 24.8676352
LIBRARY_LONGITUDE = 67.076096
ALLOWED_RADIUS = 50  # meters

# Function to check if the user is within the allowed radius
def is_within_radius(user_lat, user_lon, lib_lat, lib_lon, radius):
    user_location = (user_lat, user_lon)
    lib_location = (lib_lat, lib_lon)
    distance = geodesic(user_location, lib_location).meters
    return distance <= radius

st.subheader("Mark Attendance")

# Detect user's location via IP
g = geocoder.ip('me')
user_lat = g.latlng[0]
user_lon = g.latlng[1]

st.write(f"Detected Latitude: {user_lat}")
st.write(f"Detected Longitude: {user_lon}")

# Check if the user is within the allowed radius
if st.button("Mark Attendance"):
    if user_lat and user_lon:
        if is_within_radius(user_lat, user_lon, LIBRARY_LATITUDE, LIBRARY_LONGITUDE, ALLOWED_RADIUS):
            st.success("You are within the library. Attendance marked.")
        else:
            st.error("You are not within the library's allowed radius.")
    else:
        st.error("Could not retrieve your location.")
