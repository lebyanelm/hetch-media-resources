"""
________________________________
HETCH MEDIA RESOURCES 
Handles file uploads and serving media content of the users.
________________________________
"""
import tempfile
import traceback
import flask
import flask_cors
import os
import dotenv
import requests
import nanoid
import pyclamd

from models.response import Response
from models.time_created import TimeCreatedModel
from models.file_upload import FileUploadModel

from hetch_utilities import log
from freshclam import run_freshclam

# Initiate PyClamd scanner instance
if os.environ.get("ENVIRONMENT") == "production":
	""" Update virus signatures database. """
	run_freshclam()
	pyclamd = pyclamd.ClamdAgnostic()

"""
__________________________________

DEVELOPMENTAL ENVIRONMENT VARIABLES
__________________________________
"""
if os.environ.get("ENVIRONMENT") != "production":
	dotenv.load_dotenv()


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
SERVER INSTANCE ROUTES
__________________________________
"""
# Returns status of the server
@server_instance.route("/media-resources/status", methods=["GET"])
@flask_cors.cross_origin()
def status():
	return Response(
				cd=200,
				msg="Running",
				d=dict()).to_json()


# Uploading a file
@server_instance.route("/media-resources/upload", methods=["POST"])
@flask_cors.cross_origin()
def upload_a_file():
	try:
		# Request an authorization of the user creating the upload
		auth_response = requests.get("/".join([ os.environ["ACCOUNTS_ENDPOINT"], "authentication/re" ]),
								headers={ "Authorization": flask.request.headers.get("Authorization") })
		if auth_response.status_code == 200:
			""" Check if files were selected to be uploaded """
			if flask.request.files.get("selected_file"):
				# temporarily save the file somewhere temporarily to scan it
				log("Creating temporary upload folder...")
				tmpdir = tempfile.mkdtemp()
				log("Temporary folder created. ✅")
				uploaded_file = flask.request.files["selected_file"]
				filename = ".".join([nanoid.generate(size=10), uploaded_file.filename.split(".")[-1]])
				tmp_upload_path = os.path.join(tmpdir, filename)
				uploaded_file.save(tmp_upload_path)
				log("File saved to temporary folder.")
				
				""" Use PyClamd to scan the temporary uploaded file. """
				scan_results = pyclamd.scan_file(tmp_upload_path) if os.environ.get("ENVIRONMENT") == "production" else None
				if scan_results == None:
					log("File upload safe from viruses. ✅")
					""" Uploaded file is safe from viruses upload the file """
					today_folder = TimeCreatedModel().formatted_date.replace(" ", "_").replace(",", "")
					save_path = os.path.join(os.getcwd(), "uploads")
					if not os.path.exists(save_path):
						os.mkdir(save_path)
					save_path= os.path.join(save_path, today_folder)
					if not os.path.exists(save_path):
						os.mkdir(save_path,)
					save_path= os.path.join(save_path, filename)
					os.rename(tmp_upload_path, save_path)
					log("Moved to permenant location. 👍")
					log("Uploaded file ... " + filename + " in " + today_folder + " 🎉")

					uploaded_file_url= f'{os.environ.get("SELF_ENDPOINT")}/{today_folder}/{filename}'
					data= FileUploadModel(original_filename=uploaded_file.filename,
								filename=filename,
								url=uploaded_file_url,
								uid=auth_response.json()["data"]["p+d"]["email_address"]).__dict__
					return Response(cd=200, d=data).to_json()
				else:
					os.remove(tmp_upload_path)
					return Response(cd=400, msg="Uploaded files not trusted. Not uploaded.").to_json()
			else:
				return Response(cd=400, msg="No files were selected for upload.").to_json()
		else: 
			return Response(cd=auth_response.status_code, d=auth_response.json()).to_json()
	except:
		log(traceback.format_exc())
		return Response(cd=500, msg="Something went wrong.").to_json()


# Getting an uploaded file
@server_instance.route("/media-resources/<date_uploaded>/<file_name>", methods=["GET"])
@flask_cors.cross_origin()
def get_uploaded_file(date_uploaded, file_name):
	try:
		file_path = os.path.join(os.getcwd(), "uploads", date_uploaded, file_name)
		if os.path.exists(file_path):
			return flask.send_file(file_path)
		else:
			return flask.redirect("https://www.hetchfund.capital/not-found")
	except:
		log(traceback.format_exc())
		return Response(cd=500, msg="Something went wrong.").to_json()