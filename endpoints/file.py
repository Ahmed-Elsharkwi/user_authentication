""" file api """
from endpoints import app_views
from models.file_model import File
from models.connection import obj
from utils.create_jwt_token import verify_jwt
from flask import jsonify, request, make_response
from datetime import datetime, timedelta
import json
import uuid


@app_views.route('/new_file', strict_slashes=False, methods=['POST'])
def create_file():
    """ create new file for the user """
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401


    file_data = request.form.to_dict()

    file = request.files.get('file')


    if file is None:
        
        return jsonify({'state': 'bad request'}), 400

    if 'result_date' in file_data:
        date_format = '%Y-%m-%d'

        file_data['result_date'] = datetime.strptime(file_data['result_date'], date_format)

    file_data['status'] = 'pending'
    file_data['file_id'] = str(uuid.uuid4())
    file_data['file_path'] = f"./files/{file_data['file_id']}.txt"

    if data['role'] == "admin" or data['role'] == "doctor":
        
        file_data['doctor_admin_id'] = data['user_id']

    else:
        
        file_data['patient_id'] = data['user_id']
    
    new_file = File(file_data)
    result = new_file.create_element('file')

    try:
        with open(file_data['file_path'], "wb") as f:
    
            f.write(file.read())

    except OSError as e:

        print(f"file error: {e}")

    new_file.save_changes()


    return jsonify({'state': result}), 200


@app_views.route('/file_info', strict_slashes=False, methods=['GET'])
def get_file():
    """ get file by id """
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    file_id = request.args.get('file_id')

    element_data = obj.get_element('file', [['file_id', file_id]])

    if element_data is not None:

        file_data = {
                'phone_number': None, 
                'country_code': None, 
                'result_data': None,
                'selected_lab_test': None,
                'result_type': None,
                'content': None,
                'status': None
        }
        index = 1

        for key in file_data:

            if key == "content":

                try:
                    with open(element_data[0][index], "r") as f:

                        file_data[key] = f.read()

                except OSError as e:

                    print(f"file error: {e}")
            else:
            
                file_data[key] = element_data[0][index]

            index += 1
        
        return jsonify(file_data), 200

    return jsonify({'state': 'the file is not found'}), 404


@app_views.route('/files_info', strict_slashes=False, methods=['GET'])
def get_files():
    """ get all pending files """
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if data['role'] != 'admin':
        return jsonify({"state": "Not Authorized"}), 403

    element_data = obj.get_element('file', [['status', 'pending']])

    if element_data is not None:

        files_data = {
                'phone_number': None,
                'country_code': None,
                'result_data': None,
                'selected_lab_test': None,
                'result_type': None,
                'content': None,
                'status': None
        }
        data_dict = []

        for element in element_data:

            index = 1
            files_data = files_data.copy()
            for key in files_data:

                if key == "content":

                    try:
                        with open(element[index], "r") as f:

                            files_data[key] = f.read()

                    except OSError as e:

                        print(f"file error: {e}")
                else:

                    files_data[key] = element[index]

                index += 1

            data_dict.append(files_data)

        return jsonify(data_dict), 200

    return jsonify({'state': 'There are not any pending files'}), 404


@app_views.route('/file_status', strict_slashes=False, methods=['PATCH'])
def update_file_status():
    """ update file status with its id """
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    if data['role'] != 'admin':
        return jsonify({"state": "Not Authorized"}), 403

    file_data = request.json

    if ('accept_file' not in file_data) or ('file_id' not in file_data):
        return jsonify({"state": " bad request "}), 400

    respond = obj.update_element('file', {'status': file_data['accept_file']}, ['file_id', file_data['file_id']])

    obj.save_changes()

    return jsonify({"state": respond}), 200
