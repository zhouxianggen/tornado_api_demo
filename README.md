tornado_api_demo
![](https://img.shields.io/badge/python%20-%203.7-brightgreen.svg)
========
> 使用tornado开发api后台的例子

一个使用tornado, sqlalchemy, redis开发api后台的例子:

1. 利用concurrent和ThreadPoolExecutor满足一定的并发需求
2. 按版本动态匹配数据模型，使版本迭代更新不影响旧版本
3. 对每个请求提供一个独立的sqlalchemy session
4. 提供存取缓存的修饰符，方便请求数据的缓存

### 文件组织

| file & dir | desc |
| :--: | :--:|
| errors.py | 错误定义 |
| util.py | 通用法规范 |
| pyredis.py | redis封装 |
| run.py | 主程序 |
| model | 数据模型 |
| model/factory.py | 数据模型工厂 |
| model/v* | 某个版本的数据模型 |

