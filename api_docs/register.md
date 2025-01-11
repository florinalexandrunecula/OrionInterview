# Register

Route used to register a new user

**URL** : `/users/register`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[username]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "testuser",
    "password": "password123"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "access_token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d",
    "token_type": "bearer"
}
```
