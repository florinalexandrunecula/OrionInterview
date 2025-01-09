import streamlit as st


def save_token(access_token: str):
    st.session_state["access_token"] = access_token


def save_username(username: str):
    st.session_state["username"] = username


def get_token():
    return st.session_state.get("access_token", None)


def get_username():
    return st.session_state.get("username", None)


def is_authenticated():
    return "access_token" in st.session_state


def logout():
    st.session_state.pop("access_token", None)
    st.session_state.pop("username", None)
