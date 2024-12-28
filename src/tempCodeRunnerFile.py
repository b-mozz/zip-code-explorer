    income_data = read_csv_file(
        "data/uszips.csv",
        skiprows=2583,
        nrows=1825,
        column_names=pd.read_csv("data/uszips.csv", nrows=1).columns
    )
    crime_data = read_csv_file("data/arrestData.csv")
    home_value = read_csv_file("data/average_value.csv")