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

### 某个用户下的所有处方签

**GET** /api/users/{pk}/prescriptions/

#### 请求参数

- pk：用户id。

如果对应用户是病人，则返回该病人所拥有的所有处方签；如果对应用户是医生，则返回该医生开出的所有处方签。

#### 响应参数

##### 成功时 200

与**所有处方签**返回格式相同。（可以为空，即`[]`，表示该用户下没有处方签）

##### 失败时 401 404

## 病历相关

### 创建病历

**POST** /api/medical-records/

#### 请求参数

```json
{
    "patient": 1,
    "department": 1,
    "onset_date": "2019-01-01",
    "diagnosis": "医生对病人的诊断",
    "detail": "医生对病情的详细描述", // 可不传入
    "patient_description": "病人自己的描述", // 可不传入
    "onset_history": "发病史", // 可不传入
    "medicine_history": "药物史" // 可不传入
}
```

#### 响应参数

##### 200 400 401

### 所有病历

**GET** /api/medical-records/

#### 响应参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "onset_date": "2019-01-01",	// 发病日期
        "diagnosis": "医生对病人的诊断",
        "detail": "医生对病情的详细描述",
        "patient_description": "病人自己的描述",
        "onset_history": "发病史",
        "time": "2019-12-16T20:56:10.587306",	// 就诊时间，由系统添加
        "medicine_history": "药物史",
        "can_modify": true,	// 是否可以编辑
        "create_time": "2019-12-16T20:56:10.684305",
        "modify_time": "2019-12-16T20:56:10.684305",
        "patient": 14,	// 病人id
        "department": 233,	// 科室id
        "creator": 19,	// 创建者（一般为医生）id
        "modifier": null	// 修改者（一般为医生）id
    },
    ...
]
```

##### 失败时 401

### 某条病历

**GET** /api/medical-records/{pk}/

#### 请求参数

- pk：病历id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 1,
    "onset_date": "2019-01-01",	// 发病日期
    "diagnosis": "医生对病人的诊断",
    "detail": "医生对病情的详细描述",
    "patient_description": "病人自己的描述",
    "onset_history": "发病史",
    "time": "2019-12-16T20:56:10.587306",	// 就诊时间，由系统添加
    "medicine_history": "药物史",
    "can_modify": true,	// 是否可以编辑
    "create_time": "2019-12-16T20:56:10.684305",
    "modify_time": "2019-12-16T20:56:10.684305",
    "patient": 14,	// 病人id
    "department": 233,	// 科室id
    "creator": 19,	// 创建者（一般为医生）id
    "modifier": null	// 修改者（一般为医生）id
}
```

##### 失败时 401 404

### 更新某条病历

**PUT** /api/medical-records/{pk}/

#### 请求参数

- pk：病历id。

以下所有参数均可不传入。

```json
{
    "onset_date": "2019-01-01",
    "diagnosis": "医生对病人的诊断",
    "detail": "医生对病情的详细描述",
    "patient_description": "病人自己的描述",
    "onset_history": "发病史",
    "medicine_history": "药物史",
    "can_modify": 0
}
```

#### 响应参数

##### 200 400 401 404

### 某个用户下的所有病历

**GET** /api/users/{pk}/medical-records/

#### 请求参数

- pk：用户id。

#### 响应参数

##### 成功时 200

与**所有病历**响应参数相同。

##### 失败时 400 401 404