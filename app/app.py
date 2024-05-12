import os
import uuid
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from api.allowedFileTypes import fileEndings
from job.jobProcessor import jobProcessor
from job.jobObject import jobObject
from job.NotReadyException import NotReadyException
import threading
import queue

app = Flask(__name__)

FILESTORE = "store/"

#create route and pass in url
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':

        f = request.files['file']

        _, file_extension = os.path.splitext(f.filename)

        if(fileEndings.has_value(file_extension.lower())):

            file_name = str(uuid.uuid4())
            path = os.path.join(FILESTORE, file_name)
            f.save(path)

            job = jobObject(path, file_name)

            jobRegistry[job.id] = job

            jobQueue.put(job)

            response_object = jsonify({"jobid" : job.id})

            status_code = 200

        else:
            status_code = 422

            response_object = jsonify({"Error" : "Unsupported file ending: " + file_extension})

        return response_object,status_code

@app.route("/get_file", methods=["GET"])
def get_wiggle_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type = str)

        if(id in jobRegistry.keys()):
            job = jobRegistry[id]

            return send_from_directory(FILESTORE, job.name)
        else:
            status_code = 404

            response_object = jsonify({"Error": "No file found with id: " + id})

            return response_object, status_code

@app.route("/get_state", methods=["GET"])
def get_job_state_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type = str)

        if(id in jobRegistry.keys()):
            job = jobRegistry[id]

            status = job.status.value

            status_code = 200

            response_object = jsonify({"Job status": status})

        else:
            status_code = 404

            response_object = jsonify({"Error": "No file found with id: " + id})

        return response_object, status_code


@app.route("/get_tss", methods=["GET"])
def get_tss_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)

        if (id in jobRegistry.keys()):
            job = jobRegistry[id]

            try:
                returnObject = job.getReturnObject()
                status_code = 200
                response_object = jsonify(returnObject)
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})




        else:
            status_code = 404

            response_object = jsonify({"Error": "No file found with id: " + id})

        return response_object, status_code

if(__name__ == "__main__"):

    jobQueue = queue.Queue()

    jobThread = threading.Thread(target=jobProcessor, args= (jobQueue,))

    jobThread.daemon = True

    jobThread.start()

    jobRegistry = {}

    app.run(debug=True)