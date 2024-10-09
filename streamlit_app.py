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

# JavaScript to fetch user location through Geolocation API
geolocation_script = """
    <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById("user_lat").innerText = lat;
                document.getElementById("user_lon").innerText = lon;
                // Simulate click on the submit button
                document.getElementById("mark_attendance").click();
            },
            (error) => {
                alert("Could not fetch location. Please allow location access in your browser settings.");
            }
        );
    </script>
"""

# Inject the geolocation script
st.markdown(geolocation_script, unsafe_allow_html=True)

# Create hidden elements to store latitude and longitude
st.markdown('<div id="user_lat" style="display:none;"></div>', unsafe_allow_html=True)
st.markdown('<div id="user_lon" style="display:none;"></div>', unsafe_allow_html=True)

# Button to mark attendance
if st.button("Mark Attendance", key="mark_attendance"):
    # Get latitude and longitude from hidden elements
    user_lat = st.session_state.get("user_lat", None)
    user_lon = st.session_state.get("user_lon", None)

    if user_lat is not None and user_lon is not None:
        user_lat = float(st.session_state.user_lat)
        user_lon = float(st.session_state.user_lon)
        
        if is_within_radius(user_lat, user_lon, LIBRARY_LATITUDE, LIBRARY_LONGITUDE, ALLOWED_RADIUS):
            st.success("You are within the library. Attendance marked.")
        else:
            st.error("You are not within the library's allowed radius.")
    else:
        st.warning("Could not retrieve your location. Please allow location access.")
