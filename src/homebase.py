# This script contains all the functions required for running the application
import folium
import pandas as pd
from sklearn.neighbors import NearestNeighbors


#reads a csv file
def read_csv_file(file_path, skiprows=None, nrows=None, column_names=None):
    """
    Reads a CSV file and returns a pandas DataFrame.
    """
    # Convert column_names to a list, if provided
    if column_names is not None:
        column_names = list(column_names)
        return pd.read_csv(file_path, skiprows=skiprows, nrows=nrows, names=column_names)
    else:
        return pd.read_csv(file_path, skiprows=skiprows, nrows=nrows)



def merge_datasets_by_coordinates(df1, df2, lat1_col, lon1_col, lat2_col, lon2_col, key_col="zip"): #used generative ai for some parts of this function
    
    # This function serves as the foundation of the entire project.
    # The arrest data contains various locations specified by latitude and longitude.
    # This function maps these locations to their corresponding ZIP codes using the sklearn.neighbors library.

    # Extract coordinates
    coords1 = df1[[lat1_col, lon1_col]].to_numpy()
    coords2 = df2[[lat2_col, lon2_col]].to_numpy()

    # Fit Nearest Neighbors
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(coords2)
    distances, indices = nbrs.kneighbors(coords1)

    # Add the matching key column to df1
    df1[key_col] = df2.iloc[indices.flatten()][key_col].values

    # Merge on the key column
    merged_df = pd.merge(df1, df2, on=key_col, how="left")
    return merged_df

#this function merges two different datasets
def merge_datasets(df1, df2):
    merged_data = pd.merge(df1, df2, on="zip")
    return merged_data

#this function counts the number of crimes committed in a specific ZIP CODE
def crimeCounts(df, zip_code):
    info = df[df['zip']==zip_code]
    return len(info)

def crimeRates(df, zip_code):
    count = crimeCounts(df, zip_code)
    row = df[df['zip']==zip_code]

    population = row['population'].values[0]

    return count/population*1000


#returns the average home price in a given ZIP code
def average_home_value(df, zip_code=None):

    
    if zip_code:
        # Filter DataFrame for the specified ZIP code
        dfForHomevalue = df[df['zip'] == zip_code]
        if dfForHomevalue.empty:
            print(f"No data found for ZIP code {zip_code}.")
            return None
        avg_value = dfForHomevalue['home_value'].mean()

    return avg_value


def lookup_zip_codes(df):
    # Initialize an empty list to store ZIP code data
    zip_data = []

    i = 1

    while i > 0:
        # Prompt the user for a ZIP code
        zip_code = input("Enter a ZIP code (or type 'exit' to quit): ")
        
        if zip_code.lower() == "exit":
            print("Goodbye!")
            break

        else:
        
            if zip_code.isdigit():  # Check if the input is numeric
                zip_code = int(zip_code)  # Convert to an integer
                
            else:
                print("Invalid ZIP code.")




        # Filter the row(s) for the given ZIP code
        row = df[df['zip'] == zip_code]
        
        if row.empty:
            print(f"No data found for ZIP code {zip_code}. Please enter a valid Zip code.")
    

        # Extract crime data
        else:
            count = crimeCounts(df, zip_code)
            rate = crimeRates(df, zip_code)
            value = average_home_value(df, zip_code)

            # Extract latitude and longitude (assuming consistent lat/lng across rows)
            lat = row['lat'].iloc[0]
            lng = row['lng'].iloc[0]
            

            # Save the data for later use
            zip_data.append({
                "zip_code": zip_code,
                "num_crimes": count,
                "crime_rate": rate,
                "lat": lat,
                "lng": lng,
                "home_value": value 
            })

    # Return the stored data for later use
    return zip_data


#generates a map if the code is run locally
def generateMap(df):
    # Create a base map centered around NYC
    mapNYC = folium.Map(location=[40.75, -74.125], zoom_start=10)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract necessary data from the row
        lat = row['lat']
        lng = row['lng']
        zip_code = row['zip_code']
        crime_rate = row['crime_rate']
        avg_home_value = row['home_value']

        # Add a marker to the map
        newMarker = folium.Marker(
            location=[lat, lng],
            tooltip=f"ZIP: {zip_code}<br><br>Crime Rate: {crime_rate:.2f} per 1000<br><br>Average Home Price: ${avg_home_value}"
        )
        newMarker.add_to(mapNYC)

    # Return the map object for display or saving
    return mapNYC





