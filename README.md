tornado_api_demo
![](https://img.shields.io/badge/python%20-%203.7-brightgreen.svg)
========
> 如何使用tornado开发api后台

演示如何基于tornado, sqlalchemy, redis实现一个api后台，这个框架有下列特征:

1. 利用concurrent和ThreadPoolExecutor满足一定的并发需求
2. 按版本加载对应数据模型，版本之间完全独立，这样可以进行灵活的版本开发管理
3. 对每个请求提供一个独立的sqlalchemy session
4. 提供存取缓存的修饰符

### 文件组织

| file & dir | desc |
| :--: | :--:|
| base.py | 通用方法和类 |
| context.py | 全局上下文 |
| pyredis.py | redis封装 |
| run.py | 主程序 |
| model | 数据模型 |
| model/factory.py | 数据模型工厂 |
| model/version_* | 某个版本的数据模型 |

