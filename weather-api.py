import streamlit as st
import requests as rq

st.title("Live Temperature")    

response = rq.get("https://api.open-meteo.com/v1/forecast", params={"latitude": 28.6692, "longitude": 77.4538, "current": "temperature_2m"})
# coords of GZB

@st.fragment(run_every="3s")
def show():
    st.metric("Temperature in degree Centigrade", f"{response.json()['current']['temperature_2m']} °C")


if response.status_code == 200:
    show()
else:
    st.error(f"Failed to request! {response.status_code}")
    st.write(response.text)