## 缴费类型相关

### 所有缴费类型

**GET** /api/pay-types/

#### 响应参数

```json
[
    {
        "id": 1,
        "name": "专家号挂号费用",
        "price": 100,	// 此类缴费金额，某些特殊缴费类型（如药物费用）此字段无效，金额单独计算
        "create_time": "2019-12-15T23:23:21.199801",
        "modify_time": "2019-12-15T23:23:21.199801",
        "creator": 19,
        "modifier": null
    },
    ...
]
```

### 添加缴费类型

**POST** /api/pay-types/

#### 请求参数

```json
{
	"name": "药物费用",
	"price": 0	// 此类缴费金额，某些特殊缴费类型（如药物费用）此字段无效，金额单独计算
}
```

#### 响应参数

##### 200 400 401

### 某种缴费类型

**GET** /api/pay-types/{pk}/

#### 请求参数

- pk：缴费类型id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 1,
    "name": "专家号挂号费用",
    "price": 100,	// 此类缴费金额，某些特殊缴费类型（如药物费用）此字段无效，金额单独计算
    "create_time": "2019-12-15T23:23:21.199801",
    "modify_time": "2019-12-15T23:23:21.199801",
    "creator": 19,
    "modifier": null
}
```

##### 失败时 401 404

### 修改某种缴费类型

### 删除某种缴费类型

#### 请求参数

- pk：缴费类型id。

#### 响应参数

##### 204 401 403 404

### 某种缴费类型下的所有缴费记录

## 缴费记录相关

### 创建缴费记录

**POST** /api/pay-records/

#### 请求参数

```json
{
    "type": 1,	// 缴费类型id，关联缴费类型
    "id": 1		// 相关类型的id，如type为处方签，则此处代表的是处方签的id
}
```

#### 响应参数

##### 200 400 401

## 退款记录相关

## 结算相关