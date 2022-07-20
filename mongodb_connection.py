import os
import pymongo
import traceback
import sys
from hetch_utilities import log


""" Flag to tell if the DB Connection is active or not. """
database = None
default_collection = None

def initiate_mongodb_connection():
    if os.environ.get("MONGODB_HOST"):
        try:
            log("Connecting to database and testing connection...")
            mongo_client = pymongo.MongoClient(os.environ.get("MONGODB_HOST"),
                server_api=pymongo.server_api.ServerApi("1"))

            database = mongo_client[os.environ["DATABASE_NAME"]]
            collection  = database.media_resources
            default_collection = collection
            document_count = collection.count_documents({ })

            log(f"Database successfully connected with `{document_count}` documents in collection `media_resources`.")

            return default_collection, True
        except:
            log("Opps something went wrong. " + traceback.format_exc())
            sys.exit(1)
    else:
        log("No database connection specified. Not connecting to any.")
        return None, False