""" user api """
from endpoints import app_views
from models.connection import obj
from utils.create_jwt_token import create_jwt, verify_jwt
from flask import jsonify, request, make_response
from utils.hash_passwords import hash_password
from datetime import datetime, timedelta
import re


@app_views.route('/new_user', strict_slashes=False, methods=['POST'])
def create_new_user():
    """ sign up endpoint """

    user_data = request.json
    table = None

    if ('user_name' not in user_data) or (
            'password' not in user_data) or (
                    'role' not in user_data):

                return jsonify({"state": "bad request"}), 400

    if (user_data['role'].lower() == 'patient') and ((
            'phone_number' not in user_data) or (
                'first_name' not in user_data) or (
                    'last_name' not in user_data)):

                return jsonify({"state": "Patient info is missing"}), 400

    user_check = re.match(r'^[a-zA-Z0-9]{3,16}$', user_data['user_name'])
    password_check = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", user_data['password'])

    if user_check is None:
        return jsonify({'state': 'Not a valid user_name'}), 400

    if password_check is None:
        return jsonify({'state': 'Not a valid password'}), 400


    if user_data['role'] == 'admin' or user_data['role'] == 'doctor':

        table = 'doctor_admin'
    
    elif user_data['role'] == 'patient':
        
        table = 'patient'

    else:
        return jsonify({"state": "role is not valid"}), 400


    if obj.get_element(table, [['user_name', user_data['user_name']]]) is None:
        
        result = obj.create_element(table, user_data)
        obj.save_changes()
        
        return jsonify({'state': result}), 200

    return jsonify({'state': 'User_name already exist'}), 200


@app_views.route('/login', strict_slashes=False, methods=['POST'])
def login_fun():
    """ log the user in the system and return jwt token to user """
       
    user_data = request.json
    list_attributes = [['user_name', user_data['user_name']]]

    if ('user_name' not in user_data) or (
            'password' not in user_data) or (
                    'role' not in user_data):

                return jsonify({'state': 'bad_request'}), 400
        
    user_check = re.match(r'^[a-zA-Z0-9]{3,16}$', user_data['user_name'])
    password_check = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", user_data['password'])

    if user_check is None:
        return jsonify({'state': 'Not a valid user_name'}), 400

    if password_check is None:
        return jsonify({'state': 'Not a valid password'}), 400

    if user_data['role'] == 'admin' or user_data['role'] == 'doctor':
        
        list_attributes.append(['role', user_data['role']])
        table = 'doctor_admin'

    elif user_data['role'] == 'patient':

        table = 'patient'

    else:
        return jsonify({"state": "role is not valid"}), 400


    data = obj.get_element(table, list_attributes)
        
    if data is not None:

        if hash_password(user_data['password']) != data[0][2]:
            return jsonify({'state': 'password is not correct '}), 401
            
        token = create_jwt({"user_id": data[0][0], 'exp': datetime.utcnow() + timedelta(seconds=60000), 'role': user_data['role']})
        response = make_response()
        response.set_cookie('user_token', token, samesite='None', secure=True)

        return response

    return jsonify({'state': 'User is not found please sign up'}), 404


@app_views.route('/user_info', strict_slashes=False, methods=['GET'])
def get_user_info():
    """ get the user info using his id """
    
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_id = data['user_id']
    role = data['role']
    user_attributes_list = ['user_id', 'user_name', 'password', 'role']
    user_data = {}
    count = 0


    if role == 'admin' or role == 'doctor':

        table = 'doctor_admin'

    elif role == 'patient':

        patient_attributes_list = ['user_id', 'user_name', 'password', 'phone_number', 'first_name', 'last_name', 'role']

        table = 'patient'

    else:
        return jsonify({"state": "role is not valid"}), 400

    data = obj.get_element(table, [[f'{table}_id', user_id]])

    if data is not None:
        for value in data[0]:

            if role == 'patient':
                user_data[patient_attributes_list[count]] = value

            else:
                user_data[user_attributes_list[count]] = value
            
            count += 1

        return jsonify({'data': user_data}), 200
    
    return jsonify({'state': 'There is no info for the user'}), 404


@app_views.route('/new_user_info', strict_slashes=False, methods=['PATCH'])
def update_user_info():
    """ update user info with its id """

    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    user_data = request.json
    user_name = user_data.get('user_name')
    role = data.get('role')

    if role == 'admin' or role == 'doctor':
        
        table = 'doctor_admin'

    elif role == 'patient':
        
        table = 'patient'

    else:
        return jsonify({"state": "role is not valid"}), 400


    if user_name is None or ((user_name is not None) and (obj.get_element(table, [['user_name', user_name]]) is None)):

        respond = obj.update_element(table, user_data, [f'{table}_id', data['user_id']])
        obj.save_changes()

        return jsonify({'state': respond})
    
    return jsonify({'state': "the user name already exist please change it to another one"})


@app_views.route('/patient_info', strict_slashes=False, methods=['GET'])
def get_patient_info():
    """ get the user info using his id """

    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    role = data['role']
    phone_number = request.args.get('phone_number')
    user_data = {}
    count = 0


    if role == 'patient':

        patient_attributes_list = ['user_id', 'user_name', 'password', 'phone_number', 'first_name', 'last_name', 'role']

        table = 'patient'

    else:
        return jsonify({"state": "role is not valid"}), 400

    data = obj.get_element(table, [['phone_number', phone_number]])

    if data is not None:
        for value in data[0]:

            user_data[patient_attributes_list[count]] = value
            count += 1

        return jsonify({'data': user_data}), 200

    return jsonify({'state': 'There is no info for the user'}), 404

