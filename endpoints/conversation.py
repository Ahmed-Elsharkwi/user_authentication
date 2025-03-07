""" ai chat api """
from endpoints import app_views
from models.mongodb_connection import session
from utils.create_jwt_token import verify_jwt
from flask import jsonify, request, make_response
from datetime import datetime, timedelta
import uuid
from google import genai
from PIL import Image
import pybase64
import requests
import json


@app_views.route('/new_chat', strict_slashes=False, methods=['POST'])
def create_new_chat():
    """ create new chat with gemini """
    jwt_token = request.cookies.get("user_token")
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({"state": "Not Authenticated"}), 401

    data = request.json
    content = []

    if ('image' not in data) or (
            'text' not in data):
        return jsonify({'state': 'bad request'}), 400

    image_path = f"./images/{str(uuid.uuid4())}.jpg"
    
    with open(image_path, "wb") as file:
        file.write(pybase64.b64decode(data['image']))

    del data['image']
    data['image_path'] = image_path
    content.append(Image.open(image_path))
    content.append(data['text'])


    if "file_id" in data:
        response = requests.get(f"http://127.0.0.1:5000/app/file_info?file_id={data['file_id']}", cookies={"user_token": jwt_token})
        content.append(json.loads(response.text)['content'])

    client = genai.Client(api_key="AIzaSyBRCtQL38UvIwVVabMqBV_JiQaiXl25vXY")

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=content
    )

    data["respond"] = response.text

    session_id = str(session.insert_one(data).inserted_id)


    return jsonify({"session_id": session_id, "message": response.text}), 200
