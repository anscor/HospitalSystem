## 用户模块

### 用户注册

**POST** /api/users/

#### 请求参数

```json
{
    "username": "test1",
    "password": "password1",
    "email": "email1@test.com",
    "profile": {
        "gender": 0,
        "occupation": 34,
        "age": 18,
        "name": "name",
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1"
    }
}
```

#### 返回参数

##### 成功时 200

```json
{
    "detail": "注册成功！"
}
```

##### 失败时 400 

```json
{
    "detail": "错误信息！"
}
```

### 用户登录

**POST** /api/auth/

#### 请求参数

```json
{
    "username": "username",
    "password": "password"
}
```

#### 返回参数

##### 成功时 200

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3Njg5NjAwNywianRpIjoiMThmZDU3MzMxNzQ0NGM4ZGIzNTU4MTllYjE4MjUyYTEiLCJ1c2VyX2lkIjo3fQ.-xBt27NlNZ_fJYbar0es62pQZoZp9IhDcS01U3fpIYo",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2Mjk0ODA3LCJqdGkiOiJiNjhmMWIyMGEzMWY0YTIwOTUyMDhjYjNlM2NhMjM2YSIsInVzZXJfaWQiOjd9.OaJNTGpZm-pPYzfJCgk0JhBM0LTqBu4C0vBuj2EImjQ"
}
```

`refresh`用于刷新token（7天过期），`access`用于带在请求头上进行登录验证（60分钟过期）。

##### 失败时 401 400

```json
{
    "detail": "No active account found with the given credentials"
}
```

```json
{
    "username": [
        "该字段不能为空。"
    ],
    "password": [
        "该字段不能为空。"
    ]
}
```

#### 示例

```http
POST /api/auth/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/x-www-form-urlencoded
Cache-Control: no-cache

username=test1&password=password1
```

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3Njg5NjAwNywianRpIjoiMThmZDU3MzMxNzQ0NGM4ZGIzNTU4MTllYjE4MjUyYTEiLCJ1c2VyX2lkIjo3fQ.-xBt27NlNZ_fJYbar0es62pQZoZp9IhDcS01U3fpIYo",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2Mjk0ODA3LCJqdGkiOiJiNjhmMWIyMGEzMWY0YTIwOTUyMDhjYjNlM2NhMjM2YSIsInVzZXJfaWQiOjd9.OaJNTGpZm-pPYzfJCgk0JhBM0LTqBu4C0vBuj2EImjQ"
}
```

### 所有用户信息

**GET** /api/users/

#### 请求参数

无

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "username": "username",
        "email": "",
        "profile": null
    },
    {
        "id": 2,
        "username": "username",
        "email": "",
        "profile": {
            "age": 18,
            "name": "name",
            ...
        }
    },
    ...
]
```

##### 失败时 403 401

403

```json
{
    "detail": "您没有执行该操作的权限。"
}
```

#### 示例

```http
GET /api/users/ HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2MjkzMTQ4LCJqdGkiOiIyMGQxNzNiODA1NGE0NWU3OGRkYmY0NjBhNzAwNTg0MSIsInVzZXJfaWQiOjF9.COb9ts0SDLUCd9f46sUVKRtGLNep7EsFrvegja38Vuc
Cache-Control: no-cache
```

```json
[
    {
        "id": 1,
        "username": "anscor",
        "email": "",
        "profile": null
    },
    {
        "id": 2,
        "username": "default",
        "email": "",
        "profile": null
    },
    {
        "id": 7,
        "username": "test1",
        "email": "email1@test.com",
        "profile": {
            "age": 18,
            "name": "name",
            "name_pinyin": "name",
            "gender": 0,
            "identify_id": "100000190001010001",
            "phone": "18888888888",
            "address": "address1",
            "create_time": "2019-12-14T00:08:16.967537",
            "modify_time": "2019-12-14T00:08:16.967537",
            "user": 7,
            "occupation": 34,
            "creator": 7,
            "modifier": null
        }
    }
]
```

### 某一个用户的信息

**GET** /api/users/{pk}/

#### 请求参数

- pk：用户id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 7,
    "username": "test1",
    "email": "email1@test.com",
    "profile": {
        "age": 18,
        "name": "name",
        "name_pinyin": "name",
        "gender": 0,
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1",
        "create_time": "2019-12-14T00:08:16.967537",
        "modify_time": "2019-12-14T00:08:16.967537",
        "user": 7,
        "occupation": 34,
        "creator": 7,
        "modifier": null
    }
}
```

