# Profile

Route is used to return the profile information of a certain user

**URL** : `/users/profile`

**Method** : `GET`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "user": {
        "role": "user", 
        "username": "testuser", 
        "id": 2
    }, 
    "number_of_posts": 0
}
```
