import os
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import glob


client = InfluxDBClient(url="http://13.250.36.201:8086", token="BMZHFuL-71SF8s3CFrRHAeszar92OYwxx_BhmQ5ue4Y7NS5oH0sDCP2Vol-iz9pkijt4nSf_eEDxfov1hzAZaA==")
bucket = "Streamli1"

write_api = client.write_api(write_options=SYNCHRONOUS)


file_path = r'/var/lib/jenkins/workspace/Database_data2/Mar-2023_15-03-2023.csv'

csvReader = pd.read_csv(file_path)

print(csvReader.shape)
print(csvReader.columns)
for row_index, row in csvReader.iterrows():
    field_value = row[2]
    json_body = [
                { 
                "measurement": "Newcsv",
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
