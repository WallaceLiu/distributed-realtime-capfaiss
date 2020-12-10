# 分布式实时Faiss召回
- 1, 概述
- 2, 部署
- 3, 压测
- 参考

# 1, 概述
分布式实时Faiss召回系统

# 2, grpc
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ compute.proto
```
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```
# 3, 部署
具体参考 [部署](doc/02.部署.md)
# 4, 压测
具体参考 [压测](doc/03.压测.md)
# 参考