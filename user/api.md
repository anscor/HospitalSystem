## 用户登录注册相关

### 用户注册

**POST** /api/users/

#### 请求参数

```json
{
    "username": "test1",
    "password": "password1",
    "email": "email1@test.com",
    "group": 123,  // 关联组id。可以不传，不传时设置为病人
    "profile": {
        "gender": 0,
        "occupation": 34,	// 关联职业id
        "name": "name",
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1"
    }
}
```

#### 返回参数

##### 成功时 201

```json
{
    "id": 14,
    "username": "test6",
    "email": "email6@test.com",
    "profile": {
        "name": "test6",
        "name_pinyin": "test6",
        "gender": 0,
        "identify_id": "100000190001010006",
        "phone": "18888888886",
        "address": "address6",
        "create_time": "2019-12-14T21:11:55.225293",
        "modify_time": "2019-12-14T21:11:55.226335",
        "user": 14,
        "occupation": 34,
        "creator": 14,
        "modifier": null
    }
}
或
{
    "id": 2,
    "username": "default",
    "email": "",
    "profile": null
}
```

##### 失败时 400

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

### 通过token获取用户信息

**GET** /api/auth/user/

#### 返回参数

##### 成功时 200

```json
{
    "id": 7,
    "username": "test1",
    "email": "email1@test.com",
    "profile": {
        "name": "name",
        "name_pinyin": "name",
        "gender": 0,
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1",
        "create_time": "2019-12-14T00:08:16.967537",
        "modify_time": "2019-12-14T00:08:16.967537",
        "user": 7,	// profile对应用户id，一般没用
        "occupation": 34,	// 关联职业id
        "creator": 7,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
```

##### 失败时 401

### 刷新token

**POST** /api/auth/refresh/

#### 请求参数

```json
"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3Njg5NjAwNywianRpIjoiMThmZDU3MzMxNzQ0NGM4ZGIzNTU4MTllYjE4MjUyYTEiLCJ1c2VyX2lkIjo3fQ.-xBt27NlNZ_fJYbar0es62pQZoZp9IhDcS01U3fpIYo"
```

#### 返回参数

##### 200

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2Mjk0ODA3LCJqdGkiOiJiNjhmMWIyMGEzMWY0YTIwOTUyMDhjYjNlM2NhMjM2YSIsInVzZXJfaWQiOjd9.OaJNTGpZm-pPYzfJCgk0JhBM0LTqBu4C0vBuj2EImjQ"
}
```

### 用户登出

**GET** /api/auth/logout/

#### 返回参数

##### 200

## 用户信息相关

### 所有用户信息

**GET** /api/users/

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
        "id": 7,
        "username": "test1",
        "email": "email1@test.com",
        "profile": {
            "name": "name",
            "name_pinyin": "name",
            "gender": 0,
            "identify_id": "100000190001010001",
            "phone": "18888888888",
            "address": "address1",
            "create_time": "2019-12-14T00:08:16.967537",
            "modify_time": "2019-12-14T00:08:16.967537",
            "user": 7,	// profile对应用户id，一般没用
            "occupation": 34,	// 关联职业id
            "creator": 7,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    ...
]
```

##### 失败时 403 401

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
        "name": "name",
        "name_pinyin": "name",
        "gender": 0,
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1",
        "create_time": "2019-12-14T00:08:16.967537",
        "modify_time": "2019-12-14T00:08:16.967537",
        "user": 7,	// profile对应用户id，一般没用
        "occupation": 34,	// 关联职业id
        "creator": 7,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
或
{
    "id": 2,
    "username": "default",
    "email": "",
    "profile": null
}
```

##### 失败时 404 403

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
        "occupation": 34,	// 关联职业id
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
    "id": 7,
    "username": "test1",
    "email": "email1@test.com",
    "profile": {
        "name": "name",
        "name_pinyin": "name",
        "gender": 0,
        "identify_id": "100000190001010001",
        "phone": "18888888888",
        "address": "address1",
        "create_time": "2019-12-14T00:08:16.967537",
        "modify_time": "2019-12-14T00:08:16.967537",
        "user": 7,	// profile对应用户id，一般没用
        "occupation": 34,	// 关联职业id
        "creator": 7,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
或
{
    "id": 2,
    "username": "default",
    "email": "",
    "profile": null
}
```

