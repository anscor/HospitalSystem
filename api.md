## 总述

### 接口权限验证

管理员拥有所有接口访问权限。在接口说明不再单独说明。

以下列出所有API除用户登录、用户注册、刷新token外，其余接口均需以token方式进行登录验证。token提供方式如下：

```http
DELETE /api/users/8/ HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2MjkzMTQ4LCJqdGkiOiIyMGQxNzNiODA1NGE0NWU3OGRkYmY0NjBhNzAwNTg0MSIsInVzZXJfaWQiOjF9.COb9ts0SDLUCd9f46sUVKRtGLNep7EsFrvegja38Vuc
```

如果未提供token或token过期、不合法等，会得到401响应，返回如下信息：

```json
"token过期、不合法": {
    "detail": "Given token not valpk for any token type",
    "code": "token_not_valpk",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalpk or expired"
        }
    ]
},
"未提供token": {
    "detail": "身份认证信息未提供。"
}
```

### 请求、返回参数说明

#### 请求参数

以列表形式给出时，表示此参数放在`URL`或请求头中，以`json`形式给出时表示此参数放在请求体当中，没有说明时表示没有任何请求参数。

#### 返回参数

默认返回参数如下：

```json
{
    "detail": "返回信息！"
}
```

返回状态用加粗数字表示，如未对参数进行说明，则表示为默认格式。

### 各方法返回状态码说明

- POST：成功返回201，并返回创建的内容。
- GET：成功返回200，并返回相应内容。
- PUT：成功返回200，并返回修改后的内容。不允许更改时返回405。
- DELETE：成功返回204，没有任何其他数据返回。不允许删除时返回405。

## 用户模块

| 请求方法 | 地址                         | 说明                                         |
| :------- | :--------------------------- | :------------------------------------------- |
| POST     | /api/auth/                   | 用户登录（完成）                             |
| GET      | /api/auth/user/              | 通过token获取用户信息（完成）                |
| POST     | /api/auth/refresh/           | 刷新token（完成）                            |
| GET      | /api/auth/logout/            | 用户登出（完成）                             |
| POST     | /api/users/                  | 用户注册（完成）                             |
| GET      | /api/users/                  | 所有用户信息（管理员可用）（完成）           |
| GET      | /api/users/{pk}/             | 某个用户信息（本人可用）（完成）             |
| DELETE   | /api/users/{pk}/             | 删除某个用户（管理员可用）（完成）           |
| PUT      | /api/users/{pk}/             | 更新某个用户信息（本人可用）（完成）         |
| GET      | /api/groups/                 | 所有组信息（完成）                           |
| POST     | /api/groups/                 | 添加组（管理员可用）（完成）                 |
| GET      | /api/departments/            | 所有可预约的科室信息（完成）                 |
| GET      | /api/groups/?name=           | 某个组信息（完成）                           |
| GET      | /api/groups/{pk}/            | 某个组信息（完成）                           |
| PUT      | /api/groups/{pk}/            | 修改某个组信息（管理员可用）（完成）         |
| DELETE   | /api/groups/{pk}/            | 删除某个组（管理员可用）（完成）             |
| GET      | /api/groups/{pk}/users/      | 某个组下的所有用户信息（管理员可用）（完成） |
| GET      | /api/users/{pk}/groups/      | 某个用户所属的所有组（完成）                 |
| POST     | /api/groups/{pk}/users/      | 为某个组添加用户（管理员可用）（完成）       |
| POST     | /api/users/{pk}/groups/      | 为某个用户添加所属组（管理员可用）（完成）   |
| GET      | /api/occupations/            | 所有职业信息（完成）                         |
| POST     | /api/occupations/            | 创建职业信息（完成）                         |
| GET      | /api/occupations/{pk}/       | 某个职业的信息（完成）                       |
| PUT      | /api/occupations/{pk}/       | 更改某个职业的信息（管理员可用）（完成）     |
| DELETE   | /api/occupations/{pk}/       | 删除某个职业（管理员可用）（完成）           |
| GET      | /api/occupations/{pk}/users/ | 某个职业下的所有用户（管理员可用）（完成）   |
| GET      | /api/black-list/             | 病人黑名单（完成）                           |

## 门诊模块

| 请求方法 | 地址                             | 说明                           |
| -------- | -------------------------------- | ------------------------------ |
| GET      | /api/medical-records/            | 所有病历（完成）               |
| POST     | /api/medical-records/            | 创建病历（完成）               |
| PUT      | /api/medical-records/{pk}/       | 更新某条病历（完成）           |
| GET      | /api/medical-records/{pk}/       | 某条病历（完成）               |
| GET      | /api/users/{pk}/medical-records/ | 某个用户下的所有病历（完成）   |
| GET      | /api/prescriptions/              | 所有处方签（完成）             |
| POST     | /api/prescriptions/              | 添加处方签（完成）             |
| GET      | /api/prescriptions/{pk}/         | 某条处方签（完成）             |
| GET      | /api/users/{pk}/prescriptions/   | 某个用户下的所有处方签（完成） |

## 财务模块

