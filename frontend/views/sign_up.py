import streamlit as st
from utils.api import post


def sign_up():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        response = post("/users/register",
                        {"username": username, "password": password})
        if "access_token" in response:
            st.success("Successfully registered!")
        else:
            st.error(response.get("detail", "Registration failed."))
