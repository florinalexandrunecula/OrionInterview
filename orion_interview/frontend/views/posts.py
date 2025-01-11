import streamlit as st
import time
import base64
from PIL import Image
from io import BytesIO
from utils.api import get, post, put, delete
from utils.auth import get_token, is_authenticated


def posts():
    """
    Implementation of a forum page, with the following functionalities:
        - The user can see a list of all the posts
        - The user can add a new post
        - The user can edit/delete his posts
    """
    if not is_authenticated():
        st.warning("You need to sign in to view posts.")
        st.stop()

    st.title("Forum Posts")

    token = get_token()

    if "edit_mode" in st.session_state and st.session_state.edit_mode:
        edit_post(token)
        return

    st.subheader("Create a New Post")
    title = st.text_input("Post Title", key="post_title_input")
    content = st.text_area("Post Content", key="post_content_input")
    uploaded_file = st.file_uploader(
        "Choose a photo", type=["jpg", "jpeg", "png"])

    if st.button("Submit Post", key="submit_post_button"):
        if not title or not content:
            st.error("Please fill in both the title and content.")
        else:
            photo = None
            if uploaded_file is not None:
                photo = base64.b64encode(uploaded_file.read()).decode("utf-8")
            post_data = {
                "title": title,
                "content": content,
                "photo": photo,
            }
            response = post("/forum/posts", post_data, token)
            if response.get("message") == "Post created successfully.":
                st.success(f"Post '{title}' created successfully!")
                time.sleep(2)
                st.rerun()
            else:
                st.error(
                    "Failed to create post")

    response = get("/forum/posts", token)
    if isinstance(response, list):
        for post_dict in response:
            st.subheader(f"{post_dict['title']} (ID: {post_dict['_id']})")
            st.write(post_dict["content"])
            st.write(f"Author: {post_dict['author']}")
            st.write(f"Created At: {post_dict['created_at']}")
            if post_dict.get("photo"):
                image_data = base64.b64decode(post_dict["photo"])
                image = Image.open(BytesIO(image_data))
                st.image(image, use_container_width=True)

            if st.button("Edit", key=f"edit_{post_dict['_id']}"):
                st.session_state.edit_mode = True
                st.session_state.edit_title = post_dict["title"]
                st.session_state.edit_id = post_dict["_id"]
                st.rerun()

            if st.button("Delete", key=f"delete_{post_dict['_id']}"):
                delete_post(post_dict["_id"], token)
                st.rerun()

            st.write("---")
    else:
        st.error("Failed to load posts")


def edit_post(token: str | None = None):
    """
    Implementation of a helper view that contains an editing menu for a post

    Args:
        token (str | None, optional): The generated JWT token. Defaults to None.
    """
    title = st.session_state.get("edit_title")
    st.subheader(f"Edit Post: {title}")
    id = st.session_state.get("edit_id")

    response = get(f"/forum/posts/{id}", token)
    if "title" not in response:
        st.error("Failed to load the post for editing.")
        st.session_state.edit_mode = False
        st.rerun()

    new_title = st.text_input(
        "New Title", value=response["title"], key="edit_title_input")
    new_content = st.text_area(
        "New Content", value=response.get("content"), key="edit_content_input")

    if response.get("photo"):
        st.write("Current Photo:")
        image_data = base64.b64decode(response["photo"])
        image = Image.open(BytesIO(image_data))
        st.image(image, use_container_width=True)

    uploaded_file = st.file_uploader(
        "Upload a new photo (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Save Changes", key="save_changes_button"):
        new_photo = None
        if uploaded_file is not None:
            new_photo = base64.b64encode(uploaded_file.read()).decode("utf-8")
        post_data = {
            "title": new_title,
            "content": new_content,
            "photo": new_photo,
        }
        response = put(f"/forum/posts/{id}", post_data, token)
        if response.get("message") == "Post updated successfully.":
            st.success("Post updated successfully!")
            st.session_state.edit_mode = False
            time.sleep(2)
            st.rerun()
        else:
            st.error("Failed to update the post.")

    if st.button("Cancel", key="cancel_edit_button"):
        st.session_state.edit_mode = False
        st.rerun()


def delete_post(id: str, token: str | None = None):
    """
    Helper component responsible for deleting a post

    Args:
        id (str): id of the post
        token (str | None, optional): The generated JWT token. Defaults to None.
    """
    response = delete(f"/forum/posts/{id}", {}, token)
    if response.get("message") == "Post deleted successfully.":
        st.success(f"Post '{id}' deleted successfully!")
        time.sleep(2)
    else:
        st.error("Failed to delete the post.")
        time.sleep(2)
