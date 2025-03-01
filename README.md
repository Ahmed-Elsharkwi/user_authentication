# README

## Installation

To install and set up the project, follow these steps:

1. Clone the repository:
```
git clone https://github.com/your-username/your-project.git
```
2. Navigate to the project directory:
```
cd your-project
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

To use the application, follow these steps:

1. Start the Flask server:
```
python app.py
```
2. Access the application in your web browser at `http://localhost:5000`.

## API

The application provides the following API endpoints:

### `POST /new_user`
- **Description:** Create a new user.
- **Request Body:**
  - `user_name` (string): The username of the new user.
  - `password` (string): The password of the new user.
  - `role` (string): The role of the new user (e.g., "admin", "doctor", "patient").
  - `phone_number` (string, optional): The phone number of the new user (required for "patient" role).
  - `first_name` (string, optional): The first name of the new user (required for "patient" role).
  - `last_name` (string, optional): The last name of the new user (required for "patient" role).
- **Response:**
  - `200 OK`: The user was created successfully.
  - `400 Bad Request`: The request body is missing required fields or the input is invalid.

### `POST /login`
- **Description:** Log in a user and return a JWT token.
- **Request Body:**
  - `user_name` (string): The username of the user.
  - `password` (string): The password of the user.
  - `role` (string): The role of the user (e.g., "admin", "doctor", "patient").
- **Response:**
  - `200 OK`: The user was logged in successfully, and a JWT token is returned in the response cookie.
  - `400 Bad Request`: The request body is missing required fields or the input is invalid.
  - `401 Unauthorized`: The username or password is incorrect.
  - `404 Not Found`: The user is not found.

### `GET /user_info`
- **Description:** Get the user's information.
- **Request:** The JWT token is included in the request cookie.
- **Response:**
  - `200 OK`: The user's information is returned.
  - `401 Unauthorized`: The user is not authenticated.

### `PATCH /new_user_info`
- **Description:** Update the user's information.
- **Request Body:** The updated user information.
- **Request:** The JWT token is included in the request cookie.
- **Response:**
  - `200 OK`: The user's information was updated successfully.
  - `401 Unauthorized`: The user is not authenticated.

### `GET /patient_info`
- **Description:** Get the patient's information.
- **Request:** The JWT token is included in the request cookie, and the `phone_number` parameter is provided in the query string.
- **Response:**
  - `200 OK`: The patient's information is returned.
  - `401 Unauthorized`: The user is not authenticated.
  - `404 Not Found`: The patient's information is not found.

## Contributing

To contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests, execute the following command:

```
python -m unittest discover tests
```

This will run all the tests in the `tests` directory.