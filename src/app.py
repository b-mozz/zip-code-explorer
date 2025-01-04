import streamlit as st
from dataframe import df
import pandas as pd
import folium
from homebase import crimeCounts, crimeRates, average_home_value
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import numpy as np


st.title("ZIP Code Explorer: Crime Rates and Home Values in NYC")

st.markdown("""
<div style="
    font-size:19px; 
    font-weight:bold; 
    color:#c24b4b; 
    border: 2px solid #c24b4b; 
    padding: 15px; 
    border-radius: 5px; 
    background-color: #ffeaea;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);">
If you're planning to move to a new neighborhood or simply curious about your current one, just provide us with the ZIP codes (as many as you like), and we'll take care of the rest!
</div>
""", unsafe_allow_html=True)

st.write(" ")


if "zip_data" not in st.session_state:
    st.session_state.zip_data = []

# Form for input
with st.form("zip_input_form"):
    zip_code = st.text_input("Enter a ZIP code (Type 'exit' to stop):", key="zip_input")
    submit = st.form_submit_button("Add ZIP Code")


if submit:
    if zip_code.lower() == "exit":
        st.write("Goodbye!")
    elif not zip_code.isdigit():
        st.write("Invalid ZIP code. Please enter a numeric value.")
    else:
        zip_code = int(zip_code)
        row = df[df["zip"] == zip_code]

        if row.empty:
            st.write(f"No data found for ZIP code {zip_code}.")
        else:
            count = crimeCounts(df, zip_code)
            rate = crimeRates(df, zip_code)
            value = average_home_value(df, zip_code)
            lat = row["lat"].iloc[0]
            lon = row["lng"].iloc[0]

            
            st.session_state.zip_data.append({
                "zip_code": zip_code,
                "num_crimes": count,
                "crime_rate/1000": rate,
                "lat": lat,
                "lon": lon,
                "home_price": value,
            })
            st.write(f"ZIP code {zip_code} added!")
            st.write("Enter another ZIP code or type exit.")

# Create a DataFrame from session state
mapData = pd.DataFrame(st.session_state.zip_data)
st.table(mapData)

# Create a map once ZIP codes are collected
if not mapData.empty:
    st.write("Map and bar charts have been generated below...")
    st.write(' ')
    mapNYC = folium.Map(location=[40.75, -74.125], zoom_start=10)

    for _, row in mapData.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        zip_code = row["zip_code"]
        crime_rate = row["crime_rate/1000"]
        avg_home_value = row["home_price"]

        folium.Marker(
            location=[lat, lon],
            tooltip=f"ZIP: {zip_code}<br><br>Crime Rate: {crime_rate:.2f} per 1000<br><br>Average Home Price: ${avg_home_value}"
        ).add_to(mapNYC)

    
    folium_static(mapNYC, width=700, height=500)

    st.write("Crime and Home Value Metrics by ZIP Code")
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = mapData["zip_code"].astype(str)
    x = np.arange(len(labels))
    width = 0.25
    multiplier = 0
    bar_colors = ["#FF9999", "#99CCFF", "#99FF99"]

    metrics = {
        "Number of Crimes": mapData["num_crimes"],
        "Crime Rate (per 1000)": mapData["crime_rate/1000"],
        "Average Home Price (in $1000)": mapData["home_price"] / 1000
    }

    for idx, (metric, values) in enumerate(metrics.items()):
        offset = width * multiplier
        rects = ax.bar(x + offset, values, width, label=metric, color=bar_colors[idx])
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_xlabel("ZIP Code")
    ax.set_ylabel("Values")
    ax.set_title("Crime Statistics and Home Prices")
    ax.set_xticks(x + width, labels)
    ax.legend(loc="best")
    st.pyplot(fig)

    


    
    







