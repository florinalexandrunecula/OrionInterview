# All Users

Route is used to get a list of all the users present in the database

**URL** : `/users/all_users`

**Method** : `GET`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "role": "admin", 
        "username": "admin", 
        "id": 1
    }, 
    {
        "role": "user", 
        "username": "testuser", 
        "id": 2
    }
]
```
