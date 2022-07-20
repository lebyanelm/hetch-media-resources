import sys
import subprocess
from hetch_utilities import log
import os
import mongodb_connection

dbconn, IS_CONNECTED = mongodb_connection.initiate_mongodb_connection()

"""
For safety of the files stored, and users
recieving shared links, scan files uploaded
for viruses.
"""

log(f""" File selected for scanning {sys.argv[1]}""")
SELECTED_SCAN_FILE = sys.argv[1]

log(""" Have the file scanned with clamav """)
log(""" Only scan files while in production environment """)
if os.environ.get("ENVIRONMENT") != "production":
    completed_process = subprocess.run(["clamscan", SELECTED_SCAN_FILE], capture_output=True, text=True)
    stdout, stderr = completed_process.stdout, completed_process.stderr
    if stderr == "":
        is_file_safe = False
        if "Infected files: 1" in stdout and "Scanned files: 1" in stdout:
            is_file_safe = True
        file_in_db = dbconn.find_one({ "filename": SELECTED_SCAN_FILE.split("/")[-1].split(".")[0] })
        if file_in_db:
            file_in_db["is_virus_safe"] = is_file_safe
            dbconn.update_one({"filename": file_in_db["filename"]}, {"$set": { **file_in_db }})
    else:
        log(stderr)