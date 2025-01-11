# Create Post

Route is used to create a post inside the forum

**URL** : `/forum/posts`

**Method** : `POST`

**Auth required** : YES

**Data constraints**

```json
{
    "title": "[post title]",
    "content": "[post content]",
    "photo": "[optional photo content, encoded using base64.b64encode()]"
}
```

**Data example**

```json
{
    "title": "Post Example",
    "content": "Example post content."
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "message": "Post created successfully."
}
```
