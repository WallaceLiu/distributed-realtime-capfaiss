# 分布式实时Faiss召回系统
- 1 概述
- 2 结构
- 3 gRPC
- 4 API
- 5 打包
- 6 部署
- 7 后续
- 参考

# 1 概述
原生的Faiss不支持分布式，本文利用S3和Zookeeper实现一个分布式实时Faiss系统，
功能包括索引的查询、删除、增加、重建等四个功能，部署在Docker上。

支持向量检索的开源框架，比如vearch、milvus等，但我并没有用，因为，

首先，业务方没有那么大的数据量，

其次，开源框架，虽然部署简单，但也是有成本的，比如，学习成本、部署成本、运维成本等，

与其这样，还不如自己写一个。

整个应用虽然也就花了7天，但测试比开发时间长很多。

# 2 结构

![结构](doc/image/flow.png?raw=true)

图1 结构

![更新流程](doc/image/arc.png?raw=true)

图2 索引更新流程

整个Faiss集群外部是四层均衡负载：

1. 实线，为核心流程。只能由Master节点完成向量索引的增加、删除，以及与其他节点同步索引，并返回给客户端索引更新的详细信息，包括集群每个节点IP、更新前后的向量数量等。
2. 长划线，为集群选举Master节点。在应用启动时，或运行期间，master挂点后，选举master节点。
3. 点划线，为集群索引同步。master节点通过gRPC与其他节点同步索引。
4. 点虚线，若客户端请求到达的是Slave节点，则需要转发给Master节点，完成集群节点的索引更新。 

> 若图片不能正常显示，配置hosts文件
>
> ```shell script
> 151.101.76.133 raw.githubusercontent.com
> ``` 

# 3 索引同步gRPC
索引同步gRPC定义在`protos`里，用如下命令，生成py文件，以便在应用中使用：
```shell script
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ syncindex.proto
```

# 4 API
对外公开的是Restful API，当然，也有gRPC接口：

[Restful API](doc/Restful%20API.md)

# 5 打包
执行`umake.py`脚本，会将应用打包到`deploy`目录。

# 6 部署
我部署在Core8、Men24GB的docker上。如果不缓存结果，则TPS=120，TP99=30ms。

# 7 后续
1. 召回的数据量，10，100，1000……都有可能，所以，如果使用Restful API的话，并且调用链路太长，
耗时可能会长，此时，你可以试试gRPC接口。
2. Faiss消耗CPU资源。
3. 若要支撑更多的TPS，采用缓存，分布式系统，要有自己的缓存系统。
4. 索引同步，可以采用asyncio改写，强化性能。
