# User API

## Installation

To use the User API, you'll need to have the following dependencies installed:

- Flask
- datetime
- re

You can install these dependencies using pip:

```
pip install flask datetime re
```

## Usage

The User API provides the following endpoints:

### Create New User
**Endpoint:** `/new_user`
**Method:** POST
**Request Body:**
```json
{
    "user_name": "example_user",
    "password": "ExamplePassword123!",
    "role": "patient",
    "phone_number": "1234567890",
    "first_name": "John",
    "last_name": "Doe"
}
```
**Response:**
```json
{
    "state": "element is successfully added"
}
```

### Login
**Endpoint:** `/login`
**Method:** POST
**Request Body:**
```json
{
    "user_name": "example_user",
    "password": "ExamplePassword123!",
    "role": "patient"
}
```
**Response:**
```
Set-Cookie: user_token=<JWT_TOKEN>
```

### Get User Info
**Endpoint:** `/user_info`
**Method:** GET
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Response:**
```json
{
    "data": {
        "user_id": 1,
        "user_name": "example_user",
        "password": "hashed_password",
        "role": "patient",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

### Update User Info
**Endpoint:** `/new_user_info`
**Method:** PATCH
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Request Body:**
```json
{
    "user_name": "user_name",
    "phone_number": "1234567890",
    "first_name": "John",
    "last_name": "Doe"
}
```
**Response:**
```json
{
    "state": "the element is successfully updated"
}
```

### Get Patient Info
**Endpoint:** `/patient_info`
**Method:** GET
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Query Parameters:**
```
phone_number=1234567890
```
**Response:**
```json
{
    "data": {
        "user_id": 1,
        "user_name": "example_user",
        "password": "hashed_password",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "role": "patient"
    }
}
```

## API

The User API provides the following endpoints:

1. `/new_user`: Create a new user.
2. `/login`: Log in a user and return a JWT token.
3. `/user_info`: Get the user's information.
4. `/new_user_info`: Update the user's information.
5. `/patient_info`: Get a patient's information.


# File API

## Usage

The File API provides the following endpoints:

### Create New File
**Endpoint:** `/new_file`
**Method:** POST
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Request Body:**
```
file: <file_data>
{
    result_date: 2023-05-01,
    phone_number: 012894789,
    country_code: +20,
    selected_lab_test: lab_1,
    result_type: postive
}
    
```
**Response:**
```json
{
    "state": "element is successfully added"
}
```

### Get File Info
**Endpoint:** `/file_info`
**Method:** GET
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Query Parameters:**
```
file_id=<file_id>
```
**Response:**
```json
{
    "phone_number": "1234567890",
    "country_code": "US",
    "result_data": "2023-05-01",
    "selected_lab_test": "COVID-19",
    "result_type": "Positive",
    "content": "File content",
    "status": "pending"
}
```

### Get All Pending Files
**Endpoint:** `/files_info`
**Method:** GET
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Response:**
```json
[
    {
        "phone_number": "1234567890",
        "country_code": "US",
        "result_data": "2023-05-01",
        "selected_lab_test": "COVID-19",
        "result_type": "Positive",
        "content": "File content",
        "status": "pending"
    },
    {
        "phone_number": "0987654321",
        "country_code": "CA",
        "result_data": "2023-04-15",
        "selected_lab_test": "Flu",
        "result_type": "Negative",
        "content": "File content",
        "status": "pending"
    }
]
```

### Update File Status
**Endpoint:** `/file_status`
**Method:** PATCH
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Request Body:**
```json
{
    "accept_file": "approved",
    "file_id": "<file_id>"
}
```
**Response:**
```json
{
    "state": "element is successfully updated"
}
```

## API

The File API provides the following endpoints:

1. `/new_file`: Create a new file for the user.
2. `/file_info`: Get information about a specific file.
3. `/files_info`: Get information about all pending files.
4. `/file_status`: Update the status of a file.

# AI Chat API

## Usage

The AI Chat API provides the following endpoint:

### Create New Chat
**Endpoint:** `/new_chat`
**Method:** POST
**Headers:**
```
Cookie: user_token=<JWT_TOKEN>
```
**Request Body:**
```json
{
    "image": "<base64_encoded_image>",
    "text": "Hello, Gemini!",
    "file_id": "<file_id>"
}
```
**Response:**
```json
{
    "session_id": "<session_id>",
    "message": "Hello! How can I assist you today?"
}
```

## API

The AI Chat API provides the following endpoint:

1. `/new_chat`: Create a new chat session with Gemini, the AI assistant.

The endpoint accepts an image (in base64 encoded format), text, and an optional file ID. It then generates a response from the Gemini AI model and returns the session ID and the response message.
