# cap faiss
- 1 概述
- 2 部署
- 参考

# 1 概述
分布式实时Faiss召回系统

![架构](https://github.com/WallaceLiu/distributed-realtime-capfaiss/blob/main/doc/image/%E5%88%86%E5%B8%83%E5%BC%8F%E5%AE%9E%E6%97%B6Faiss%E6%B5%81%E7%A8%8B%E5%9B%BE.png?raw=true)

# 2 grpc
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ compute.proto
```
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```

# 2 sure部署
具体参考 [部署](doc/02.部署.md)

# 参考