##### 失败时 400 403 404

### 删除某个用户

**DELETE** /api/users/{pk}/

#### 请求参数

- pk：用户id。

#### 返回参数

##### 成功时 200 404 401

## 用户组相关

### 所有组别信息

**GET** /api/groups/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 221,
        "name": "化验科",
        "profile": {
            "location": "化验科地址",
            "contact_phone": "18812341234",
            "create_time": "2019-12-14T17:16:02.911170",
            "modify_time": "2019-12-14T17:16:02.911170",
            "group": 221,	// profile对应组的id，一般没用
            "parent_group": 238,	// 关联组id
            "creator": 1,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    {
        "id": 218,
        "name": "医生",
        "profile": null
    },
    ...
]
```

### 所有可预约的科室信息

**GET** /api/departments/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 221,
        "name": "化验科",
        "profile": {
            "location": "化验科地址",
            "contact_phone": "18812341234",
            "create_time": "2019-12-14T17:16:02.911170",
            "modify_time": "2019-12-14T17:16:02.911170",
            "group": 221,	// profile对应组的id，一般没用
            "parent_group": 238,	// 关联组id
            "creator": 1,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    {
        "id": 218,
        "name": "医生",
        "profile": null
    },
    ...
]
```

### 添加组

**POST** /api/groups/

#### 请求参数

```json
{
    "name": "group1",
    "profile": {
        "location": "location1",
        "contact_phone": "18888888881",
        "parent_group": 238	// 关联组id。可选
    }
}
```

#### 返回参数

##### 成功时 201

```json
{
    "id": 221,
    "name": "化验科",
    "profile": {
        "location": "化验科地址",
        "contact_phone": "18812341234",
        "create_time": "2019-12-14T17:16:02.911170",
        "modify_time": "2019-12-14T17:16:02.911170",
        "group": 221,	// profile对应组的id，一般没用
        "parent_group": 238,	// 关联组id
        "creator": 1,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
```

##### 失败时 400 401 403

### 某一个组的详细信息

**GET** /api/groups/{pk}/

**GET** /api/groups/?name=

#### 请求参数

- pk：组id。
- name：组名。

#### 返回参数

##### 成功时 200

```json
{
    "id": 221,
    "name": "化验科",
    "profile": {
        "location": "化验科地址",
        "contact_phone": "18812341234",
        "create_time": "2019-12-14T17:16:02.911170",
        "modify_time": "2019-12-14T17:16:02.911170",
        "group": 221,	// profile对应组的id，一般没用
        "parent_group": 238,	// 关联组id
        "creator": 1,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
```

##### 失败时 401 404

### 修改某个组的信息

**PUT** /api/groups/{pk}/

#### 请求参数

- pk：组id。

```json
{
    "name": "group1",
    "profile": {
        "location": "location1",
        "contact_phone": "18888888881",
        "parent_group": 238	// 关联组id
    }
}
```

#### 返回参数

##### 成功时 200

```json
{
    "id": 221,
    "name": "化验科",
    "profile": {
        "location": "化验科地址",
        "contact_phone": "18812341234",
        "create_time": "2019-12-14T17:16:02.911170",
        "modify_time": "2019-12-14T17:16:02.911170",
        "group": 221,	// profile对应组的id，一般没用
        "parent_group": 238,	// 关联组id
        "creator": 1,	// 关联用户id
        "modifier": null	// 关联用户id
    }
}
```

##### 失败时 400 401 403 404

### 删除某个组

**DELETE** /api/groups/{pk}/

#### 请求参数

- pk：组id。

