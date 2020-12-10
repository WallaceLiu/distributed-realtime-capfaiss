# cap faiss
- 1 概述
- 2 部署
- 参考

# 1 概述
分布式实时Faiss召回系统

![架构](doc/image/arc.png?raw=true)

整个Faiss集群外部是四层均衡负载：

1. 实线，为核心流程，只能由Master节点完成向量索引的增加、删除，及与其他节点的索引同步，并返回给客户端索引更新的详细信息，包括集群每个节点IP、更新前后的向量数量等
2. 长划线，为集群选举Master节点
3. 点划线，为集群索引同步
4. 点虚线，若客户端请求到达的是Slave节点，则需要转发给Master节点，完成集群节点的更新 

> 若图片不能正常显示
> 配置hosts文件
> 151.101.76.133 raw.githubusercontent.com

# 2 grpc
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ compute.proto
```
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```

# 2 部署
具体参考 [部署](doc/02.部署.md)

# 参考