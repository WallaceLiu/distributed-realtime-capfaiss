# cap faiss
- 1 概述
- 2 工程结构
- 3 sure部署
- 4 压力测试
- 5 项目
- 参考

# 1 概述
分布式实时Faiss召回系统
![](doc/image/分布式实时Faiss流程图.png)
# 2 grpc
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ compute.proto
```
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```
具体参考 [工程结构](doc/01.工程结构.md)
# 3 sure部署
具体参考 [sure部署](doc/03.sure部署.md)
# 4 压力测试
具体参考 [压力测试](doc/04.压力测试.md)
# 参考