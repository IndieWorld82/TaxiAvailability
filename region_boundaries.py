import pyodbc
import xml.etree.ElementTree as ET

# Set up the database connection
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=kch-sql-bi-dev;'
                            'Database=TEST_API;'
                            'Trusted_Connection=yes;')


# Define the KML file path
kml_file_path = 'C:/Users/hnting/Downloads/master-plan-2019-subzone-boundary-no-sea/master-plan-2019-subzone-boundary-no-sea-kml.kml'

# Parse the KML file
tree = ET.parse(kml_file_path)
root = tree.getroot()

# Get the namespace
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# Iterate over the Placemark elements in the KML file
placemarks = root.findall('.//kml:Placemark', namespace)
for placemark in placemarks:
    # Get the region attributes
    region_name = placemark.find('.//kml:SimpleData[@name="REGION_N"]', namespace).text
    region_code = placemark.find('.//kml:SimpleData[@name="REGION_C"]', namespace).text
    subzone_no = placemark.find('.//kml:SimpleData[@name="SUBZONE_NO"]', namespace).text
    subzone_name = placemark.find('.//kml:SimpleData[@name="SUBZONE_N"]', namespace).text
    subzone_code = placemark.find('.//kml:SimpleData[@name="SUBZONE_C"]', namespace).text
    area_name = placemark.find('.//kml:SimpleData[@name="PLN_AREA_N"]', namespace).text
    area_code = placemark.find('.//kml:SimpleData[@name="PLN_AREA_C"]', namespace).text
    inc_crc = placemark.find('.//kml:SimpleData[@name="INC_CRC"]', namespace).text
    fmel_upd_d = placemark.find('.//kml:SimpleData[@name="FMEL_UPD_D"]', namespace).text
    
    # Get the region boundary coordinates
    coordinates = placemark.find('.//kml:coordinates', namespace).text.strip().split()

    # Create a polygon geometry from the coordinates
    wkt_polygon = 'POLYGON (('
    for coordinate in coordinates:
        lng, lat, _ = coordinate.split(',')
        wkt_polygon += f'{lng} {lat}, '
    wkt_polygon = wkt_polygon[:-2] + '))'

    # Insert the region data into the MSSQL table
    cursor = connection.cursor()
    insert_query = f"INSERT INTO RegionBoundaries (RegionName, RegionCode, Geometry, SubZoneNo, SubZoneName, SubZoneCode, AreaName, AreaCode, INC_CRC, FMEL_UPD_D) " \
                   f"VALUES (?, ?, geometry::STGeomFromText(?, 4326), ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(insert_query, (region_name, region_code, wkt_polygon, subzone_no, subzone_name, subzone_code, area_name, area_code, inc_crc, fmel_upd_d))
    cursor.commit()

# Close the database connection
connection.close()
