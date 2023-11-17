import requests

url = "http://127.0.0.1:5000/get_form"

data = {
    "user_name": "John Doe",
    "order_date": "2022-01-01"
}

response = requests.post(url, data=data)

print(response.json())
