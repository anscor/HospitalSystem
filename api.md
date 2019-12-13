## 用户模块

| 请求方法 | 地址                         | 说明                       |
| :------- | :--------------------------- | :------------------------- |
| POST     | /api/auth/                   | 用户登录                   |
| POST     | /api/auth/refresh/           | 刷新token                  |
| GET      | /api/auth/logout/            | 用户登出                   |
| POST     | /api/users/                  | 用户注册                   |
| GET      | /api/users/                  | 所有用户信息               |
| GET      | /api/users/{id}/             | 某个用户信息               |
| GET      | /api/groups/                 | 所有组信息                 |
| POST     | /api/groups/                 | 添加组                     |
| GET      | /api/groups/{id}/            | 某个组信息                 |
| GET      | /api/groups/{id}/users/      | 某个组下的所有用户信息     |
| GET      | /api/users/{id}/groups/      | 某个用户所属的所有组       |
| POST     | /api/groups/{id}/users/      | 为某个组添加用户           |
| POST     | /api/users/{id}/groups/      | 为某个用户添加所属组       |
| GET      | /api/occupations/            | 所有职业信息               |
| POST     | /api/occupations/            | 创建职业信息               |
| GET      | /api/occupations/{id}/       | 某个职业的信息             |
| GET      | /api/occupations/{id}/users/ | 某个职业下的所有用户       |
| GET      | /api/user-logs/              | 所有登入登出记录           |
| GET      | /api/user-logs/{id}/         | 某条登入登出记录           |
| GET      | /api/users/{id}/user-logs/   | 某个用户的所有登入登出记录 |
| GET      | /api/black-list/             | 病人黑名单                 |

## 门诊模块

| 请求方法 | 地址                             | 说明                           |
| -------- | -------------------------------- | ------------------------------ |
| GET      | /api/medical-records/            | 所有病历（根据用户进行筛选）   |
| POST     | /api/medical-records/            | 创建病历                       |
| PUT      | /api/medical-records/{id}/       | 更新某条病历                   |
| GET      | /api/medical-records/{id}/       | 某条病历                       |
| PATCH    | /api/medical-records/{id}/       | 更新某条病历                   |
| GET      | /api/users/{id}/medical-records/ | 某个用户下的所有病历           |
| GET      | /api/prescriptions/              | 所有处方签（根据用户进行筛选） |
| POST     | /api/prescriptions/              | 添加处方签                     |
| GET      | /api/prescriptions/{id}/         | 某条处方签                     |
| GET      | /api/users/{id}/prescriptions/   | 某个用户下的所有处方签         |
| GET      | /api/prescriptions/{id}/items/   | 某条处方签中的所有项目         |
| POST     | /api/prescriptions/{id}/items/   | 为某条处方签的添加项目         |

## 财务模块

| 请求方法 | 地址                             | 说明                             |
| -------- | -------------------------------- | -------------------------------- |
| GET      | /api/pay-records/                | 所有缴费记录（根据用户进行筛选） |
| POST     | /api/pay-records/                | 创建缴费记录                     |
| GET      | /api/pay-records/{id}/           | 某条缴费记录                     |
| GET      | /api/pay-types/                  | 所有缴费类型                     |
| POST     | /api/pay-types/                  | 添加缴费类型                     |
| GET      | /api/pay-types/{id}/             | 某种缴费类型                     |
| GET      | /api/pay-types/{id}/pay-records/ | 某种缴费类型下的所有缴费记录     |
| GET      | /api/users/{id}/pay-records/     | 某个用户下的所有缴费记录         |
| GET      | /api/pay-records/{id}/items/     | 某条缴费记录下的所有项目         |
| POST     | /api/pay-records/{id}/items/     | 为某条缴费记录的添加项目         |
| GET      | /api/refund-records/             | 所有退款记录（根据用户进行筛选） |
| POST     | /api/refund-records/             | 创建退款记录                     |
| GET      | /api/refund-records/{id}/        | 某条退款记录                     |
| GET      | /api/users/{id}/refund-records/  | 某个用户下的所有退款记录         |
| GET      | /api/audit-records/              | 所有结算记录（根据用户进行筛选） |
| POST     | /api/audit-records/              | 创建结算记录                     |
| GET      | /api/audit-records/{id}/         | 某条结算记录                     |
| PUT      | /api/audit-records/{id}/         | 更新某条结算记录                 |
| PATCH    | /api/audit-records/{id}/         | 更新某条结算记录                 |
| GET      | /api/users/{id}/audit-records/   | 某个用户下的所有结算记录         |
| GET      | /api/audit-records/{id}/items/   | 某条结算记录下的所有项目         |
| POST     | /api/audit-records/{id}/items/   | 为某条结算记录的添加项目         |