| 请求方法 | 地址                             | 说明                                         |
| -------- | -------------------------------- | -------------------------------------------- |
| GET      | /api/pay-records/                | 所有缴费记录（完成）                         |
| POST     | /api/pay-records/                | 创建缴费记录（完成）                         |
| GET      | /api/pay-records/{pk}/           | 某条缴费记录（完成）                         |
| PUT      | /api/pay-records/{pk}/           | 更新某条缴费记录（主要用于实现缴费）（完成） |
| GET      | /api/pay-types/                  | 所有缴费类型（完成）                         |
| POST     | /api/pay-types/                  | 添加缴费类型（完成）                         |
| GET      | /api/pay-types/{pk}/             | 某种缴费类型（完成）                         |
| PUT      | /api/pay-types/{pk}/             | 修改某种缴费类型（完成）                     |
| DELETE   | /api/pay-types/{pk}/             | 删除某种缴费类型（管理员可用）（完成）       |
| GET      | /api/pay-types/{pk}/pay-records/ | 某种缴费类型下的所有缴费记录（完成）         |
| GET      | /api/users/{pk}/pay-records/     | 某个用户下的所有缴费记录                     |
| GET      | /api/refund-records/             | 所有退款记录                                 |
| POST     | /api/refund-records/             | 创建退款记录                                 |
| GET      | /api/refund-records/{pk}/        | 某条退款记录                                 |
| GET      | /api/users/{pk}/refund-records/  | 某个用户下的所有退款记录                     |
| GET      | /api/audit-records/              | 所有结算记录                                 |
| POST     | /api/audit-records/              | 创建结算记录                                 |
| GET      | /api/audit-records/{pk}/         | 某条结算记录                                 |
| PUT      | /api/audit-records/{pk}/         | 更新某条结算记录                             |
| PATCH    | /api/audit-records/{pk}/         | 更新某条结算记录                             |
| GET      | /api/users/{pk}/audit-records/   | 某个用户下的所有结算记录                     |

## 化验模块

| 请求方法 | 地址                                     | 说明                                   |
| :------- | ---------------------------------------- | -------------------------------------- |
| GET      | /api/laboratories/                       | 所有化验单（完成）                     |
| POST     | /api/laboratories/                       | 添加化验单（完成）                     |
| GET      | /api/laboratories/{pk}/                  | 某条化验单（完成）                     |
| GET      | /api/users/{pk}/laboratories/            | 某个用户下的所有化验单（完成）         |
| GET      | /api/laboratory-types/                   | 所有化验类型（完成）                   |
| POST     | /api/laboratory-types/                   | 添加化验类型（管理员可用）（完成）     |
| GET      | /api/laboratory-types/{pk}/              | 某个化验类型（完成）                   |
| DELETE   | /api/laboratory-types/{pk}/              | 删除某个化验类型（管理员可用）（完成） |
| GET      | /api/laboratory-types/{pk}/laboratories/ | 某个化验类型下的所有化验单（完成）     |

## 药房模块

| 请求方法 | 地址                                | 说明                                   |
| -------- | ----------------------------------- | -------------------------------------- |
| GET      | /api/medicine-types/                | 所有药物类型（完成）                   |
| POST     | /api/medicine-types/                | 添加药物类型（完成）                   |
| GET      | /api/medicine-types/{pk}/           | 某种药物类型（完成）                   |
| PUT      | /api/medicine-types/{pk}/           | 更改某种药物类型（完成）               |
| DELETE   | /api/medicine-types/{pk}/           | 删除某种药物类型（管理员可用）（完成） |
| GET      | /api/medicine-types/{pk}/medicine/  | 某种药物类型下的所有药物（完成）       |
| GET      | /api/medicine/                      | 所有药物（完成）                       |
| POST     | /api/medicine/                      | 添加药物（完成）                       |
| GET      | /api/medicine/{pk}/                 | 某种药物（完成）                       |
| PUT      | /api/medicine/{pk}/                 | 修改某种药物（完成）                   |
| DELETE   | /api/medicine/{pk}/                 | 删除某种药物（管理员可用）（完成）     |
| GET      | /api/medicine-handout-records/      | 所有药物发放记录                       |
| POST     | /api/medicine-handout-records/      | 添加药物发放记录                       |
| GET      | /api/medicine-handout-records/{pk}/ | 某条药物发放记录                       |

## 预约模块

| 请求方法 | 地址                                     | 说明                                                   |
| -------- | ---------------------------------------- | ------------------------------------------------------ |
| GET      | /api/reservations/                       | 所有预约记录（管理员可用）（完成）                     |
| POST     | /api/reservations/                       | 添加预约记录（病人可用）（完成）                       |
| GET      | /api/reservations/{pk}/                  | 某条预约记录（完成）                                   |
| PUT      | /api/reservations/{pk}/                  | 更新某条预约记录（仅完成了取消预约，其他更改不会生效） |
| DELETE   | /api/reservations/{pk}/                  | 删除某条预约记录（管理员可用）（完成）                 |
| GET      | /api/users/{pk}/reservations/            | 某个用户下的所有预约记录（完成）                       |
| GET      | /api/groups/{pk}/reservations/           | 某个科室下的所有预约记录（完成）                       |
| GET      | /api/reservation-time/                   | 所有预约时间段（完成）                                 |
| POST     | /api/reservation-time/                   | 添加预约时间段（管理员可用）（完成）                   |
| GET      | /api/reservation-time/{pk}/              | 某个预约时间段（完成）                                 |
| PUT      | /api/reservation-time/{pk}/              | 更新某个预约时间段（管理员可用）（完成）               |
| DELETE   | /api/reservation-time/{pk}/              | 删除某个预约时间段（管理员可用）（完成）               |
| GET      | /api/reservation-time/{pk}/reservations/ | 某个预约时间段下的所有预约记录（管理员可用）（完成）   |
| GET      | /api/visits/                             | 所有坐诊时间记录（完成）                               |
| POST     | /api/visits/                             | 创建坐诊时间记录（专家医生可用）（完成）               |
| GET      | /api/visits/{pk}/                        | 某个坐诊时间记录（完成）                               |
| PUT      | /api/visits/{pk}/                        | 更新某个坐诊时间记录（专家医生可用）（完成）           |
| DELETE   | /api/visits/{pk}/                        | 删除某个坐诊时间记录（专家医生可用）（完成）           |
| GET      | /api/users/{pk}/visits/                  | 某个用户下的所有坐诊时间记录（完成）                   |