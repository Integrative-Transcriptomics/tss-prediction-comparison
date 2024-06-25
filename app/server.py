import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, Response
from app.api.allowedFileTypes import FileEndings
from app.job.jobProcessor import job_processor
from app.job.JobObject import JobObject
from app.job.JobObject import returnType
from app.job.JobExceptions import NotReadyException
from json import loads, dumps
import threading
import queue
import io

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

# turn dataframe into csv object for response endpoints
def df_to_response(df, filename):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0) #reset buffer

    response = Response(buffer, mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=" + filename

    return response

# Upload endpoint. Checks uploaded file for wiggle file ending, stores file, creates job object and returns job id
# upon sucess
@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':

        conditions_forward = {}
        conditions_reverse = {}

        gff_path = None
        master_table_path = None

        for key in request.files:
            print(key)
            if key.startswith("condition_"):
                condition = key.split("condition_")[1].split("_")[0]

                if "forward" in key:

                    if condition not in conditions_forward:
                        conditions_forward[condition] = [key]
                    else:
                        conditions_forward[condition] += [key]
                else:
                    if condition not in conditions_reverse:
                        conditions_reverse[condition] = [key]
                    else:
                        conditions_reverse[condition] += [key]

            if (key == "gff"):
                file_name, path, file_extension = save_file(request.files.get(key))

                if file_name:
                    gff_path = path
                else:
                    status_code = 422
                    response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})
                    return response_object, status_code

            if (key == "master_table"):
                file_name, path, file_extension = save_file(request.files.get(key))

                if file_name:
                    master_table_path = path
                else:
                    status_code = 422
                    response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})
                    return response_object, status_code

        response_json = {}
        for condition in conditions_forward:
            paths = []
            for key in conditions_forward[condition]:
                file_name, path, file_extension = save_file(request.files.get(key))
                if file_name:
                    paths.append(path)
                else:
                    status_code = 422
                    response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})
                    return response_object, status_code


            job = JobObject(filepaths=[path], name=file_name, master_table_path=master_table_path, gff_path=gff_path, is_reverse_strand=False)
            jobRegistry[job.id] = job
            jobQueue.put(job)
            response_json["Condition " + condition] = {"forward": job.id}

        for condition in conditions_reverse:
            paths = []
            for key in conditions_reverse[condition]:
                file_name, path, file_extension = save_file(request.files.get(key))
                if file_name:
                    paths.append(path)
                else:
                    status_code = 422
                    response_object = jsonify({"Error": "Unsupported file ending: " + file_extension})
                    return response_object, status_code

            job = JobObject(filepaths=[path], name=file_name, master_table_path=master_table_path, gff_path=gff_path, is_reverse_strand=True)
            jobRegistry[job.id] = job
            jobQueue.put(job)
            response_json["Condition " + condition]["reverse"] = job.id

        print(response_json)
        status_code = 200
        response_object = jsonify(response_json)

        return response_object, status_code


# get file by id endpoint. Returns the wiggle file if a job with given id exists
@app.route("/get_file", methods=["GET"])
def get_wiggle_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)
        if job:
            try:
                mean_df = job.get_processed_df()
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})
                return response_object, status_code

            return_df = mean_df.to_json()
            parsed_json = loads(return_df)

            status_code = 200

            return parsed_json, status_code
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
                tss_df = job.get_file(returnType.TSS)
                response_object = df_to_response(tss_df, "tss_prediction.csv")
                status_code = 200
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
        return response_object, status_code

# gets tss comparison by id. Fails if Job state is not finished.
@app.route("/get_common", methods=["GET"])
def get_common_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)
        if job:
            try:
                common_df = job.get_file(returnType.COMMON)
                response_object = df_to_response(common_df, "common_prediction.csv")
                status_code = 200
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
        return response_object, status_code

# gets master table by id. Fails if Job state is not finished.
@app.route("/get_master_table", methods=["GET"])
def get_master_by_id():
    if request.method == 'GET':
        id = request.args.get('jobid', type=str)
        job = get_job_by_id(id)
        if job:
            try:
                master_df = job.get_file(returnType.MASTERTABLE)
                response_object = df_to_response(master_df, "master_table.csv")
                status_code = 200
            except NotReadyException as e:
                status_code = 400
                response_object = jsonify({"Error": e.message})
        else:
            status_code = 404
            response_object = jsonify({"Error": "No file found with id: " + id})
        return response_object, status_code


if __name__ == "__main__":
    app.run(debug=True)