#### 返回参数

##### 204 404 403 401

## 用户与组关系相关

### 某个组下的所有用户信息

**GET** /api/groups/{pk}/users/

#### 请求参数

- pk：用户组id。

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
        "id": 7,
        "username": "test1",
        "email": "email1@test.com",
        "profile": {
            "name": "name",
            "name_pinyin": "name",
            "gender": 0,
            "identify_id": "100000190001010001",
            "phone": "18888888888",
            "address": "address1",
            "create_time": "2019-12-14T00:08:16.967537",
            "modify_time": "2019-12-14T00:08:16.967537",
            "user": 7,	// profile对应用户id，一般没用
            "occupation": 34,	// 关联职业id
            "creator": 7,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    ...
]
```

##### 失败时 400 404 403 401

### 某个用户所属的所有组

**GET** /api/users/{pk}/groups/

#### 请求参数

- pk：用户id。

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 221,
        "name": "化验科",
        "profile": {
            "location": "化验科地址",
            "contact_phone": "18812341234",
            "create_time": "2019-12-14T17:16:02.911170",
            "modify_time": "2019-12-14T17:16:02.911170",
            "group": 221,	// profile对应组的id，一般没用
            "parent_group": 238,	// 关联组id
            "creator": 1,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    {
        "id": 218,
        "name": "医生",
        "profile": null
    },
    ...
]
```

##### 失败时 400 404 403 401

### 为某个组添加用户

**POST** /api/groups/{pk}/users/

#### 请求参数

- pk：用户组id。

```json
{
    "user": 1	// 关联用户id
}
```

#### 返回参数

##### 成功时 200

##### 失败时 400 401 403 404

### 为某个用户添加所属组

**POST** /api/users/{pk}/groups/

#### 请求参数

- pk：用户id。

```json
{
    "group": 1	// 关联组id
}
```

#### 返回参数

##### 成功时 200

##### 失败时 400 401 403 404

## 职业相关

### 所有职业

**GET** /api/occupations/

#### 返回参数

##### 成功时 200

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

##### 失败时 401

### 创建职业

**POST** /api/occupations/

#### 请求参数

```json
{
    "name": "name"
}
```

#### 返回参数

##### 成功时 201

```json
{
    "id": 2,
    "name": "name"
}
```

##### 失败时 403 401 400

### 某个职业

**GET** /api/occupations/{pk}/

#### 请求参数

- pk：职业id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 1,
    "name": "name"
}
```

##### 失败时 404 401

### 更改某个职业

**PUT** /api/occupations/{pk}/

#### 请求参数

- pk：职业id。

```json
{
    "name": "name"
}
```

#### 返回参数

##### 成功时 201

```json
{
    "id": 2,
    "name": "name"
}
```

##### 失败时 404 401 403

### 删除某个职业

**DELETE** /api/occupations/{pk}/

#### 请求参数

- pk：职业id。

#### 返回参数

##### 204 404 401 403

### 某个职业下的所有用户

**GET** /api/occupations/{pk}/users/

#### 请求参数

- pk：职业id。

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
        "id": 7,
        "username": "test1",
        "email": "email1@test.com",
        "profile": {
            "name": "name",
            "name_pinyin": "name",
            "gender": 0,
            "identify_id": "100000190001010001",
            "phone": "18888888888",
            "address": "address1",
            "create_time": "2019-12-14T00:08:16.967537",
            "modify_time": "2019-12-14T00:08:16.967537",
            "user": 7,	// profile对应用户id，一般没用
            "occupation": 34,	// 关联职业id
            "creator": 7,	// 关联用户id
            "modifier": null	// 关联用户id
        }
    },
    ...
]
```

##### 失败时 400 401 403 404

## 黑名单

### 所有病人黑名单

**GET** /api/black-list/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "patient": 1,
        "join_time": xxxxxx,
        "is_delete": 0,
        "reason": "xxx"
    },
    ...
]
```

##### 失败时 401