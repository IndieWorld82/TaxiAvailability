import pyodbc
import matplotlib.pyplot as plt
import streamlit as st

# Establish database connection
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=kch-sql-bi-dev;'
                            'Database=TEST_API;'
                            'Trusted_Connection=yes;')

# Write the SQL query to retrieve the top 10 areas of taxi population
query_highest = """
    WITH TAXI_CTE AS
    (SELECT T.Timestamp, R.SubZoneName, R.SubZoneCode, R.AreaName, R.AreaCode, COUNT(*) AS TaxiCount FROM TaxiAvailability T INNER JOIN RegionBoundaries R
    ON T.RegionID = R.ID
    WHERE Timestamp = (SELECT MAX(Timestamp) FROM TaxiAvailability)
    GROUP BY T.Timestamp, R.SubZoneName, R.SubZoneCode, R.AreaName, R.AreaCode)
    SELECT TOP 10 Timestamp, SubZoneName, SubZoneCode, AreaName, AreaCode, TaxiCount FROM TAXI_CTE ORDER BY TAXICOUNT DESC
    """

# Execute the SQL query and fetch the results for highest population areas
cursor = connection.cursor()
cursor.execute(query_highest)
results_highest = cursor.fetchall()

# Extract the data for visualization
Subzone_name_highest = [row.SubZoneName for row in results_highest]
Taxi_count_highest = [row.TaxiCount for row in results_highest]

# Create a figure for the highest areas
fig_highest = plt.figure()
plt.bar(Subzone_name_highest, Taxi_count_highest)
plt.xlabel('Sub Zone Name')
plt.ylabel('Available Taxi Count')
plt.title('Top 10 Areas of Taxi Population')
plt.xticks(rotation=90)
plt.tight_layout()

# Display the bar chart using Streamlit
st.pyplot(fig_highest)

# Write the SQL query to retrieve the lowest 10 areas of taxi population
query_lowest = """
    WITH TAXI_CTE AS
    (SELECT T.Timestamp, R.SubZoneName, R.SubZoneCode, R.AreaName, R.AreaCode, COUNT(*) AS TaxiCount FROM TaxiAvailability T INNER JOIN RegionBoundaries R
    ON T.RegionID = R.ID
    WHERE Timestamp = (SELECT MAX(Timestamp) FROM TaxiAvailability)
    GROUP BY T.Timestamp, R.SubZoneName, R.SubZoneCode, R.AreaName, R.AreaCode)
    SELECT TOP 10 Timestamp, SubZoneName, SubZoneCode, AreaName, AreaCode, TaxiCount FROM TAXI_CTE ORDER BY TAXICOUNT ASC
    """

# Execute the SQL query and fetch the results for lowest population areas
cursor.execute(query_lowest)
results_lowest = cursor.fetchall()

# Extract the data for visualization
Subzone_name_lowest = [row.SubZoneName for row in results_lowest]
Taxi_count_lowest = [row.TaxiCount for row in results_lowest]

# Create a figure for the lowest areas
fig_lowest = plt.figure()
plt.bar(Subzone_name_lowest, Taxi_count_lowest)
plt.xlabel('Sub Zone Name')
plt.ylabel('Available Taxi Count')
plt.title('Lowest 10 Areas of Taxi Population')
plt.xticks(rotation=90)
plt.tight_layout()

# Display the bar chart using Streamlit
st.pyplot(fig_lowest)


# Write the SQL query to display hourly trend of taxi population
query_hourly = """
    WITH taxidata AS
    (SELECT DISTINCT Timestamp, CAST(Timestamp as date) AS Date, datepart(hour, Timestamp) AS [Hour], Taxicount FROM TaxiAvailability)
    SELECT Date, Hour, Avg(Taxicount) AS Taxicount FROM taxidata GROUP BY Date, Hour ORDER BY date, hour
    """

cursor.execute(query_hourly)
results_hourly = cursor.fetchall()

# Extract the data from the results
dates = [row.Date for row in results_hourly]
hours = [row.Hour for row in results_hourly]
taxi_counts = [row.Taxicount for row in results_hourly]

# Combine the date and hour values into a single list for x-axis labels
x_labels = [f"{date} {hour:02d}:00" for date, hour in zip(dates, hours)]

# Create a figure for the lowest areas
fig_hourly = plt.figure()
plt.plot(x_labels, taxi_counts)
plt.xlabel('Date and Hour')
plt.ylabel('Taxi Count')
plt.title('Available Taxi Count by Date and Hour')
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability

# Display the plot using Streamlit
st.pyplot(fig_hourly)
