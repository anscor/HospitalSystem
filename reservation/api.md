## 预约时间段相关

### 所有预约时间段

**GET** /api/reservation-time/

#### 响应参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "start": "08:30:00",
        "end": "09:00:00",
        "patient_num": 30,	// 可预约的最大人数
        "reserved_num": 1	// 已经预约的人数
    },
    ...
]
```

##### 失败时 401

### 添加预约时间段

**POST** /api/reservation-time/

#### 请求参数

```json
{
    "start": "08:30",
    "end": "09:00",
    "patient_num": 30	// 可预约的最大人数
}
```

#### 响应参数

##### 200 400 401 403

### 某个预约时间段

**GET** /api/reservation-time/{pk}/

#### 请求参数

- pk：时间段id。

#### 响应参数

##### 成功时 200

```json
{
    "id": 1,
    "start": "08:30:00",
    "end": "09:00:00",
    "patient_num": 30,	// 可预约的最大人数
    "reserved_num": 1	// 已经预约的人数
}
```

##### 失败时 401 404

### 更新某个预约时间段

**PUT** /api/reservation-time/{pk}/

#### 请求参数

- pk：时间段id。

```json
{
    "start": "08:30",
    "end": "09:00",
    "patient_num": 30	// 可预约的最大人数
}
```

#### 响应参数

##### 200 400 401 403 404

### 删除某个预约时间段

**DELETE** /api/reservation-time/{pk}/

#### 请求参数

- pk：时间段id。

#### 响应参数

##### 200 401 403 404

### 某个预约时间段下的所有预约记录

**GET** /api/reservation-time/{pk}/reservations/

## 专家坐诊时间

### 所有坐诊时间记录

**GET** /api/visits/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "date": "2019-01-01",
        "start": "08:30:00",
        "end": "17:30:00",
        "patient_num": 150,	// 可预约的最大人数
        "room": "A栋404",
        "doctor": 19	// 医生id，关联专家医生
    },
    {
        "id": 2,
        "date": "2019-01-01",
        "start": "08:30:00",
        "end": "17:30:00",
        "patient_num": 150,	// 可预约的最大人数
        "room": "A栋404",
        "doctor": 19	// 医生id，关联专家医生用户id
    }
]
```

##### 失败时 400 401

### 创建坐诊时间记录

**POST** /api/visits/

#### 请求参数

```json
{
	"doctor": 20, // 医生id。如果是管理员创建，此字段必须传入；如果是专家医生，则可以不传入，传入也不使用
	"date": "2019-01-01",
	"start": "08:30",
	"end": "17:30",
	"patient_num": 150,	// 可预约的最大人数
	"room": "A栋404"	// 可选
}
```

#### 返回参数

##### 200 400 401 403

### 某个坐诊时间记录

**GET** /api/visits/{pk}/

#### 请求参数

- pk：坐诊时间id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 1,
    "date": "2019-01-01",
    "start": "08:30:00",
    "end": "17:30:00",
    "patient_num": 150,	// 可预约的最大人数
    "room": "A栋404",
    "doctor": 19	// 医生id，关联专家医生用户id
}
```

##### 失败时 400 401 404

### 更新某个坐诊时间记录

**PUT** /api/visits/{pk}/

#### 请求参数

- pk：坐诊时间id。

```json
{
	"doctor": 20,	// 医生id。如果不是管理员，这个字段不能传入（传入也不会生效）
	"date": "2019-01-01",
	"start": "08:30",
	"end": "17:30",
	"patient_num": 150,	// 可预约的最大人数
	"room": "A栋404"
}
```

#### 返回参数

##### 200 400 401 403 404

### 删除某个坐诊时间记录

**DELETE** /api/visits/{pk}/

#### 请求参数

- pk：坐诊时间id。

#### 返回参数

##### 成功时 204

这里没有返回任何数据。

##### 失败时 400 401 403 404

### 某个用户下的所有坐诊时间记录

**GET** /api/users/{pk}/visits/

#### 请求参数

- pk：用户id（此处应为专家医生）。

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "date": "2019-01-01",
        "start": "08:30:00",
        "end": "17:30:00",
        "patient_num": 150,	// 可预约的最大人数
        "room": "A栋404",
        "doctor": 19	// 医生id，关联专家医生用户id
    },
    ...
]
```

