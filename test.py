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

    
    with open("./test_image.jpg", "rb") as f:
        post_data['image'] = pybase64.b64encode(f.read())
        response = requests.post(url, json=post_data, cookies=cookies)
                
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    print(response.cookies)

# Example Usage
if __name__ == "__main__":
    url = 'http://127.0.0.1:5000/app/new_chat'
    
    cookies = {'user_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNDI1ZWQxYjItM2UwNS00ZjFlLThlMDQtMzUxNTVkMmE4YjA5IiwiZXhwIjoxNzQxNDE0Mjg5LCJyb2xlIjoicGF0aWVudCJ9.PWMYx4soNT0sC36Ih93JTPDzKaxshcbeI5oRSKC4VfE'}
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
        "user_name": "rahama",
        "password": "Ahmedelu2*",
        "phone_number": "0124332",
        "first_name": "rahama",
        "last_name": "elsharkawy",
        "role": "patient"
    }
    conversation = {
        "text": "can you tell me what is in the picture ?",
        "file_id": "d0f2bf7c-bcd7-404a-8ed3-e7bf139c8fd7"
    }
    send_post_request(url, conversation, cookies)
