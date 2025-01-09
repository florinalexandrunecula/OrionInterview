import streamlit as st
from utils.api import get, put, delete
from utils.auth import get_token, is_authenticated

def admin():
    """
    Implementation of an admin page, with the following functionalities:
        - Admins can see a list of all non-admin users
        - They can promote a certain user to admin role
        - They can delete a certain user
    """
    if not is_authenticated():
        st.warning("You need to sign in to view this page.")
        st.stop()

    token = get_token()

    current_user = get("/users/profile", token)
    if current_user.get("user", {}).get("role") != "admin":
        st.error("You do not have permission to access this page.")
        st.stop()

    st.title("Admin Panel - Manage Users")

    response = get("/users/all_users", token)
    if isinstance(response, list):
        non_admin_users = [user for user in response if user["role"] != "admin"]

        if not non_admin_users:
            st.info("No users available to manage.")
            return

        for user in non_admin_users:
            st.subheader(user["username"])
            st.write(f"Role: {user['role']}")

            if user["role"] != "admin":
                if st.button(f"Make Admin - {user['username']}", key=f"make_admin_{user['username']}"):
                    response = put(f"/users/{user['username']}/role", {"role": "admin"}, token)
                    if response.get("message") == f"User '{user['username']}' role changed to 'admin' successfully.":
                        st.success(f"User {user['username']} is now an admin.")
                        st.rerun()
                    else:
                        st.error("Failed to update user role.")

            if st.button(f"Delete Account - {user['username']}", key=f"delete_user_{user['username']}"):
                response = delete(f"/users/{user['username']}", {}, token)
                if response.get("message") == f"User '{user['username']}' deleted successfully.":
                    st.success(f"User {user['username']} deleted successfully.")
                    st.rerun()
                else:
                    st.error("Failed to delete user account.")

            st.write("---")
    else:
        st.error("Failed to load users. Please check your token.")
