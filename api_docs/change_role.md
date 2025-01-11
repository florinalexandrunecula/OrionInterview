# Change Role

Route is used to change the role of a certain user

**URL** : `/users/{username}/role`

**Method** : `PUT`

**Auth required** : YES

**Data constraints**

```json
{
    "role": "[new role]"
}
```

**Data example**

```json
{
    "role": "admin"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "message": "User 'testuser' role changed to 'admin' successfully."
}
```
