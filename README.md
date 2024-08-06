# bili-emoji-downloader-vue

用于批量下载 B站 表情包，部署在 Vercel 上

[![deploy](https://camo.githubusercontent.com/0d115430c1db17132964386282927e5e313543c7d868fc06bc9a7c65d7ec974e/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/new/git/external?repository-url=https://github.com/magicFeirl/bili-emoji-downloader-vue)

## 配置

根据项目 example.env 中的示例环境变量字段配置环境变量，之后在 vercel 中导入配置的环境变量值，重新部署项目

## Vercel 后端部署

该项目后端非常简单，基本只是充当一个反代功能，所以放在前端文件夹里面了。查阅 Vercel 官方文档之后发现后端的结构是：放在项目根目录，文件夹命名为 api，默认有个 index.py 实现功能。

### 问题

一开始搜索接口的端点是 `/search` 尝试使用 `/api/search` 或者 `/search` 访问均 404，查看示例项目之后发现需要加个 `/api` BaseURL，也就是接口端点改为 `/api/search`，继续部署发现还是 404，但是访问 `/api` 的时候能路由到 FastAPI，并且由 FastAPI 报 404。测试多次后发现貌似 Vercel 的后端只能用默认几个端点，比如 `/api`和 `/api/index`，所以最后接口端点是: `/api/index` 而不是 `/search`

~~复用性问题：每个 endpoint 需要单独创建对应的文件，其中创建 FastAPI 实例和其它代码可能大量重复，可能需要导出成一个公共文件之后分别导入~~

具体路由可以参考官方示例配置文件：[vercel.json](https://github.com/vercel/examples/blob/main/python/flask2/vercel.json)，[rewrites-on-verce](https://vercel.com/docs/edge-network/rewrites#rewrites-on-vercel)

此外，FastAPI 结合 Vue 的时候，接口端点一般会加上 `/api` 前缀，发送请求时路由接收到的是 `/api/xxx`，如果后端的路由是 `/xxx` 则会 404，解决方法有两个：
1. 后端路由统一添加 `/api` 前缀，也就是 `/api/xxx`
2. 设置 `root_path='/api'`，实例功能有点类似前端反代的 path rewrite，但是接受到请求时会去掉 `/api` 前缀，[root_path 文档](https://fastapi.tiangolo.com/advanced/behind-a-proxy/?h=root_#providing-the-root_path)



## 开发
```sh
# vue3
npm install
npm run dev

npm run build

# python
cd api
uvicorn index:app
```