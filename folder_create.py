#
# SECOND PART ::  MOVING TO FOLDERS BASED ON MONTHS
#
import os
import string
import shutil

# Define the path where the CSV files are located
csv_path = "/var/lib/jenkins/workspace/Database_data"

# Define the path where the new folders will be created
new_folder_path = "/var/lib/jenkins/workspace/Database_data"

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