##### 失败时 400 403

```json
{
    "detail": "错误信息"
}
```

### 更新某个用户信息

**PUT** /api/users/{pk}/

#### 请求参数

- pk：用户id。

```json
{
    "password": "password1",
    "email": "email1@test.com",
    "profile": {
        "gender": 0,
        "occupation": 34,
        "age": 18,
        "name": "name",
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1"
    }
}
```

#### 返回参数

##### 成功时 200

```json
{
    "detail": "更改用户信息成功！"
}
```

##### 失败时 400 403

```json
{
    "detail": "错误信息！"
}
```

### 所有组别信息

**GET** /api/groups/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "name": "name",
        "location": "location",
        "contact_phone": "1xxxxxxxxxx"
        ...
    },
    {
        "id": 2,
        "name": "name",
        "location": "location",
        "contact_phone": "1xxxxxxxxxx"
        ...
    },
    ...
]
```

### 某一个组的详细信息

**GET** /api/groups/{pk}/

#### 请求参数

无

#### 返回参数

```json
{
    "id": 1,
    "name": "name",
    "location": "location",
    "contact_phone": "1xxxxxxxxxx"
    ...
}
```

### 某个组下的所有用户信息

**GET** /api/groups/{pk}/users/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "username": "username",
        ...
    },
    {
        "id": 2,
        "username": "username",
        ...
    },
    ...
]
```

### 某个用户所属的所有组

**GET** /api/users/{pk}/groups/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "name": "name",
        "location": "location",
        "contact_phone": "1xxxxxxxxxx"
        ...
    },
    {
        "id": 2,
        "name": "name",
        "location": "location",
        "contact_phone": "1xxxxxxxxxx"
        ...
    },
    ...
]
```

### 所有职业

**GET** /api/occupations/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "name": "name"
    },
    {
        "id": 2,
        "name": "name"
    },
    ...
]
```

### 创建职业

**POST** /api/occupations/

#### 请求参数

```json
{
    "name": "name"
}
```

#### 返回参数

### 某个职业

**GET** /api/occupations/{pk}/

#### 请求参数

无

#### 返回参数

```json
{
    "id": 1,
    "name": "name"
}
```

### 某个职业下的所有用户

**GET** /api/occupations/{pk}/users/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "username": "username",
        ...
    },
    {
        "id": 2,
        "username": "username",
        ...
    },
    ...
]
```

### 所有登入登出记录

**GET** /api/user-logs/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "user": 1,
        "ip": "xxxxxxx",
        "operation": 0,		// 0表示登入，1表示登出
        "operator": 1,
        "operate_time": xxxxxx
    },
    {
        "id": 2,
        "user": 1,
        "ip": "xxxxxxx",
        "operation": 0,		// 0表示登入，1表示登出
        "operator": 1,
        "operate_time": xxxxxx
    },
    ...
]
```

### 某条登入或登出记录

**GET** /api/user-logs/{pk}/

#### 请求参数

无

#### 返回参数

```json
{
    "id": 1,
    "user": 1,
    "ip": "xxxxxxx",
    "operation": 0,		// 0表示登入，1表示登出
    "operator": 1,
    "operate_time": xxxxxx
}
```

### 某个用户的所有登入登出记录

**GET** /api/users/{pk}/user-logs/

#### 请求参数

无

#### 返回参数

```json
[
    {
        "id": 1,
        "user": 1,
        "ip": "xxxxxxx",
        "operation": 0,		// 0表示登入，1表示登出
        "operator": 1,
        "operate_time": xxxxxx
    },
    {
        "id": 2,
        "user": 1,
        "ip": "xxxxxxx",
        "operation": 0,		// 0表示登入，1表示登出
        "operator": 1,
        "operate_time": xxxxxx
    },
    ...
]
```

### 所有病人黑名单

**GET** /api/black-list/

#### 请求参数

无

#### 返回参数

```json
{
    "patient": 1,
    "join_time": xxxxxx,
    "is_delete": 0,
    "reason": "xxx"
}
```

