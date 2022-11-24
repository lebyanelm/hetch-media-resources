import sys
import subprocess
import random_utilities
import os

media_resources, IS_CONNECTED = random_utilities.initiate_mongodb_connection(
    mongo_host=os.environ["MONGODB_HOST"],
    database_name=os.environ["DATABASE_NAME"],
    collection_name="media_resources"
)

"""
For safety of the files stored, and users
recieving shared links, scan files uploaded
for viruses.
"""

# Some change

random_utilities.log(f""" File selected for scanning {sys.argv[1]}""")
SELECTED_SCAN_FILE = sys.argv[1]

random_utilities.log(""" Have the file scanned with clamav """)
random_utilities.log(""" Only scan files while in production environment """)

completed_process = subprocess.run(["clamscan", SELECTED_SCAN_FILE], capture_output=True, text=True)
stdout, stderr = completed_process.stdout, completed_process.stderr
if stderr == "":
    is_file_safe = False
    if "Infected files: 0" in stdout and "Scanned files: 1" in stdout:
        is_file_safe = True
    file_in_db = media_resources.find_one({ "filename": SELECTED_SCAN_FILE.split("/")[-1].split(".")[0] })
    if file_in_db:
        file_in_db["is_virus_safe"] = is_file_safe
        file_in_db["scan_results"] = stdout
        media_resources.update_one({"filename": file_in_db["filename"]}, {"$set": { **file_in_db }})
else:
    random_utilities.log(stderr)