##### 失败时 400 401 404

## 预约相关

### 所有预约记录

**GET** /api/reservations/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 19,
        "date": "2019-01-01",
        "is_cancel": 0,
        "is_paid": 0,
        "is_finish": 0,
        "is_expert": 1,
        "patient": 14,
        "department": 232,
        "pay": {
            "id": 6,
            "receive": null,
            "refund": null,
            "method": 0,
            "create_time": "2019-12-17T16:18:03.897531",
            "modify_time": "2019-12-17T16:18:03.897531",
            "patient": 14,
            "pay_type": 2,
            "creator": 14,
            "modifier": null,
            "items": [
                {
                    "id": 5,
                    "name": "专家号费用",
                    "count": 1,
                    "price": 100,
                    "record": 6
                }
            ]
        },
        "time": 3,
        "doctor": 19
    },
    ...
]
```

##### 失败时 400 401

### 添加预约记录

**POST** /api/reservations/

#### 请求参数

```json
{
    "date": "2019-01-01",
    "patient": 14,	// 此参数如果为管理员创建则必须传入，如果不是则可以不传入（传入也不使用）
    "department": 232,	// 预约科室，关联可预约科室id
    "time": 2,	// 预约时间段，关联预约时间段id
    "doctor": 19	// 可选，传入时表示预约的是专家号
}
```

#### 返回参数

##### 成功时 201

```json
{
    "id": 19,
    "date": "2019-01-01",
    "is_cancel": 0,
    "is_paid": 0,
    "is_finish": 0,
    "is_expert": 1,
    "patient": 14,
    "department": 232,
    "pay": {
        "id": 6,
        "receive": null,
        "refund": null,
        "method": 0,
        "create_time": "2019-12-17T16:18:03.897531",
        "modify_time": "2019-12-17T16:18:03.897531",
        "patient": 14,
        "pay_type": 2,
        "creator": 14,
        "modifier": null,
        "items": [
            {
                "id": 5,
                "name": "专家号费用",
                "count": 1,
                "price": 100,
                "record": 6
            }
        ]
    },
    "time": 3,
    "doctor": 19
}
```

##### 失败时 400 401 403

### 某条预约记录

**GET** /api/reservations/{pk}/

#### 请求参数

- pk：预约id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 19,
    "date": "2019-01-01",
    "is_cancel": 0,
    "is_paid": 0,
    "is_finish": 0,
    "is_expert": 1,
    "patient": 14,
    "department": 232,
    "pay": {
        "id": 6,
        "receive": null,
        "refund": null,
        "method": 0,
        "create_time": "2019-12-17T16:18:03.897531",
        "modify_time": "2019-12-17T16:18:03.897531",
        "patient": 14,
        "pay_type": 2,
        "creator": 14,
        "modifier": null,
        "items": [
            {
                "id": 5,
                "name": "专家号费用",
                "count": 1,
                "price": 100,
                "record": 6
            }
        ]
    },
    "time": 3,
    "doctor": 19
}
```

##### 失败时 400 401 403 404

### 更新某条预约记录

**PUT** /api/reservations/{pk}/

#### 请求参数

- pk：预约id。

#### 返回参数

##### 成功时 200

##### 失败时 400 401 403 404

### 删除某条预约记录

**DELETE** /api/reservations/{pk}/

#### 请求参数

- pk：预约id。

#### 返回参数

##### 成功时 200

##### 失败时 400 401 403 404

### 某个用户下的所有预约记录

**GET** /api/users/{pk}/reservations/

#### 请求参数

- pk：用户id。

#### 返回参数

##### 成功时 200

与**所有预约记录**返回参数格式相同。

##### 失败时 400 401 403 404

### 某个科室下的所有预约记录

**GET** /api/groups/{pk}/reservations/

#### 请求参数

- pk：科室id。

#### 返回参数

##### 成功时 200

与**所有预约记录**返回参数格式相同。

##### 失败时 400 401 403 404