## 化验模块

| 请求方法 | 地址                                     | 说明                       |
| :------- | ---------------------------------------- | -------------------------- |
| GET      | /api/laboratories/                       | 所有化验单                 |
| POST     | /api/laboratories/                       | 添加化验单                 |
| GET      | /api/laboratories/{id}/                  | 某条化验单                 |
| GET      | /api/users/{id}/laboratories/            | 某个用户下的所有化验单     |
| GET      | /api/laboratory-types/                   | 所有化验类型               |
| POST     | /api/laboratory-types/                   | 添加化验类型               |
| GET      | /api/laboratory-types/{id}/              | 某个化验类型               |
| GET      | /api/laboratory-types/{id}/laboratories/ | 某个化验类型下的所有化验单 |
| GET      | /api/laboratories/{id}/items/            | 某条化验单下的所有项目     |
| POST     | /api/laboratories/{id}/items/            | 为条化验单的添加项目       |

## 药房模块

| 请求方法 | 地址                                | 说明                     |
| -------- | ----------------------------------- | ------------------------ |
| GET      | /api/medicine-types/                | 所有药物类型             |
| POST     | /api/medicine-types/                | 添加药物类型             |
| GET      | /api/medicine-types/{id}/           | 某种药物类型             |
| GET      | /api/medicine-types/{id}/medicine/  | 某种药物类型下的所有药物 |
| GET      | /api/medicine/                      | 所有药物                 |
| POST     | /api/medicine/                      | 添加药物                 |
| GET      | /api/medicine/{id}/                 | 某种药物                 |
| GET      | /api/medicine-handout-records/      | 所有药物发放记录         |
| POST     | /api/medicine-handout-records/      | 添加药物发放记录         |
| GET      | /api/medicine-handout-records/{id}/ | 某条药物发放记录         |

## 预约模块

| 请求方法 | 地址                                      | 说明                           |
| -------- | ----------------------------------------- | ------------------------------ |
| GET      | /api/reservations/                        | 所有预约记录                   |
| POST     | /api/reservations/                        | 添加预约记录                   |
| GET      | /api/reservations/{id}/                   | 某条预约记录                   |
| PUT      | /api/reservations/{id}/                   | 更新某条预约记录               |
| PATCH    | /api/reservations/{id}/                   | 更新某条预约记录               |
| GET      | /api/users/{id}/reservations/             | 某个用户下的所有预约记录       |
| GET      | /api/groups/{id}/reservations/            | 某个科室下的所有预约记录       |
| GET      | /api/reservation-times/                   | 所有预约时间段                 |
| POST     | /api/reservation-times/                   | 添加预约时间段                 |
| GET      | /api/reservation-times/{id}/              | 某个预约时间段                 |
| GET      | /api/reservation-times/{id}/reservations/ | 某个预约时间段下的所有预约记录 |
| GET      | /api/visits/                              | 所有坐诊时间记录               |
| POST     | /api/visits/                              | 创建坐诊时间记录               |
| GET      | /api/visits/{id}/                         | 某个坐诊时间记录               |
| PUT      | /api/visits/{id}/                         | 更新某个坐诊时间记录           |
| PATCH    | /api/visits/{id}/                         | 更新某个坐诊时间记录           |
| GET      | /api/users/{id}/visits/                   | 某个用户下的所有坐诊时间记录   |