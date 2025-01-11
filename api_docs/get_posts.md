# Get Posts

Route will return all the posts for the forum

**URL** : `/forum/posts`

**Method** : `GET`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "_id": "67822fe9e8b8df4fd74ceec4", 
        "title": "Hello World!", 
        "content": "This post was written automatically", 
        "author": "admin", 
        "created_at": "2025-01-11T10:46:33.624000", 
        "updated_at": None, 
        "photo": None
    }
]
```
