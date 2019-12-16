## 处方相关

### 添加处方签

**POST** /api/prescriptions/

#### 请求参数

```json
{
    "patient": 1,
    "items": [{
            "medicine": 1,
            "method": "药物用法",
            "ratio": "3次/天",
            "days": 7, //服用时长，可为空
            "commet": "其他注意事项",
            "count": 10, // 开出的药物总量
            "count_unit": "总量单位",
            "dosage": "1/3", // 每次用量
            "dosage_unit": "用量单位",
            "skin_test": "皮试结果" //可为空，为空表示没有进行皮试
        },
        ...
    ]
}
```

#### 返回参数

##### 200 400 401

### 所有处方签

**GET** /api/prescriptions/

#### 响应参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "is_paid": false,	// 是否已经缴费
        "create_time": "2019-12-16T16:39:26.071565",
        "modify_time": "2019-12-16T16:39:26.071565",
        "patient": 14,
        "creator": 19,
        "midifier": null,
        "items": [
            {
                "id": 1,
                "method": "温水送服",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "盒",
                "dosage": "1/3",
                "dosage_unit": "片",
                "skin_test": "正常",
                "prescription": 1,
                "medicine": 1
            }
        ]
    },
    {
        "id": 2,
        "is_paid": false,
        "create_time": "2019-12-16T16:41:03.393783",
        "modify_time": "2019-12-16T16:41:03.393783",
        "patient": 15,
        "creator": 19,
        "midifier": null,
        "items": [
            {
                "id": 2,
                "method": "温水送服",
                "ratio": "3次/天",
                "days": 7,
                "commet": "其他注意事项",
                "count": 10,
                "count_unit": "盒",
                "dosage": "1/3",
                "dosage_unit": "片",
                "skin_test": "正常",
                "prescription": 2,
                "medicine": 1
            },
            {
                "id": 3,
                "method": "温水送服",
                "ratio": "3次/天",
                "days": 15,
                "commet": "其他注意事项",
                "count": 5,
                "count_unit": "盒",
                "dosage": "15",
                "dosage_unit": "颗",
                "skin_test": null,
                "prescription": 2,
                "medicine": 2
            }
        ]
    }
]
```

##### 失败时 401

### 某条处方签

**GET** /api/prescriptions/{pk}/

#### 请求参数

- pk：处方签id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 2,
    "is_paid": false,
    "create_time": "2019-12-16T16:41:03.393783",
    "modify_time": "2019-12-16T16:41:03.393783",
    "patient": 15,
    "creator": 19,
    "midifier": null,
    "items": [
        {
            "id": 2,
            "method": "温水送服",
            "ratio": "3次/天",
            "days": 7,
            "commet": "其他注意事项",
            "count": 10,
            "count_unit": "盒",
            "dosage": "1/3",
            "dosage_unit": "片",
            "skin_test": "正常",
            "prescription": 2,
            "medicine": 1
        },
        {
            "id": 3,
            "method": "温水送服",
            "ratio": "3次/天",
            "days": 15,
            "commet": "其他注意事项",
            "count": 5,
            "count_unit": "盒",
            "dosage": "15",
            "dosage_unit": "颗",
            "skin_test": null,
            "prescription": 2,
            "medicine": 2
        }
    ]
}
```

##### 失败时 401 404

## 病历相关