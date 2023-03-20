#
# PART THREE ::  UPLOAD TO INFLUX
import os
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import glob

# InfluxDB connection details
client = InfluxDBClient(url="http://13.229.128.150:8086", token="BMZHFuL-71SF8s3CFrRHAeszar92OYwxx_BhmQ5ue4Y7NS5oH0sDCP2Vol-iz9pkijt4nSf_eEDxfov1hzAZaA==")
bucket = "Streamli1"

# Write API instance
write_api = client.write_api(write_options=SYNCHRONOUS)

# Parent directory containing subdirectories with CSV files
csv_dir = "/var/lib/jenkins/workspace/Database_data"

# Find all subdirectories in the parent directory
subdirs = [entry for entry in os.scandir(csv_dir) if entry.is_dir()]

# Loop through each subdirectory
for subdir in subdirs:
    print(f"Processing folder: {subdir.name}")
    
    # Find all CSV files in the subdirectory
    csv_files = glob.glob(f"{subdir.path}/*.csv")

    # Loop through each CSV file in the subdirectory
    for csv_file in csv_files:
        # Read CSV file into a pandas dataframe
        df = pd.read_csv(csv_file, low_memory=False)


        # Extract item name from file name (without .csv extension)
        item_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Loop through each row in the dataframe
        for row_index, row in df.iterrows():
            field_value = row[2]
            json_body = [
                { 
                    "measurement": subdir.name,
                    "tags": {
                        "Date": row[3],
                        "Time": row[8],
                        "Hostname": row[4],
                        "Itemname": row[7],
                        "Host_Group": row[5],
                    },
                    "fields": {
                        "value": field_value,
                    }
                } 
            ]
            print(json_body)
            write_api.write(bucket=bucket, org="dadee4434fd794ea", record=json_body)
