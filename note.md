## Vercel 后端部署

该项目后端非常简单，基本只是充当一个反代功能，所以放在前端文件夹里面了。查阅 Vercel 官方文档之后发现后端的结构是：放在项目根目录，文件夹命名为 api，默认有个 index.py 实现功能。

### 问题


**前端**

一开始只考虑表情包下载，导致后续新增功能代码松散、增加了代码复杂程度

**后端**

没有做好封装

一开始搜索接口的端点是 `/search` 尝试使用 `/api/search` 或者 `/search` 访问均 404，查看示例项目之后发现需要加个 `/api` BaseURL，也就是接口端点改为 `/api/search`，继续部署发现还是 404，但是访问 `/api` 的时候能路由到 FastAPI，并且由 FastAPI 报 404。测试多次后发现貌似 Vercel 的后端只能用默认几个端点，比如 `/api`和 `/api/index`，所以最后接口端点是: `/api/index` 而不是 `/search`

~~复用性问题：每个 endpoint 需要单独创建对应的文件，其中创建 FastAPI 实例和其它代码可能大量重复，可能需要导出成一个公共文件之后分别导入~~

具体路由可以参考官方示例配置文件：[vercel.json](https://github.com/vercel/examples/blob/main/python/flask2/vercel.json)，[rewrites-on-verce](https://vercel.com/docs/edge-network/rewrites#rewrites-on-vercel)

此外，FastAPI 结合 Vue 的时候，接口端点一般会加上 `/api` 前缀，发送请求时路由接收到的是 `/api/xxx`，如果后端的路由是 `/xxx` 则会 404，解决方法有两个：
1. 后端路由统一添加 `/api` 前缀，也就是 `/api/xxx`
2. 设置 `root_path='/api'`，实例功能有点类似前端反代的 path rewrite，但是接受到请求时会去掉 `/api` 前缀，[root_path 文档](https://fastapi.tiangolo.com/advanced/behind-a-proxy/?h=root_#providing-the-root_path)