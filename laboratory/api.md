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