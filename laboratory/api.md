## 化验类型相关

### 添加化验类型

**POST** /api/laboratory-types/

#### 请求参数

```json
{
	"name": "化验项目3",
	"price": 350
}
```

#### 响应参数

##### 201 400 401 403

### 所有化验类型

**GET** /api/laboratory-types/

#### 响应参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "name": "化验项目1",
        "price": 100,
        "create_time": "2019-12-16T23:14:55.432949",
        "creator": 1
    },
    ...
]
```

##### 失败时 401

### 某个化验类型

**GET** /api/laboratory-types/{pk}/

#### 请求参数

- pk：化验类型id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 1,
    "name": "化验项目1",
    "price": 100,
    "create_time": "2019-12-16T23:14:55.432949",
    "creator": 1
}
```

##### 失败时 400 401 404

### 删除某个化验类型

**DELETE** /api/laboratory-types/{pk}/

#### 请求参数

- pk：化验类型id。

#### 响应参数

##### 204 401 403 404

### 某个化验类型下的所有化验单

**GET** /api/laboratory-types/{pk}/laboratories/

#### 请求参数

- pk：化验类型id。

#### 响应参数

##### 成功时 200

```json

```

##### 失败时 400 401 404

## 化验单相关

### 添加化验单

**POST** /api/laboratories/

#### 请求参数

```json
{
    "patient": 1,	// 病人id
    "executor": 1,	// 执行此检查的科室id
    "items": [{
        "laboratory_type": 1,	// 检查类型id
        "commet": "注意事项",	// 可不传入
        "check_part": "检查部位"	// 可不传入
    },
    ...
    ]
}
```

#### 响应参数

##### 201 400 401

### 所有化验单

**GET** /api/laboratories/

#### 响应参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "create_time": "2019-12-17T14:32:57.436552",
        "patient": 14,
        "executor": 222,
        "creator": 1,
        "items": [
            {
                "id": 1,
                "commet": "注意事项",
                "check_part": "检查部位",
                "laboratory": 1,
                "laboratory_type": 1
            },
            ...
        ]
    },
    ...
]
```

##### 失败时 401

### 某条化验单

**GET** /api/laboratories/{pk}/

#### 请求参数

- pk：化验单id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 1,
    "create_time": "2019-12-17T14:32:57.436552",
    "patient": 14,
    "executor": 222,
    "creator": 1,
    "items": [
        {
            "id": 1,
            "commet": "注意事项",
            "check_part": "检查部位",
            "laboratory": 1,
            "laboratory_type": 1
        },
        ...
    ]
}
```

##### 失败时 401 404

### 某个用户下的所有化验单

**GET** /api/users/{pk}/laboratories/

#### 请求参数

- pk：用户id。

#### 响应参数

##### 成功时 200

与**所有化验单**响应参数格式相同。

##### 失败时 400 401 404（用户）