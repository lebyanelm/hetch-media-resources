"""
________________________________
HETCH MEDIA RESOURCES 
Handles file uploads and serving media content of the users.
________________________________
"""
import subprocess
import asyncio
from dataclasses import field
import traceback
import flask
import flask_cors
import os
import dotenv
import requests
import nanoid
import random_utilities
from random_utilities.models import ResponseModel

from models.file_upload import FileUploadModel
from allowed_mimetypes import allowed_mimetypes

"""
__________________________________

DEVELOPMENTAL ENVIRONMENT VARIABLES
__________________________________
"""
if os.environ.get("ENVIRONMENT") != "production":
	dotenv.load_dotenv()
else:
	""" Update virus signatures database. """
	os.system("freshclam")


"""
__________________________________
SERVER INSTANCE SETUP
__________________________________
"""
server_instance = flask.Flask(__name__,
			static_folder="./assets/",
            static_url_path="/server_name/assets/")
flask_cors.CORS(server_instance, resources={r"*": {"origins": "*"}})


"""
__________________________________
DATABASE CONNECTION
__________________________________
"""
media_resources, IS_DB_CONNECTED = random_utilities.initiate_mongodb_connection(
	mongo_host=os.environ["MONGODB_HOST"],
	database_name=os.environ["DATABASE_NAME"],
	collection_name="media_resources"
)


""" Location in which media resource files will be saved. """
DEFAULT_UPLOAD_PATH = "/media-resources" if os.environ.get("ENVIRONMENT") == "production" else "./uploads"

"""
__________________________________
SERVER INSTANCE ROUTES
__________________________________
"""
# Returns status of the server
@server_instance.route("/media-resources/status", methods=["GET"])
@flask_cors.cross_origin()
def status():
	try:
		IS_STORAGE_MOUNT = os.path.exists(DEFAULT_UPLOAD_PATH)
		return ResponseModel(
				cd=200 if all([IS_DB_CONNECTED, IS_STORAGE_MOUNT]) else 500,
				msg="Running" if all([IS_DB_CONNECTED, IS_STORAGE_MOUNT]) else "Something went wrong.",
				d={
					"Database Connection": IS_DB_CONNECTED,
					"File Storage Mount": IS_STORAGE_MOUNT
				}).to_json()
	except:
		random_utilities.log(traceback.format_exc())
		return ResponseModel(
			cd=500,
			msg="Something went wrong while getting status.").to_json()


# Uploading a file
@server_instance.route("/media-resources/upload", methods=["POST"])
@flask_cors.cross_origin()
def upload_a_file():
	try:
		# Request an authorization of the user creating the upload
		auth_response = requests.get("/".join([ os.environ["ACCOUNTS_ENDPOINT"], "authentication/re" ]),
								headers={ "Authorization": flask.request.headers.get("Authorization") })

		if auth_response.status_code == 200:
			selected_file = flask.request.files["file"]
			print(selected_file)
			uploader_id = auth_response.json().get("data").get("p+d").get("email_address")
			rand_filename = nanoid.generate()
			filename = ".".join([rand_filename, selected_file.filename.split(".")[-1]])
			today_folder = random_utilities.models.TimeCreatedModel().formatted_date.replace(" ", "_").replace(",", "")
			
			""" Check if the upload folder path exists. """
			upload_path = os.path.join(DEFAULT_UPLOAD_PATH, today_folder)
			if os.path.exists(upload_path) == False: os.mkdir(upload_path)

			""" Save the file to storage """
			upload_path = os.path.join(upload_path, filename)
			selected_file.save(upload_path)

			""" Given the file is below max file size save the file upload to the database"""
			if selected_file.mimetype in allowed_mimetypes:
				maximum_allowed_upload_size = 2e+8 # In B, 200MB equivalent
				file_upload_size = os.stat(upload_path).st_size
				if file_upload_size <= maximum_allowed_upload_size:
					upload_db_entry = FileUploadModel(dict(
						original_name = selected_file.filename.replace(" ", "_"),
						file_extension = selected_file.filename.split(".")[-1],
						filename = rand_filename,
						uploader_id = uploader_id,
						file_path = upload_path,
						file_size = (file_upload_size / (1e+6)),
						alternate_name = flask.request.form.get("alternate_name", None),
						credits_name = flask.request.form.get("credits_name", None),
						url_link = os.path.join(os.environ.get("SELF_ENDPOINT"), "attachments", rand_filename, selected_file.filename.replace(" ", "_")),
						mime_type = selected_file.mimetype
					))
					
					media_resources.insert_one(upload_db_entry.__dict__)
					upload_db_entry._id = str(upload_db_entry._id)
					
					async def scan_uploaded_file():
						subprocess.Popen(["python", "scan_uploaded_file.py", upload_path])
					asyncio.run(scan_uploaded_file())
					
					return ResponseModel(cd=200, d=upload_db_entry.__dict__).to_json()
				else:
					return ResponseModel(cd=400, msg="Selected file above maximum limit of 200MB.").to_json()
			else:
				return ResponseModel(cd=400, msg="Selected file not allowed for upload please try another file type.").to_json()
		else:
			return ResponseModel(cd=auth_response.status_code, d=auth_response.json()).to_json()
	except:
		random_utilities.log(traceback.format_exc())
		return ResponseModel(cd=500, msg="Something went wrong.").to_json()


