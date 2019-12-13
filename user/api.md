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

### 所有用户信息

**GET** /api/users/

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

### 某一个用户的信息

**GET** /api/users/{id}/

#### 请求参数

无

#### 返回参数

```json
{
    "id": 1,
    "username": "username",
    ...
},
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

**GET** /api/groups/{id}/

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

**GET** /api/groups/{id}/users/

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

**GET** /api/users/{id}/groups/

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

**GET** /api/occupations/{id}/

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

**GET** /api/occupations/{id}/users/

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

**GET** /api/user-logs/{id}/

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

**GET** /api/users/{id}/user-logs/

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

