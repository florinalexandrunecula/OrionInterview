import streamlit as st
from views.sign_in import sign_in
from views.sign_up import sign_up
from views.posts import posts
from views.profile import profile
from views.admin import admin
from utils.auth import is_authenticated, logout, get_username


PAGES = {
    "Sign In": sign_in,
    "Sign Up": sign_up,
    "Posts": posts,
    "Profile": profile,
    "Admin": admin
}

LOGGED_IN_PAGES = {
    "Posts": posts,
    "Profile": profile,
    "Admin": admin
}


def main():
    if is_authenticated():
        username = get_username()
        st.sidebar.write(f"Hello, {username}!")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()

    selected_page = st.sidebar.radio("Go to", list(
        PAGES.keys() if not is_authenticated() else LOGGED_IN_PAGES.keys()))

    page = PAGES[selected_page]
    page()


if __name__ == "__main__":
    main()
