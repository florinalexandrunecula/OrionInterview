# OrionInterview
## Project Overview
Project represents a simple forum application, in which users and admins can post text and images.
The project structure contains two directories (frontend and backend), containing the code of the app components. 

## Project Requirements
- Python3.13
- MongoDB
- SQLite

## Getting Started

### Clone the repository
Clone the repository using
`git clone https://github.com/florinalexandrunecula/OrionInterview.git`

### Python environment setup
If you haven't created a python virtual environment yet, you can create one using `python3.13 -m venv <path_to_venv>` and source it using `source <path_to_venv>/bin/activate`.
Replace `<path_to_venv>` with a suitable path.
Inside the root of the repository, run the following command to install all the python packages dependencies `pip install -r requirements.txt`.

### SQLite and MongoDB setup
To initialize the databases with data, a script is provided inside `backend/app/utils`. This script will create the SQLite database inside `backend` directory and will populate the MongoDB with a post example. To run the script, use `python -m app.utils.init_db`.
###### Note: the code will assume that the MonogDB is locally deployed on `mongodb://localhost:27017`. If you want to provide another DB location, export a new Environment Variable called `MONGO_URL` and populate it with the connection string.

## Running the App
### Backend
Navigate to `backend` directory and run `uvicorn app.main:app --reload`.
This will deploy the backend application on `http://127.0.0.1:8000`.

### Frontend
Navigate to `frontend` directory and run `streamlit run app.py`.
This will deploy the frontend application on `http://localhost:8501`.

## Testing the App
### Backend
Navigate to `backend` directory and run `pytest testing/`. A small suite of tests is present, showcasing different functionalities of the backend.

### Frontend
Navigate to `frontend` directory and run `pytest testing/ --headed`. A small suite of tests is present, showcasing different functionalities of the frontend.