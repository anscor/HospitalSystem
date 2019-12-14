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
        "patient_num": 30
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
    "patient_num": 30
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

