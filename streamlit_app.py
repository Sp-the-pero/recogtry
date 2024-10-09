import streamlit as st
from geopy.distance import geodesic

# Coordinates for the library (replace with actual values)
LIBRARY_LATITUDE = 24.8676352
LIBRARY_LONGITUDE = 67.076096
ALLOWED_RADIUS = 50  # meters

def is_within_radius(user_lat, user_lon, lib_lat, lib_lon, radius):
  user_location = (user_lat, user_lon)
  lib_location = (lib_lat, lib_lon)
  distance = geodesic(user_location, lib_location).meters
  return distance <= radius

st.subheader("Mark Attendance")

# JavaScript code to automatically get location and pass it to Streamlit
geolocation_script = """
    <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById("user_lat").value = lat;
                document.getElementById("user_lon").value = lon;
                document.getElementById("location_button").click();
            },
            (error) => {
                console.log(error);
            }
        );
    </script>
"""

# Render the geolocation script on the page
st.markdown(geolocation_script, unsafe_allow_html=True)

# Create hidden inputs to capture the latitude and longitude from the script
user_lat = st.empty()
user_lon = st.empty()

# Use a button to trigger the location fetch
submit_button = st.button(" ", key="location_button")

# Get the latitude and longitude
user_lat = st.session_state.get("user_lat", "")
user_lon = st.session_state.get("user_lon", "")

# Display the fetched coordinates
if submit_button and user_lat and user_lon:
    try:
        # Convert lat and lon to float and check if within radius
        user_lat = float(user_lat)
        user_lon = float(user_lon)
        if is_within_radius(user_lat, user_lon, LIBRARY_LATITUDE, LIBRARY_LONGITUDE, ALLOWED_RADIUS):
            st.success("You are within the library. Attendance marked.")
        else:
            st.error("You are not within the library's allowed radius.")
    except ValueError:
        st.error("Invalid coordinates received.")
else:
    st.warning("Fetching location, please allow location access.")
