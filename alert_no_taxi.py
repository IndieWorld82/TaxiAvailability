import pyodbc
from telegram import Bot

# Establish database connection
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=kch-sql-bi-dev;'
                            'Database=TEST_API;'
                            'Trusted_Connection=yes;')


# Create a cursor object
cursor = connection.cursor()

# Write the SQL query to retrieve sub zone names with no taxi availabilities
query = """
    SELECT R.SubZoneName FROM RegionBoundaries R LEFT JOIN TaxiAvailability T ON R.ID = T.RegionID
    WHERE T.RegionID IS NULL AND T.Timestamp = (SELECT MAX(Timestamp) FROM TaxiAvailability)
    """

cursor.execute(query)
results = cursor.fetchall()

returnflag = 0

# Create a message string and format it with the query results
message = 'These sub zones currently do not have any taxis available:\n\n'
for row in results:
    if row[0] != "":
        returnflag = 1
        message += f'{row[0]}\n'
    else:
        returnflag = 0

if returnflag == 1:    
    # Telegram bot API token
    bot_token = 'YOUR_BOT_TOKEN'

    # Chat ID of the destination (can be a user or group chat)
    chat_id = 'YOUR_CHAT_ID'

    # Message to send
    message = 'Alert: No taxis available in certain areas.\nThe following areas have no taxis: area1, area2, area3'

    # Create a bot instance
    bot = Bot(token=bot_token)

    # Send the message
    bot.send_message(chat_id=chat_id, text=message)