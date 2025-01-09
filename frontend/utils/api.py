import requests

BASE_URL = "http://localhost:8000"


def post(endpoint: str, data: dict, token: str | None = None):
    """
    POST method implementation

    Args:
        endpoint (str): Endpoint for the request
        data (dict): Dictionary containing the request data 
        token (str | None, optional): The generated JWT token. Defaults to None.

    Returns:
        dict: The json response in dict format
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{BASE_URL}{endpoint}", json=data, headers=headers)
    return response.json()


def post_form(endpoint: str, data: dict):
    """
    POST method implementation that has content in form format

    Args:
        endpoint (str): Endpoint for the request
        data (dict): Dictionary containing the request data

    Returns:
        dict: The json response in dict format
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        f"{BASE_URL}{endpoint}", data=data, headers=headers)
    return response.json()


def put(endpoint: str, data: dict, token: str | None = None):
    """
    PUT method implementation

    Args:
        endpoint (str): Endpoint for the request
        data (dict): Dictionary containing the request data
        token (str | None, optional): The generated JWT token. Defaults to None.

    Returns:
        dict: The json response in dict format
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.put(f"{BASE_URL}{endpoint}",
                            json=data, headers=headers)
    return response.json()


def delete(endpoint: str, data: dict, token: str | None = None):
    """
    DELETE method implementation

    Args:
        endpoint (str): Endpoint for the request
        data (dict): Dictionary containing the request data
        token (str | None, optional): The generated JWT token. Defaults to None.

    Returns:
        dict: The json response in dict format
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.delete(
        f"{BASE_URL}{endpoint}", json=data, headers=headers)
    return response.json()


def get(endpoint: str, token: str | None = None):
    """
    GET method implementation

    Args:
        endpoint (str): Endpoint for the request
        token (str | None, optional): The generated JWT token. Defaults to None.

    Returns:
        dict: The json response in dict format
    """
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    return response.json()
