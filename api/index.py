import pandas as pd
import requests
import time
from pymongo import MongoClient, UpdateOne
import traceback

try:
  # Start the timer
  start_time = time.time()
  
  # Connect to your MongoDB database
  client = MongoClient('mongodb+srv://connerhoy:YiXItLVEwnSJ7TIB@buoy-data.xwg0qpk.mongodb.net/')  
  db = client['Buoy-Data']  
  collection = db['Buoys']
  
  # Request the data
  response = requests.get('https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt')
  
  # Split the text data by new lines to get each row
  data = response.text.split('\n')
  
  # The first row is the header row, so we separate that
  headers = data[0].split()
  
  # The rest of the data is the actual buoy data
  buoy_data = [row.split() for row in data[1:]]
  
  # Use pandas to create a DataFrame
  df = pd.DataFrame(buoy_data, columns=headers)
  
  # Convert the DataFrame to a list of dict records
  records = df.to_dict('records')
  
  # Prepare bulk operations
  operations = [UpdateOne({"#STN": record["#STN"]}, {"$set": record}, upsert=True) for record in records]
  
  # Perform bulk operations
  collection.bulk_write(operations)
  
  # End the timer and print the time taken
  end_time = time.time()
  print("Time taken: {:.6f}s".format(end_time - start_time))
   
except Exception as e:
    print("An error occurred:")
    print(traceback.format_exc())


