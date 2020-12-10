# API 接口
- 1, meta
- 2, search
- 3, add
- 4, del
- 5, reindex

# 1, meta
```text
GET /rc/meta
```

## 请求
变量|数据类型|说明
---|---|---
rcId|整型|可选

## 响应
变量|数据类型|说明
---|---|---
code|整型|200为成功
msg|字符串|-
data|-|-
```text
{'code': 200, 'msg': '', 'data': None}
```

## 示例
```text
curl http://localhost:8088/rc/meta
```

# 2, search
```text
POST /rc/search
```

## 请求
变量|数据类型|说明
---|---|---
rcId|字符串|必须
ids|字符串数组|必须，即user pin或itemid
vectors|二维float数组|必须，user pin的Embedding，或item的Embedding

### 示例
```shell script
curl http://localhost:8088/rc/search -X POST -H 'content-type:application/json;charset=UTF-8' -d '{"rcId": "101001101", "ids": ["u0"], "vectors": [[0.19151945412158966, 0.6221087574958801, 0.43772774934768677, ...]]}'
```

## 响应
变量|数据类型|说明
---|---|---
code|整型|200为成功
msg|字符串|-
data|字符串数组|data[0]为itemId数组，data[1]为距离数组

```text
{"code": 200, "msg": "SUCCESS", "data": ["[\"u3888\", \"u1812\", \"u1740\", ...]", "[32.10783, 31.997517, 31.576712, ...]"]}
```

# 3, add
```text
POST /rc/add
```

## 请求
变量|数据类型|说明
---|---|---
rcId|字符串|必须
ids|字符串数组|必须，即items数组
vectors|二维float数组|必须，矩阵

### 示例
```shell script
curl http://localhost:8088/rc/add -X POST -H 'content-type:application/json;charset=UTF-8' -d '{"cId": "101001101", "ids": ["u2001", "u2002", "u2003", ...], "vectors": [[0.36197173595428467, 0.9844337701797485, 0.8691965937614441, ...], [0.5464071035385132, 0.024673691019415855, 0.26135924458503723, ...], [0.8118161559104919, 0.487284392118454, 0.2417929768562317, 0.45961591601371765, ...], ...]]}'
```

## 响应
变量|数据类型|说明
---|---|---
code|字符串|200为成功
msg|字符串|-
data|字符串|各个节点的执行结果，不用解析

```text
{"code": 200, "msg": "SUCCESS", "data": "..."}
```

# 4, delete
```text
POST /rc/del
```

## 请求
变量|数据类型|说明
---|---|---
rcId|字符串|必须
ids|一维字符串数组|必须，即items

### 示例
```shell script
curl http://localhost:8088/rc/del -X POST -H 'content-type:application/json;charset=UTF-8' -d '{"rcId": "101001101", "ids": ["u1","u2","u3", ...]
```

## 响应
变量|数据类型|说明
---|---|---
code|字符串|200为成功
msg|字符串|-
data|字符串|各个节点的执行结果，不用解析

```text
{'code': 200, 'msg': '', 'data': "..."]}
```

# 5, reindex
```text
POST /rc/reindex
```

## 请求
变量|数据类型|说明
---|---|---
rcId|整型|必须
ids|一维字符串数组|必须，即items
vectors|二维数组|必须，矩阵

### 示例
```shell script
curl http://localhost:8088/rc/reindex -X POST -H 'content-type:application/json;charset=UTF-8' -d '{"rcId": "101001101", "ids": ["u1","u2","u3", ...],
    "vectors": [[0.36197173595428467, 0.9844337701797485, 0.8691965937614441, ...], [0.5464071035385132, 0.024673691019415855, 0.26135924458503723, ...], [0.8118161559104919, 0.487284392118454, 0.2417929768562317, 0.45961591601371765, ...], ...]]}'
```

## 响应
变量|数据类型|说明
---|---|---
code|整型|200为成功
msg|字符串|-
data|字符串|各个节点的执行结果，不用解析
```text
{'code': 200, 'msg': '', 'data': "..."}
```

