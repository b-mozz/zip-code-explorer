import streamlit as st
from dataframe import df
import pandas as pd
import folium
from homebase import crimeCounts, crimeRates, average_home_value
from streamlit_folium import folium_static

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
If you're planning to move to a new neighborhood or simply curious about your current one, just provide us with the ZIP code, and we'll take care of the rest!
</div>
""", unsafe_allow_html=True)

# Storage for ZIP codes
zip_data = []
zip_codes = []

# Form for input
with st.form("zip_input_form"):
    zip_code = st.text_input("Enter a ZIP code (Type 'exit' to stop):", key="zip_input")
    submit = st.form_submit_button("Add ZIP Code")

# Process input after form submission
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
            lng = row["lng"].iloc[0]

            # Save data
            zip_data.append({
                "zip_code": zip_code,
                "num_crimes": count,
                "crime_rate": rate,
                "lat": lat,
                "lng": lng,
                "home_price": value,
            })
            st.write(f"ZIP code {zip_code} added!")

mapData = pd.DataFrame(zip_data)
st.table(mapData)

# Create a map once ZIP codes are collected
if zip_data:
    st.write("Generating Map...")
    mapNYC = folium.Map(location=[40.75, -74.125], zoom_start=10)

    for _, row in mapData.iterrows():
        lat = row["lat"]
        lng = row["lng"]
        zip_code = row["zip_code"]
        crime_rate = row["crime_rate"]
        avg_home_value = row["home_price"]

        folium.Marker(
            location=[lat, lng],
            tooltip=f"ZIP: {zip_code}<br><br>Crime Rate: {crime_rate:.2f} per 1000<br><br>Average Home Price: ${avg_home_value}"
        ).add_to(mapNYC)

    # Display map
    folium_static(mapNYC, width=700, height=500)




    
    







