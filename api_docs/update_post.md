# Create Post

Route is used to update a certain post

**URL** : `/forum/posts/{id}`

**Method** : `PUT`

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
    "content": "Updated example post content."
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "message": "Post updated successfully."
}
```
