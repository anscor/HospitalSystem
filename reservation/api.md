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
        "patient_num": 30,
        "reserved_num": 1
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
    "patient_num": 30
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
    "patient_num": 30,
    "reserved_num": 1
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
    "patient_num": 30
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
        "patient_num": 150,
        "room": "A栋404",
        "doctor": 19
    },
    {
        "id": 2,
        "date": "2019-01-01",
        "start": "08:30:00",
        "end": "17:30:00",
        "patient_num": 150,
        "room": "A栋404",
        "doctor": 19
    }
]
```

##### 失败时 400 401

### 创建坐诊时间记录

**POST** /api/visits/

#### 请求参数

```json
{
	"doctor": 20, // 如果是管理员创建，此字段必须传入；如果是专家医生，则可以不传入，传入也不使用
	"date": "2019-01-01",
	"start": "08:30",
	"end": "17:30",
	"patient_num": 150,
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
    "patient_num": 150,
    "room": "A栋404",
    "doctor": 19
}
```

##### 失败时 400 401 404

### 更新某个坐诊时间记录

**PUT** /api/visits/{pk}/

#### 请求参数

- pk：坐诊时间id。

```json
{
	"doctor": 20,	// 如果不是管理员，这个字段不能传入（传入也不会生效）
	"date": "2019-01-01",
	"start": "08:30",
	"end": "17:30",
	"patient_num": 150,
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
        "patient_num": 150,
        "room": "A栋404",
        "doctor": 19
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
        "id": 1,
        "date": "2019-01-01",
        "is_cancel": false,
        "is_expert": true,
        "patient": 14,
        "department": 232,
        "time": 2,
        "doctor": 19
    },
    {
        "id": 2,
        "date": "2019-01-01",
        "is_cancel": false,
        "is_expert": false,
        "patient": 14,
        "department": 232,
        "time": 3,
        "doctor": null
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
    "department": 232,
    "time": 2,
    "doctor": 19	// 可选，传入时表示预约的是专家号
}
```

#### 返回参数

##### 200 400 401 403

### 某条预约记录

**GET** /api/reservations/{pk}/

#### 请求参数

- pk：预约id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 1,
    "date": "2019-01-01",
    "is_cancel": false,
    "is_expert": true,
    "patient": 14,
    "department": 232,
    "time": 2,
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

##### 失败时 400 401 403 404

### 某个科室下的所有预约记录

**GET** /api/groups/{pk}/reservations/

#### 请求参数

- pk：科室id。

#### 返回参数

##### 成功时 200

##### 失败时 400 401 403 404