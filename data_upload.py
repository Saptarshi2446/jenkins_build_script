#
# FIRST PART OF THE SCRIPT ::  CREATE THE CSV FILES OF THE DATA 
# 
import csv
import psycopg2
from psycopg2 import sql
import time
from datetime import datetime, timedelta

# Set the database connection details
conn = psycopg2.connect(
    host='18.222.253.244',
    port='5432',
    dbname='zabbix_db1',
    user='zabbixuser',
    password='zabbixpass'
)

# Define the time range
end_time = int(time.time())
start_time = end_time - 24 * 60 * 60

# Define the headers for the CSV file
headers = ['ItemID', 'Clock', 'Value', 'Date', 'HostName', 'HostGroupName', 'NS', 'ItemName', 'Time', 'Month']

# Define the SQL query
query = sql.SQL("""
SELECT 
    COALESCE(h.value::text, l.value::text, s.value::text, t.value::text, u.value::text) AS value,
    COALESCE(h.clock, l.clock, s.clock, t.clock, u.clock) AS clock,
    COALESCE(h.ns, l.ns, s.ns, t.ns, u.ns) AS ns,
    i.itemid as item_id, i.name AS item_name,
    ho.name AS host_name,
    g.name AS hostgroup_name
FROM items i
JOIN hosts ho ON ho.hostid = i.hostid
JOIN hosts_groups hg ON hg.hostid = ho.hostid
JOIN hstgrp g ON hg.groupid = g.groupid
LEFT JOIN history h ON h.itemid = i.itemid AND h.clock >= %s
LEFT JOIN history_log l ON l.itemid = i.itemid AND l.clock >= %s
LEFT JOIN history_str s ON s.itemid = i.itemid AND s.clock >= %s
LEFT JOIN history_text t ON t.itemid = i.itemid AND t.clock >= %s
LEFT JOIN history_uint u ON u.itemid = i.itemid AND u.clock >= %s
""")

# Execute the query and retrieve the data
cursor = conn.cursor()
cursor.execute(query, (start_time, start_time, start_time, start_time, start_time,))
data = cursor.fetchall()



# Create a dictionary to store the data by date
data_dict = {}

# Loop through the data and add it to the dictionary
for row in data:
    item_id = row[0]
    clock = row[1]
    value = row[2]
    item_name = row[3]
    ns = row[4]
    host_name = row[5]
    hostgroup_name = row[6]
    if clock is not None:
     date = datetime.fromtimestamp(clock).strftime('%d-%m-%Y')
     time_val = datetime.fromtimestamp(clock).strftime('%H:%M:%S')
     month = datetime.fromtimestamp(clock).strftime('%b-%Y')
    else:
     date = None
     time_val = None
     month = None

    if month not in data_dict:
        data_dict[month] = {}
    if date not in data_dict[month]:
        data_dict[month][date] = []
    data_dict[month][date].append({'ItemID': item_name, 'Clock': clock, 'Value': item_id, 'ItemName': ns, 'NS': value, 'HostName': host_name, 'HostGroupName': hostgroup_name, 'Date': date, 'Time': time_val, 'Month':month})

# Write the data to CSV files, one for each date
for month, dates in data_dict.items():
    for date, rows in dates.items():
        filename = f'{month}_{date}.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

# Close the database connection
cursor.close()
conn.close()


#
# SECOND PART ::  MOVING TO FOLDERS BASED ON MONTHS
#
import os
import string
import shutil

# Define the path where the CSV files are located
csv_path = "C:\\Old laptop Copy\\Copy\\datateam\\Test\\New_folder\\History"

# Define the path where the new folders will be created
new_folder_path = "C:\\Old laptop Copy\\Copy\\datateam\\Test\\New_folder\\History\\Testing"

# Loop through all files in the CSV directory
for file_name in os.listdir(csv_path):
    # Check if the file is a CSV file
    if file_name.endswith(".csv"):
        # Get the alphabetic characters in the file name
        alphabetic_chars = "".join(filter(lambda c: c in string.ascii_letters, file_name))

        # Create a new folder with the alphabetic characters in the file name
        new_folder_name = os.path.join(new_folder_path, alphabetic_chars)
        os.makedirs(new_folder_name, exist_ok=True)

        # Move the CSV file to the new folder
        old_file_path = os.path.join(csv_path, file_name)
        new_file_path = os.path.join(new_folder_name, file_name)
        shutil.move(old_file_path, new_file_path)
