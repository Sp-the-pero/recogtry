import streamlit as st

# Coordinates for the library (replace with actual values)
LIBRARY_LATITUDE = 24.8640337
LIBRARY_LONGITUDE = 67.0157538
ALLOWED_RADIUS = 50  # meters

def is_within_radius(user_lat, user_lon, lib_lat, lib_lon, radius):
  from geopy.distance import geodesic
  user_location = (user_lat, user_lon)
  lib_location = (lib_lat, lib_lon)
  distance = geodesic(user_location, lib_location).meters
  return distance <= radius

st.subheader("Mark Attendance")

# Use JavaScript to fetch user location through Geolocation API
geolocation_script = """
    <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById("user_lat").value = lat;
                document.getElementById("user_lon").value = lon;
            },
            (error) => {
                console.log(error);
            }
        );
    </script>
"""

# Render the geolocation script on the page
st.markdown(geolocation_script, unsafe_allow_html=True)

# Display hidden inputs to store the latitude and longitude from JS
user_lat = st.text_input("Latitude", "", key="user_lat")
user_lon = st.text_input("Longitude", "", key="user_lon")

# Button to mark attendance
if st.button("Mark Attendance"):
  if user_lat and user_lon:
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
    st.error("Could not retrieve your location. Please allow location access.")
