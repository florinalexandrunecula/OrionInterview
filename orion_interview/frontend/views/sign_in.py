import streamlit as st
import time
from utils.api import post_form
from utils.auth import save_token, save_username


def sign_in():
    """
    Implementation of a sign in page
    """
    st.title("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        response = post_form(
            "/auth/login", {"username": username, "password": password})
        if "access_token" in response:
            save_token(response["access_token"])
            save_username(username)
            st.success("Successfully signed in!")
            time.sleep(2)
            st.rerun()
        else:
            st.error(response.get("detail", "Login failed."))
