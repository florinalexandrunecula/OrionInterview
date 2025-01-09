import streamlit as st
from utils.api import get
from utils.auth import is_authenticated, get_token


def profile():
    if not is_authenticated():
        st.warning("You need to sign in to view your profile.")
        st.stop()

    st.title("My Profile")

    token = get_token()

    response = get("/users/profile", token)
    st.subheader(response.get("user", {}).get("username"))
    st.write(f"Role: {response.get("user", {}).get("role")}")
    st.write(f"Number of posts: {response.get("number_of_posts")}")
