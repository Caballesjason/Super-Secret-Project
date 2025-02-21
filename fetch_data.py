import requests
import pandas as pd
from time import sleep

def fetch_data():
    """fetch_data grabs the data from the parking summons API for the year 2024
    
    Args:
        None

    Returns:
        The data from the parking summons API in the form of a pandas dataframe

    """

    # Define the base url
    url = "https://data.buffalony.gov/resource/yvvn-sykd.json"

    # create an empty list to pass the raw json data into
    data = []
    
    # Start at index zero, iterate by every 10000th index to retrive 10000 rows in each api request
    for i in range(0, 160000, 10000):
        
        # define api parameters
        params = {
        "$where": "summdt between '2024-01-01T00:00:00' and '2024-12-31T23:59:59'",
        "$limit": 10000, 
        "$offset": i
        }
    
        # make api request
        response = requests.get(url, params=params)

        # If the status code is 200, grab the json and add it to the data list, else return the status code
        if response.status_code == 200:
            data += response.json()
            sleep(1)
        else:
            print(response.status_code)
            break

    # covert the data list into a dataframe
    df = pd.DataFrame(data)
    
    # Convert the 'summdt' column to datetime
    df['summdt'] = pd.to_datetime(df['summdt'])

    return df

# error handling has been done if status code is not 200.