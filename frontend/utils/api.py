import requests

BASE_URL = "http://localhost:8000"


def post(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{BASE_URL}{endpoint}", json=data, headers=headers)
    return response.json()


def post_form(endpoint, data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        f"{BASE_URL}{endpoint}", data=data, headers=headers)
    return response.json()


def put(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.put(f"{BASE_URL}{endpoint}",
                            json=data, headers=headers)
    return response.json()


def delete(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.delete(
        f"{BASE_URL}{endpoint}", json=data, headers=headers)
    return response.json()


def get(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    return response.json()
