from homebase import read_csv_file, merge_datasets_by_coordinates, merge_datasets, crimeCounts,crimeRates, lookup_zip_codes, generateMap
import pandas as pd


# Load datasets
income_data = read_csv_file(
    "data/uszips.csv",  # Updated path
    skiprows=2583,
    nrows=1825,
    column_names=pd.read_csv("data/uszips.csv", nrows=1).columns  
)
crime_data = read_csv_file("data/arrestData.csv")  
home_value = read_csv_file("data/average_value.csv")  

# Merge datasets
merge_zip = merge_datasets_by_coordinates(
    df1=crime_data,
    df2=income_data,
    lat1_col="Latitude",
    lon1_col="Longitude",
    lat2_col="lat",
    lon2_col="lng",
    key_col="zip"
)
df = merge_datasets(home_value, merge_zip)

