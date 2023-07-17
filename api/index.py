from http.server import BaseHTTPRequestHandler
import pandas as pd
import requests
import json
from pymongo import MongoClient


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))

        # Connect to your MongoDB database
        client = MongoClient(
            'mongodb+srv://connerhoy:YiXItLVEwnSJ7TIB@buoy-data.xwg0qpk.mongodb.net/')
        db = client['Buoy-Data']
        collection = db['Buoys']

        # Request the data
        response = requests.get(
            'https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt')

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
        print(records)
        # Save each record to your MongoDB collection
        for record in records:
            collection.update_one(
                {"#STN": record["#STN"]},  # filter
                {"$set": record},  # update
                upsert=True  # if not found, insert new document
            )

        return
