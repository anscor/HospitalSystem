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

##### 成功时 200

```json
[
    {
        "id": 1,
        "name": "药物1",
        "in_price": 0.5,	// 购进单价
        "price": 50,	// 售出单价
        "count": 10000,	// 库存数量
        "create_time": "2019-12-15T22:13:08.285874",
        "modify_time": "2019-12-15T22:13:08.285874",
        "medicine_type": 1,	// 药物类型，关联药物类型id
        "creator": 1,
        "modifier": null
    },
    ...
]
```

##### 失败时 400 401 404

## 药物相关

### 所有药物

**GET** /api/medicine/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "name": "药物1",
        "in_price": 0.5,	// 购进单价
        "price": 50,	// 售出单价
        "count": 10000,	// 库存数量
        "create_time": "2019-12-15T22:13:08.285874",
        "modify_time": "2019-12-15T22:13:08.285874",
        "medicine_type": 1,	// 药物类型，关联药物类型id
        "creator": 1,
        "modifier": null
    },
    ...
]
```

### 添加药物

**POST** /api/medicine/

#### 请求参数

```json
{
	"medicine_type": 1,	// 药物类型，关联药物类型id
	"name": "药物2",
	"in_price": 0.05,	// 购进单价
	"price": 500,	// 售出单价
	"count": 100	// 添加的此药物的数量
}
```

#### 返回参数

##### 200 400 401

### 某种药物

**GET** /api/medicine/{pk}/

#### 请求参数

- pk：药物id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 1,
    "name": "药物1",
    "in_price": 0.5,	// 购进单价
    "price": 50,	// 售出单价
    "count": 10000,	// 库存数量
    "create_time": "2019-12-15T22:13:08.285874",
    "modify_time": "2019-12-15T22:13:08.285874",
    "medicine_type": 1,	// 药物类型，关联药物类型id
    "creator": 1,
    "modifier": null
}
```

##### 失败时 400 401 404

### 修改某种药物

**PUT** /api/medicine/{pk}/

#### 请求参数

- pk：药物id。

```json
{
	"medicine_type": 1,	// 药物类型，关联药物类型id
	"name": "药物2",
	"in_price": 0.05,	// 购进单价
	"price": 500,	// 售出单价
	"count": 100	// 添加的此药物的数量
}
```

#### 返回参数

##### 200 400 401 404

### 删除某种药物

**DELETE** /api/medicine/{pk}/

#### 请求参数

- pk：药物id。

#### 返回参数

##### 204 401 403 404

## 药物发放相关

### 所有药物发放记录

**GET** /api/medicine-handout-records/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 3,
        "handout_status": false,	// 药物是否已经发放了
        "create_time": "2019-12-18T20:14:25.053914",
        "modify_time": "2019-12-18T20:19:21.570939",
        "prescription": {
            "id": 5,
            "is_paid": false,
            "create_time": "2019-12-18T20:14:24.483916",
            "modify_time": "2019-12-18T20:14:24.484917",
            "patient": 14,
            "pay": null,
            "creator": 19,
            "midifier": null,
            "items": [
                {
                    "id": 8,
                    "method": "药物用法",
                    "ratio": "3次/天",
                    "days": 7,
                    "commet": "其他注意事项",
                    "count": 10,
                    "count_unit": "总量单位",
                    "dosage": "1/3",
                    "dosage_unit": "用量单位",
                    "skin_test": null,
                    "prescription": 5,
                    "medicine": 1
                },
                {
                    "id": 9,
                    "method": "药物用法",
                    "ratio": "3次/天",
                    "days": 7,
                    "commet": "其他注意事项",
                    "count": 10,
                    "count_unit": "总量单位",
                    "dosage": "1/3",
                    "dosage_unit": "用量单位",
                    "skin_test": null,
                    "prescription": 5,
                    "medicine": 2
                }
            ]
        },
        "creator": 19,
        "modifier": null
    },
    ...
]
```

##### 失败时 401

### 某条药物发放记录

**GET** /api/medicine-handout-records/{pk}/

#### 请求参数

- pk：药物发放记录id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 3,
    "handout_status": false,	// 药物是否已经发放了
    "create_time": "2019-12-18T20:14:25.053914",
    "modify_time": "2019-12-18T20:19:21.570939",
    "prescription": {
        "id": 5,
        "is_paid": false,
        "create_time": "2019-12-18T20:14:24.483916",
        "modify_time": "2019-12-18T20:14:24.484917",
        "patient": 14,
        "pay": null,
        "creator": 19,
        "midifier": null,
        "items": [
            {
                "id": 8,
                "method": "药物用法",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "总量单位",
                "dosage": "1/3",
                "dosage_unit": "用量单位",
                "skin_test": null,
                "prescription": 5,
                "medicine": 1
            },
            {
                "id": 9,
                "method": "药物用法",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "总量单位",
                "dosage": "1/3",
                "dosage_unit": "用量单位",
                "skin_test": null,
                "prescription": 5,
                "medicine": 2
            }
        ]
    },
    "creator": 19,
    "modifier": null
}
```

##### 失败时 401 404

### 更新某条药物发放记录

**PUT** /api/medicine-handout-records/{pk}/

#### 请求参数

- pk：药物发放记录id。

```json
{
	"handout_status": 1
}
```

#### 返回参数

##### 成功时 200

```json
{
    "id": 3,
    "handout_status": true,	// 药物是否已经发放了
    "create_time": "2019-12-18T20:14:25.053914",
    "modify_time": "2019-12-18T20:19:21.570939",
    "prescription": {
        "id": 5,
        "is_paid": false,
        "create_time": "2019-12-18T20:14:24.483916",
        "modify_time": "2019-12-18T20:14:24.484917",
        "patient": 14,
        "pay": null,
        "creator": 19,
        "midifier": null,
        "items": [
            {
                "id": 8,
                "method": "药物用法",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "总量单位",
                "dosage": "1/3",
                "dosage_unit": "用量单位",
                "skin_test": null,
                "prescription": 5,
                "medicine": 1
            },
            {
                "id": 9,
                "method": "药物用法",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "总量单位",
                "dosage": "1/3",
                "dosage_unit": "用量单位",
                "skin_test": null,
                "prescription": 5,
                "medicine": 2
            }
        ]
    },
    "creator": 19,
    "modifier": null
}
```

##### 失败时 400 401 404