# Getting an uploaded file
@server_instance.route("/media-resources/attachments/<file_id>/<original_filename>", methods=["GET"])
def get_uploaded_file(file_id, original_filename):
	try:
		file_db_stored = media_resources.find_one({ "filename": file_id })
		if file_db_stored and os.path.exists(file_db_stored.get("file_path")) and file_db_stored.get("original_filename") == original_filename:
			return flask.send_file(file_db_stored.get("file_path"), mimetype=file_db_stored.get("mime_type"), download_name=file_db_stored.get("original_filename").replace("_", " "))
		else:
			return flask.make_response("resource not found", 404)
	except:
		random_utilities.log(traceback.format_exc())
		return ResponseModel(cd=500, msg="Something went wrong.").to_json()


# Getting details of the file
@server_instance.route("/media-resources/attachments/<file_id>/<original_filename>/details", methods=["GET"])
@flask_cors.cross_origin()
def get_uploaded_file_details(original_filename, file_id):
	file_db_stored = media_resources.find_one({ "filename": file_id })
	if file_db_stored and file_db_stored.get("original_filename") == original_filename:
		file_db_stored["_id"] = str(file_db_stored["_id"])
		return ResponseModel(cd=200, d=file_db_stored).to_json()
	else:
		return ResponseModel(cd=404, msg="Resource not found.").to_json()


# Deleting an uploaded file
@server_instance.route("/media-resources/attachments/<filename>/<original_filename>", methods=["DELETE"])
@flask_cors.cross_origin()
def delete_uploaded_file(filename, original_filename):
	try:
		# Request an authorization of the user creating the upload
		reauth_response = requests.get("/".join([ os.environ["ACCOUNTS_ENDPOINT"], "authentication/re" ]),
								headers={ "Authorization": flask.request.headers.get("Authorization") })

		if reauth_response.status_code == 200:
			media_resources_db_file = media_resources.find_one({ "filename": filename })
			if media_resources_db_file and media_resources_db_file.get("original_filename") == original_filename:
				deleter_uid = reauth_response.json().get("data").get("p+d").get("email_address")
				if media_resources_db_file.get("uploader_uid") == deleter_uid:
					if os.path.exists(media_resources_db_file.get("fpath")):
						os.remove(media_resources_db_file.get("fpath"))
						media_resources.delete_one({ "filename": filename })
						return ResponseModel(cd=200, msg="Resource has been successfully deleted.").to_json()
					else:
						return ResponseModel(cd=200, msg="Resource has been already deleted.").to_json()
				else:
					return ResponseModel(cd=403, msg="Not enough privilages to delete this resource.").to_json()
			else:
				return ResponseModel(cd=404, msg="Resource not found.").to_json()
		else:
			return ResponseModel(cd=reauth_response.status_code, d=reauth_response.json()).to_json()
	except:
		random_utilities.log(traceback.format_exc())
		return ResponseModel(cd=500, msg="Something went wrong.").to_json()