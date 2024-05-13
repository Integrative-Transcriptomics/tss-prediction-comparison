import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from api.allowedFileTypes import FileEndings
from job.jobProcessor import job_processor
from job.JobObject import JobObject
from job.NotReadyException import NotReadyException
import threading
import queue

app = Flask(__name__)
FILESTORE = "store/"
jobQueue = queue.Queue()
jobRegistry = {}


# save file and return file name, extension and as the path it is stored at
def save_file(file):
    _, file_extension = os.path.splitext(file.filename)

    if FileEndings.has_value(file_extension.lower()):
        file_name = str(uuid.uuid4())
        path = os.path.join(FILESTORE, file_name)
        file.save(path)
        return file_name, path, file_extension
    else:
        return None, None, file_extension


# returns jobid if known to registry, otherwise returns None
def get_job_by_id(id_):
    if id_ in jobRegistry:
        return jobRegistry[id_]
    else:
        return None


# Upload endpoint. Checks uploaded file for wiggle file ending, stores file, creates job object and returns job id
# upon sucess
@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_name, path, file_extension = save_file(file)

        if file_name:
            job = JobObject(path, file_name)
            jobRegistry[job.id] = job
            jobQueue.put(job)

            status_code = 200
            response_object = jsonify({"jobid": job.id})
        else:
            status_code = 422
            response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})

        return response_object, status_code


# get file by id endpoint. Returns the wiggle file if a job with given id exists
@app.route("/get_file", methods=["GET"])
def get_wiggle_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)

        if job:
            return send_from_directory(FILESTORE, job.name)
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
            return response_object, status_code


# gets job state by id. Returns job state ("Not started", "Running", "Finished", "Failed") if job exists
@app.route("/get_state", methods=["GET"])
def get_job_state_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)
        if job:
            status = job.status.value
            status_code = 200
            response_object = jsonify({"Job status": status})
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
        return response_object, status_code


# gets tss prediction by id. Fails if Job state is not finished.
@app.route("/get_tss", methods=["GET"])
def get_tss_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)
        if job:
            try:
                return_object = job.get_return_object()
                status_code = 200
                response_object = jsonify(return_object)
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
        return response_object, status_code


if __name__ == "__main__":
    jobThread = threading.Thread(target=job_processor, args=(jobQueue,))
    jobThread.daemon = True
    jobThread.start()
    app.run(debug=True)
