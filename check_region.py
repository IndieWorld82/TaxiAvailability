import folium
import pyodbc
from shapely.wkb import loads
from shapely.geometry import mapping, MultiPolygon

# Establish database connection
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=kch-sql-bi-dev;'
                            'Database=TEST_API;'
                            'Trusted_Connection=yes;')

# Create a cursor object
cursor = connection.cursor()

# Retrieve the geometry data from the MSSQL table
sql_query = "SELECT Geometry.STAsBinary() AS WKBGeometry, SubZoneName FROM RegionBoundaries"
cursor.execute(sql_query)
rows = cursor.fetchall()

# Create a Folium map centered in Singapore
sg_map = folium.Map(location=[1.3521, 103.8198], zoom_start=12, tiles="Stamen Terrain")

# Iterate over the rows and add polygons to the map
for row in rows:
    wkb_geometry = row.WKBGeometry
    subzone_name = row.SubZoneName

    # Convert the WKT geometry to Shapely object
    geometry = loads(wkb_geometry)

    geojson_obj = mapping(geometry)
    folium.GeoJson(geojson_obj, name=subzone_name).add_to(sg_map)

# Add layer control to toggle region names visibility
folium.LayerControl().add_to(sg_map)

# Save the map to an HTML file
sg_map.save("regional_map.html")
