## 药物类型相关

### 所有药物类型

**GET** /api/medicine-types/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "name": "药物1",
        "create_time": "2019-12-15T21:36:11.899658",
        "modify_time": "2019-12-15T21:51:59.770788",
        "creator": 1,
        "modifier": 1
    },
    {
        "id": 2,
        "name": "药物2",
        "create_time": "2019-12-15T21:36:38.679841",
        "modify_time": "2019-12-15T21:52:08.159748",
        "creator": 1,
        "modifier": 1
    },
    ...
]
```

### 添加药物类型

**POST** /api/medicine-types/

#### 请求参数

```json
{
	"name": "药物3"
}
```

#### 返回参数

##### 成功时 200

##### 失败时 400 401

### 某种药物类型

**GET** /api/medicine-types/{pk}/

#### 请求参数

- pk：药物类型id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 2,
    "name": "药物2",
    "create_time": "2019-12-15T21:36:38.679841",
    "modify_time": "2019-12-15T21:52:08.159748",
    "creator": 1,
    "modifier": 1
}
```

##### 失败时 404

### 更新某种药物类型

**PUT** /api/medicine-types/{pk}/

#### 请求参数

- pk：药物类型id。

```json
{
	"name": "药物3"
}
```

#### 返回参数

##### 200 401 404

### 删除某种药物类型

**DELETE** /api/medicine-types/{pk}/

#### 请求参数

- pk：药物类型id。

#### 返回参数

##### 204 401 403 404

### 某种药物类型下的所有药物

**GET** /api/medicine-types/{pk}/medicine/

#### 请求参数

- pk：药物类型id。

#### 返回参数

## 药物相关

## 药物发放相关