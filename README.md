# bili-emoji-downloader-vue

用于批量下载 B站 表情包，部署在 Vercel 上

## Vercel 后端部署

该项目后端非常简单，基本只是充当一个反代功能，所以放在前端文件夹里面了。查阅 Vercel 官方文档之后发现后端的结构是：放在项目根目录，文件夹命名为 api，默认有个 index.py 实现功能。

### 问题

一开始搜索接口的端点是 `/search` 尝试使用 `/api/search` 或者 `/search` 访问均 404，查看示例项目之后发现需要加个 `/api` BaseURL，也就是接口端点改为 `/api/search`，继续部署发现还是 404，但是访问 `/api` 的时候能路由到 FastAPI，并且由 FastAPI 报 404。测试多次后发现貌似 Vercel 的后端只能用默认几个端点，比如 `/api`和 `/api/index`，所以最后接口端点是: `/api/index` 而不是 `/search`

## 开发
```sh
# vue3
npm install
npm run dev

npm run build
```