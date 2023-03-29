import pymysql
import csv
import datetime
# Connect to the database
connection = pymysql.connect(host='18.224.31.169', user='zabbix1', password='password', database='zabbix')
query = """
SELECT DISTINCT problem.objectid, 
                DATE_FORMAT(FROM_UNIXTIME(problem.clock), '%Y-%m-%d %H:%i:%s') AS start_time,
                triggers.description as problem_description,
                r.eventid as r_eventid,
                DATE_FORMAT(FROM_UNIXTIME(IFNULL(r.clock, UNIX_TIMESTAMP())), '%Y-%m-%d %H:%i:%s') AS end_time,
                IFNULL(
                  CONCAT(
                    TIMESTAMPDIFF(HOUR, FROM_UNIXTIME(problem.clock), FROM_UNIXTIME(IFNULL(r.clock, UNIX_TIMESTAMP()))), 'h ',
                    TIMESTAMPDIFF(MINUTE, FROM_UNIXTIME(problem.clock), FROM_UNIXTIME(IFNULL(r.clock, UNIX_TIMESTAMP()))) % 60, 'm ',
                    TIMESTAMPDIFF(SECOND, FROM_UNIXTIME(problem.clock), FROM_UNIXTIME(IFNULL(r.clock, UNIX_TIMESTAMP()))) % 60, 's'
                  ),
                  ''
                ) AS duration,
                hosts.host AS hostname
FROM events problem
JOIN triggers ON triggers.triggerid = problem.objectid
LEFT JOIN events r ON r.objectid = problem.objectid AND r.value = 0 AND r.clock > problem.clock
  AND NOT EXISTS (
    SELECT 1 FROM events r2
    WHERE r2.objectid = r.objectid AND r2.value = 0 AND r2.clock > problem.clock AND r2.clock < r.clock
  )
LEFT JOIN functions f ON triggers.triggerid = f.triggerid
LEFT JOIN items i ON f.itemid = i.itemid
LEFT JOIN hosts ON i.hostid = hosts.hostid
WHERE problem.object = 0 AND problem.clock > UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 DAY)) AND problem.value = 1
  AND (r.eventid IS NOT NULL OR problem.value = 1)
ORDER BY start_time DESC;"""
try:
    with connection.cursor() as cursor:
        # Execute the SQL query
        sql = query
        cursor.execute(sql)

        # Fetch the query results
        results = cursor.fetchall()

        # Define the headers for the CSV file
        headers = ('objectid', 'start_time', 'problem_description', 'r_eventid', 'end_time', 'duration', 'hostname')

        # Open the CSV file for writing and write the headers
        with open('C:\\Old laptop Copy\\Copy\\datateam\\Test\\New_folder\\Reports\\Monthly\\report{date}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            # Write each row of the result set to the CSV file
            for row in results:
                writer.writerow(row)

finally:
    # Close the database connection
    connection.close()