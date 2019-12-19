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

**GET** /api/pay-types/{pk}/pay-records/

#### 请求参数

- pk：缴费类型id。

#### 返回参数

##### 成功时 200

与**所有缴费记录**返回参数相同。

##### 失败时 401 404

## 缴费记录相关

此处创建缴费记录只是在数据库中存储了相应的记录，但是并不进行划账。

也就是说，此处由收银员来进行POST，然后告知病人多少钱，病人把钱交给收银员后，收银员再通过PUT来修改缴费记录。

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

##### 成功时 201

```json
{
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
}
```

##### 失败时 400 401

### 更新某条缴费记录

**PUT** /api/pay-records/{pk}/

#### 请求参数

- pk：缴费记录id。

```json
{
    "receive": 1500,	// 收款金额
    "refund": 10.5,		// 找零金额，可不传入，不传入表示没有找零，系统默认添加0。
    "method": 1			// 付款方式（1：现金，2: 银联，3：支付宝，4：微信）
}
```

#### 返回参数

##### 200 400 401 404

### 所有缴费记录

**GET** /api/pay-records/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 6,
        "receive": null,
        "refund": null,
        "method": 0,	// 付款方式（1：现金，2: 银联，3：支付宝，4：微信）
        "create_time": "2019-12-17T16:18:03.897531",
        "modify_time": "2019-12-17T16:18:03.897531",
        "patient": 14,	// 病人id
        "pay_type": 2,	// 缴费类型
        "creator": 14,
        "modifier": null,
        "items": [
            {
                "id": 5,
                "name": "专家号费用",
                "count": 1,	// 数量
                "price": 100,	// 总价
                "record": 6	// 无用字段
            }
        ]
    },
    ...
]
```

##### 失败时 401

### 某条缴费记录

**GET** /api/pay-records/{pk}/

#### 请求参数

- pk：缴费单id。

#### 返回参数

##### 成功时 200

```json
{
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
}
```

##### 失败时 401 404

### 某个用户下的所有缴费记录

**GET** /api/users/{pk}/pay-records/

#### 请求参数

- pk：用户id。

#### 返回参数

##### 成功时 200

与**所有缴费记录**返回参数格式相同。

##### 失败时 401 404

## 退款记录相关

### 创建退款记录

**POST** /api/refund-records/

#### 请求参数

```json
{
    "pay": 11,				// 对应缴费单id
    "method": 3,			// 退款方式，与缴费方式相同对应
    "refund": 20,			// 退款金额
    "reason": "退款原因",	 // 退款原因，可不传入
    "items": [
        {
            "item": 10,		// 对应缴费项目id
            "refund": 20	// 退款金额
        },
        ...
    ]
}
```

#### 返回参数

##### 成功时 200

##### 失败时 400 401

### 所有退款记录

**GET** /api/refund-records/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "method": 3,
        "refund": 20,
        "reason": "退款原因",
        "create_time": "2019-12-18T23:56:45.147481",
        "pay": 11,
        "creator": 1,
        "items": [
            {
                "id": 1,
                "refund": 20,
                "record": 1,
                "item": 10
            },
            ...
        ]
    },
    ...
]
```

##### 失败时 400 401

### 某条退款记录

**GET** /api/refund-records/{pk}/

#### 请求参数

- pk：退款记录id。

#### 返回参数

##### 成功时 200

```json

{
    "id": 1,
    "method": 3,
    "refund": 20,
    "reason": "退款原因",
    "create_time": "2019-12-18T23:56:45.147481",
    "pay": 11,
    "creator": 1,
    "items": [
        {
            "id": 1,
            "refund": 20,
            "record": 1,
            "item": 10
        },
        ...
    ]
}
```

##### 失败时 400 401 404

### 某个用户下的所有退款记录

**GET** /api/users/{pk}/refund-records/\[?start=][?end=]

#### 请求参数

- pk：用户id。
- start：开始时间。格式形如：2019-01-01，可选。
- end：结束时间。格式形如：2019-01-01，可选。

#### 返回参数

##### 成功时 200

与**所有退款记录**返回参数格式相同。

##### 失败时 400 401 404

## 结算相关

### 创建结算记录

**POST** /api/audit-records/

#### 请求参数

```json
[
    {
        "receive": 1,	// 缴费单id，可不传入
        "refund": 1		// 退款单id，可不传入
    },
    ...
]
```

#### 返回参数

##### 200 400 401

### 所有结算记录

### 创建结算记录

**GET** /api/audit-records/

#### 返回参数

##### 成功时 200

```json
[
    {
        "id": 1,
        "result": null,
        "commet": null,
        "create_time": "2019-12-19T13:28:24.458948",
        "audit_time": "2019-12-19T13:28:24.458948",
        "applicant": 1,
        "auditor": null,
        "items": [
            {
                "id": 1,
                "audit": 1,
                "receive": 7,
                "refund": null
            },
            {
                "id": 2,
                "audit": 1,
                "receive": 11,
                "refund": 1
            },
            ...
        ]
    },
    ...
]
```

##### 失败时 401

### 某条结算记录

**GET** /api/audit-records/{pk}/

#### 请求参数

- pk：结算记录id。

#### 返回参数

##### 成功时 200

```json
{
    "id": 1,
    "result": null,
    "commet": null,
    "create_time": "2019-12-19T13:28:24.458948",
    "audit_time": "2019-12-19T13:28:24.458948",
    "applicant": 1,
    "auditor": null,
    "items": [
        {
            "id": 1,
            "audit": 1,
            "receive": 7,
            "refund": null
        },
        {
            "id": 2,
            "audit": 1,
            "receive": 11,
            "refund": 1
        },
        ...
    ]
}
```

##### 失败时 401 404

### 更新某条结算记录

**PUT** /api/audit-records/{pk}/

#### 请求参数

- pk：结算记录id。

```json
{
    "result": 1,	  // 可不传入，不传入时默认设置为1（审核通过）
    "commet": "备注"	// 可不传入
}
```

#### 返回参数

##### 200 401 404

### 某个用户下的所有结算记录

**GET** /api/users/{pk}/audit-records/\[?start=][?end=]

#### 请求参数

- pk：用户id。
- start：开始时间。格式形如：2019-01-01，可选。
- end：结束时间。格式形如：2019-01-01，可选。

#### 返回参数

##### 成功时 200

与**所有结算记录**返回参数格式相同。

##### 失败时 401 404