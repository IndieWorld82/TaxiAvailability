import requests
import datetime
import time
from dateutil import parser
import pyodbc
from pyodbc import Binary
from shapely.geometry import Point


# Establish database connection
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=kch-sql-bi-dev;'
                            'Database=TEST_API;'
                            'Trusted_Connection=yes;')

# Create a cursor object
cursor = connection.cursor()

while True:
    # Define parameters to pass to Taxi Availability API
    today = datetime.datetime.today()
    params = {"date": today.strftime("%Y-%m-%d")}  # YYYY-MM-DD

    # HTTP get request to the URL with parameter defined
    taxi = requests.get('https://api.data.gov.sg/v1/transport/taxi-availability', params=params).json()

    # Extract information from API
    taxi_count = taxi['features'][0]['properties']['taxi_count']
    coordinates = taxi['features'][0]['geometry']['coordinates']
    timestamp = taxi['features'][0]['properties']['timestamp']
    parsed_timestamp = parser.isoparse(timestamp)
    timestamp_str = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # For all coordinates queried, check for the regionID based on RegionBoundaries defined in MSSQL table
    for coord in coordinates:
        longitude = coord[0]
        latitude = coord[1]

        point = Point(longitude, latitude)
        
        # Check which region taxi is located
        sql_check_region = "SELECT ID FROM RegionBoundaries WHERE Geometry.STContains(geometry::STGeomFromText(?, 4326)) = 1"
        cursor.execute(sql_check_region, point.wkt)

        row = cursor.fetchone()

        # if no region ID fetched, default to region_id = 1 and set region_detected_flag = 0 to differentiate records
        if row is None:
            region_id = 1
            region_detected_flag = 0
        else:
            region_id = row.ID
            region_detected_flag = 1
                     
        
        # Prepare the SQL query with a parameter for the Location column
        sql_insert = f"INSERT INTO TaxiAvailability (Timestamp, Location, TaxiCount, RegionID, RegionDetectedFlag) VALUES (?, geometry::STGeomFromText(?, 4326), ?, ?, ?)"
        
        # Execute SQL query with parameters
        cursor.execute(sql_insert, (timestamp_str, point.wkt, taxi_count, region_id, region_detected_flag))
        
        connection.commit()
    
    # API is called every 15 minutes
    time.sleep(900)