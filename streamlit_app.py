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

# JavaScript code to fetch user location through Geolocation API
geolocation_script = """
    <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                console.log("Location fetched:", lat, lon);
                document.getElementById("user_lat").value = lat;
                document.getElementById("user_lon").value = lon;
                document.getElementById("location_button").click();
            },
            (error) => {
                console.error("Error fetching location:", error);
                alert("Could not fetch location. Ensure location access is enabled in your browser.");
            },
            {timeout: 10000}
        );
    </script>
"""

# Render the geolocation script
st.markdown(geolocation_script, unsafe_allow_html=True)

# Hidden button to trigger attendance marking
user_lat = st.text_input("Latitude", "", key="user_lat")
user_lon = st.text_input("Longitude", "", key="user_lon")
submit_button = st.button("Mark Attendance", key="location_button", help="Click this only after location is fetched.")

# Check if the user is within the allowed radius
if submit_button:
  if user_lat and user_lon:
    try:
      user_lat = float(user_lat)
      user_lon = float(user_lon)
      if is_within_radius(user_lat, user_lon, LIBRARY_LATITUDE, LIBRARY_LONGITUDE, ALLOWED_RADIUS):
        st.success("You are within the library. Attendance marked.")
      else:
        st.error("You are not within the library's allowed radius.")
    except ValueError:
      st.error("Could not process your location. Invalid latitude or longitude values.")
  else:
    st.warning("Could not retrieve your location. Please allow location access.")
