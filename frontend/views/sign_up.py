import streamlit as st
import time
from utils.api import post
from utils.auth import save_token, save_username


def sign_up():
    """
    Implementation of a sign up page
    """
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        response = post("/users/register",
                        {"username": username, "password": password})
        if "access_token" in response:
            save_token(response["access_token"])
            save_username(username)
            st.success("Successfully registered!")
            time.sleep(2)
            st.rerun()
        else:
            st.error(response.get("detail", "Registration failed."))
