import requests
import json
import pybase64

# Function to send a GET request
def send_get_request(url, cookies):
    response = requests.get(url, cookies=cookies)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

# Function to send a POST request
def send_post_request(url, post_data, cookies):
    with open('./file.txt', "rb") as f:
        files = {'file': f}
        response = requests.post(url, files= files, data=post_data, cookies=cookies)
    """
    with open("./test_image.jpg", "rb") as f:
        post_data['image'] = pybase64.b64encode(f.read())
    """
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    print(response.cookies)

# Example Usage
if __name__ == "__main__":
    url = 'http://127.0.0.1:5000/app/new_file'
    
    cookies = {'user_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMzcyMTEyMDYtNTRkNC00N2YzLTk3NmItZDI0MmE1NDg2ZWUxIiwiZXhwIjoxNzQwNDkwMjQ2LCJyb2xlIjoiYWRtaW4ifQ.ePfIunVaAKUJQo8bMsDgTjBTEBY2zM2Q7yvSgB2iuec'}
    # Sending POST request
    print("\nSending POST request...")
    post_data = {
            "result_date": "2025-6-4"
    }
    another_data = {
        "file_id": "ea613906-b528-457c-8c6a-89f9c149610f",
        "accept_file": "accepted"
    }
    user_data = {
        "user_name": "medo",
        "password": "Ahmedelu2*",
        "role": "admin"
    }
    conversation = {
        "text": "hi",
        "file_id": "381c2b07-2d43-437e-a8aa-04eb1ad069d0"
    }
    send_post_request(url, post_data, cookies)
