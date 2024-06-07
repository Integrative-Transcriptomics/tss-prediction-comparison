import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from app.api.allowedFileTypes import FileEndings
from app.job.jobProcessor import job_processor
from app.job.JobObject import JobObject
from app.job.NotReadyException import NotReadyException
import threading
import queue

app = Flask(__name__)
dirname = os.path.dirname(__file__)
FILESTORE = os.path.join(dirname, "store/")

if not os.path.exists(FILESTORE):
    os.makedirs(FILESTORE)

jobQueue = queue.Queue()
jobRegistry = {}

jobThread = threading.Thread(target=job_processor, args=(jobQueue,))
jobThread.daemon = True
jobThread.start()

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

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>File Upload and Job Management</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { width: 600px; margin: 0 auto; }
            .form-group { margin-bottom: 1em; }
            .result { margin-top: 1em; padding: 1em; border: 1px solid #ccc; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>File Upload and Job Management</h1>
          <div class="form-group">
            <form id="upload-form" method="post" action="/upload" enctype="multipart/form-data">
              <input type="file" name="files" multiple>
              <input type="submit" value="Upload">
            </form>
          </div>
          <div class="form-group">
            <label for="jobid">Job ID:</label>
            <input type="text" id="jobid">
            <button onclick="getFile()">Get File</button>
            <button onclick="getJobState()">Get Job State</button>
            <button onclick="getTSS()">Get TSS</button>
          </div>
          <div id="result" class="result"></div>
        </div>
        <script>
          document.getElementById('upload-form').onsubmit = async function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const response = await fetch('/upload', {
              method: 'POST',
              body: formData
            });
            const result = await response.json();
            document.getElementById('result').innerText = JSON.stringify(result, null, 2);
          };

          async function getFile() {
            const jobid = document.getElementById('jobid').value;
            const response = await fetch(`/get_file?jobid=${jobid}`);
            if (response.status === 200) {
              const blob = await response.blob();
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'file';
              document.body.appendChild(a);
              a.click();
              a.remove();
            } else {
              const result = await response.json();
              document.getElementById('result').innerText = JSON.stringify(result, null, 2);
            }
          }

          async function getJobState() {
            const jobid = document.getElementById('jobid').value;
            const response = await fetch(`/get_state?jobid=${jobid}`);
            const result = await response.json();
            document.getElementById('result').innerText = JSON.stringify(result, null, 2);
          }

          async function getTSS() {
            const jobid = document.getElementById('jobid').value;
            const response = await fetch(`/get_tss?jobid=${jobid}`);
            const result = await response.json();
            document.getElementById('result').innerText = JSON.stringify(result, null, 2);
          }
        </script>
      </body>
    </html>
    '''

# Upload endpoint. Checks uploaded file for wiggle file ending, stores file, creates job object and returns job id
# upon sucess
@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("files")
        paths = []
        for file in files:
            file_name, path, file_extension = save_file(file)
            if file_name:
                paths.append(path)
            else:
                status_code = 422
                response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})
                return response_object, status_code

        job = JobObject([path], file_name)
        jobRegistry[job.id] = job
        jobQueue.put(job)

        status_code = 200
        response_object = jsonify({"jobid": job.id})

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
    app.run(debug=True)
