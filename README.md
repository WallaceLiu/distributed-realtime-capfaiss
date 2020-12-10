# 分布式实时Faiss召回系统
- 1 概述
- 2 API
- 2 部署
- 参考

# 1 概述
原生的Faiss不支持分布式，本文利用S3和Zookeeper实现一个分布式的Faiss系统，
部署在Docker上。

支持向量检索的开源框架，比如vearch、milvus等，但我并没有用，

首先，业务方没有那么大的数据量，

其次，开源框架虽然部署简单，但也有一定成本，比如，学习成本、部署成本、运维成本等，

与其这样，还不如自己写一个。

![架构](doc/image/arc.png?raw=true)

整个Faiss集群外部是四层均衡负载：

1. 实线，为核心流程，只能由Master节点通过gRPC完成向量索引的增加、删除，及与其他节点的索引同步，并返回给客户端索引更新的详细信息，包括集群每个节点IP、更新前后的向量数量等
2. 长划线，为集群选举Master节点
3. 点划线，为集群索引同步
4. 点虚线，若客户端请求到达的是Slave节点，则需要转发给Master节点，完成集群节点的更新 

> 若图片不能正常显示，配置hosts文件
>
> ```shell script
> 151.101.76.133 raw.githubusercontent.com
> ``` 

# 2 grpc
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```

# 2 打包
执行：
```shell script
umake.py
```

# 3 部署
部署在docker上。