# Exploring NYC Neighborhoods: Crime Rates and Home Values in NYC

## Overview
The **Exploring NYC Neighborhoods** is an interactive web application designed to help users explore and compare NYC neighborhoods based on ZIP codes. This project allows users to:
- Analyze **crime rates** and **home values**.
- Visualize data through dynamic, interactive maps.
- Compare multiple neighborhoods using an intuitive interface.

This application leverages Python for both backend processing and frontend visualization.

## Features
- Interactive folium maps with custom markers.
- Easy-to-use ZIP code search functionality.


    
    

## **Setup Instructions**

 **1. Clone the Repository**
```bash
git clone https://github.com/b-mozz/zip-code-explorer.git
cd zip-code-explorer
```
**2. Install Dependencies:**
Ensure you have Python 3.8+ installed, then install the required libraries:
```bash
pip install -r requirements.txt
```
**3. Test Locally:**
Run the test.py file to validate the data processing logic:
```bash
python src/test.py
```
**4. Test Locally:**
Launch the app with:
```bash
streamlit run src/app.py
```
The app will open in your default browser at http://localhost:8501, or you can use the direct [***link***](https://zip-code-explorer-nyc.streamlit.app/) to access and test the web app

## Technologies Used
### Programming Languages
- **Python:**  Core language for processing data and building the application.
### Libraries and Frameworks
- **Pandas:** For data cleaning and manipulation.
- **folium:** For generating interactive maps.
- **scikit-learn:**  For geospatial data mapping.
- **streamlit:**  For web app development.
- **streamlit-folium:** For integrating maps into the Streamlit app.

### Deployment
- **Streamlit Cloud:**  Hosting the live app for public access.
- **GitHub:**  Repository management and version control.

## Crime Data
- Data has been taken from NYC OpenData. This dataset includes all the arrest in 2024.
- [Here is the link to the dataset](https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc/about_data)



## Live Demo
[***Explore the Web App Here***](https://zip-code-explorer-nyc.streamlit.app/)

## Repository
[***GitHub Repository***](https://github.com/b-mozz/zip-code-explorer)
