## 排队相关

### 将病人加入到排队队列中

**POST** /api/wait-queue/

#### 请求参数

```json
{
    "patient": 1,		// 病人id
    "department": 1,	// 科室id
    "doctor": 1,		// 医生id
    "pay": 1,			// 缴费单id
    "reservation": 1	// 预约id
}
```

其中当传入`reservation`时，其他参数无效，也均可不传入；当不传入`reservation`时，`patient`，`department`，`pay`三个参数必须传入，`doctor`只有在现场挂专家号时才会传入。

#### 返回参数

##### 200 400

### 获取排队情况

**GET** /api/wait-queue/\[?top=]\[?doctor=][?department=]

#### 请求参数

- top：此参数值只能为1。
- doctor：医生id。（用于获取某个专家医生下在排队的病人信息）
- department：科室id。（用于获取某个科室下在排队的病人信息）

传入`top`时`doctor`和`department`必须传入其中一个；不传入`top`时，`doctor`和`department`可以均不传入，也可传入其中一个，但不能两个都传入。

传入`top`时表示取出某个医生或科室第一个病人去就诊（此时会将此病人出队），不传入`top`时表示查看某个医生或某个科室下所有在排队的病人信息（主要用于向病人展示排队状态）。

均不传入时表示查看所有的排队信息。

#### 返回参数

##### 成功时 200

传入`top`时，返回一个病人信息：

```json
{
    "id": 14,
    "username": "test6",
    "email": "email6@test.com",
    "profile": {
        "name": "test6",
        "name_pinyin": "test6",
        "gender": 0,
        "identify_id": "100000190001010006",
        "phone": "18888888886",
        "address": "address6",
        "create_time": "2019-12-14T21:11:55.225293",
        "modify_time": "2019-12-14T21:11:55.226335",
        "user": 14,
        "occupation": 34,
        "creator": 14,
        "modifier": null
    }
}
```

不传入`top`时，返回某个医生或科室下的所有排队病人信息：

```json
{
    "department": {
        "232": [
            {
                "id": 14,
                "username": "test6",
                "email": "email6@test.com",
                "profile": {
                    "name": "test6",
                    "name_pinyin": "test6",
                    "gender": 0,
                    "identify_id": "100000190001010006",
                    "phone": "18888888886",
                    "address": "address6",
                    "create_time": "2019-12-14T21:11:55.225293",
                    "modify_time": "2019-12-14T21:11:55.226335",
                    "user": 14,
                    "occupation": 34,
                    "creator": 14,
                    "modifier": null
                }
            },
            ...
        ],
        ...
    }
}
或
{
    "doctor": {
        "19": [
            {
                "id": 14,
                "username": "test6",
                "email": "email6@test.com",
                "profile": {
                    "name": "test6",
                    "name_pinyin": "test6",
                    "gender": 0,
                    "identify_id": "100000190001010006",
                    "phone": "18888888886",
                    "address": "address6",
                    "create_time": "2019-12-14T21:11:55.225293",
                    "modify_time": "2019-12-14T21:11:55.226335",
                    "user": 14,
                    "occupation": 34,
                    "creator": 14,
                    "modifier": null
                }
            },
            ...
        ],
        ...
    }
}
```

三者都不传入时：

```json
{
    "doctor": {
        "19": [
            {
                "id": 14,
                "username": "test6",
                "email": "email6@test.com",
                "profile": {
                    "name": "test6",
                    "name_pinyin": "test6",
                    "gender": 0,
                    "identify_id": "100000190001010006",
                    "phone": "18888888886",
                    "address": "address6",
                    "create_time": "2019-12-14T21:11:55.225293",
                    "modify_time": "2019-12-14T21:11:55.226335",
                    "user": 14,
                    "occupation": 34,
                    "creator": 14,
                    "modifier": null
                }
            },
            ...
        ],
        ...
    },
    "department": {
        "232": [
            {
                "id": 14,
                "username": "test6",
                "email": "email6@test.com",
                "profile": {
                    "name": "test6",
                    "name_pinyin": "test6",
                    "gender": 0,
                    "identify_id": "100000190001010006",
                    "phone": "18888888886",
                    "address": "address6",
                    "create_time": "2019-12-14T21:11:55.225293",
                    "modify_time": "2019-12-14T21:11:55.226335",
                    "user": 14,
                    "occupation": 34,
                    "creator": 14,
                    "modifier": null
                }
            },
            ...
        ],
        ...
    }
}
```

##### 失败时 400 401