# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库结构

- `frontend/`：基于 Vue 3 + TypeScript + Vite 的单页应用。
- `backend/`：FastAPI 应用，采用 SQLAlchemy model / repository / service 分层，版本化路由位于 `app/api/v1`。
- `docs/`：项目文档。

## 常用命令

### 前端（`frontend/`）

安装依赖：

```bash
npm install
```

启动 Vite 开发服务器：

```bash
npm run dev
```

构建生产环境资源：

```bash
npm run build
```

预览生产构建结果：

```bash
npm run preview
```

运行 TypeScript / Vue 类型检查（`package.json` 中未定义脚本，直接使用本地二进制）：

```bash
npx vue-tsc --noEmit
```

### 后端（`backend/`）

安装依赖：

```bash
pip install -r requirements.txt
```

在 `backend/` 目录下启动本地 API：

```bash
python -m uvicorn app.main:app --reload
```

### 测试与 lint

- `frontend/package.json` 目前没有配置测试脚本。
- `frontend/package.json` 目前没有配置前端 lint 脚本。
- 我检查到的已提交文件里，没有仓库级测试命令说明。

## 前端架构

### 应用入口与路由

- SPA 入口在 `frontend/src/main.ts`，这里挂载 Pinia 和 Vue Router，并渲染 `App.vue`。
- `frontend/src/router.ts` 定义全部页面级路由，并通过 `src/pages/**` 懒加载页面组件。
- 路由鉴权是基于 token 的简单守卫：没有 `meta.public` 的页面在 `localStorage` 中缺少 `panda-app-token` 时会跳转到 `/login`；已登录用户访问 `/login` 会被重定向到 `/daily`。

### 状态管理与数据流

- 页面组件整体偏薄，通常只在 `onMounted` 中通过 Pinia store 拉取数据。
- `frontend/src/stores/` 按业务域拆分：
  - `user`：登录 / 注册 / 账号资料、token 持久化、头像上传、修改密码。
  - `profile`：八字档案创建与解读结果拉取。
  - `dailyFortune`：今日日运与历史日运。
  - `chat`：当日 AI 会话、额度状态、用户消息的乐观追加。
  - `growth` / `reminder`：成长档案与提醒设置。
- `frontend/src/api/*.ts` 中的 API 封装都比较薄，基本是一一映射后端接口。

### API 客户端约定

- `frontend/src/api/client.ts` 是唯一的通用 HTTP 层。
- Base URL 来自 `VITE_API_BASE_URL`，默认值是 `/api/v1`；`frontend/.env.development` 也显式配置了相同值。
- Vite 会把 `/api` 代理到 `http://127.0.0.1:8000`，所以本地联调默认依赖 FastAPI 服务跑在 8000 端口。
- 前端默认后端所有响应都遵循 `{ success, message, data }` 包装结构；Axios 响应拦截器会自动解包 `data`，并在 `success` 为 `false` 时抛出 `ApiError`。
- 请求拦截器会从 `localStorage` 中读取 token，并注入 `Authorization: Bearer <token>`。
- 收到 `401` 时，会清空本地认证信息，并强制跳转到 `/login`。

### UI 结构与样式体系

- 页面位于 `frontend/src/pages/`，按功能拆分为 `login`、`profile`、`daily`、`ai`、`growth`、`me` 等目录。
- 可复用 UI 分为业务组件 `frontend/src/components/**` 和共享基础组件 `components/common/`。
- 样式以 Tailwind 为主。`page-shell`、`surface-card`、`btn-primary` 以及熊猫主题背景等共享视觉原语集中定义在 `frontend/src/styles.css`。
- `frontend/tailwind.config.js` 定义了项目配色和字体 token；整体视觉语言是偏柔和的熊猫主题卡片式界面，不是通用后台模板风格。

## 后端架构

### 请求处理入口

- `backend/app/main.py` 创建 FastAPI 应用，开启 `localhost:5173` 的 CORS，挂载 `/uploads` 静态目录，注册统一异常处理，并把所有版本化路由挂到 `settings.api_prefix` 下。
- API 前缀由 `backend/app/core/config.py` 配置，当前默认是 `/api/v1`，与前端配置保持一致。

### 分层方式

后端采用比较清晰的分层：

- `app/api/v1/`：按业务域划分的 HTTP 路由（`auth`、`account`、`profile`、`daily_fortune`、`ai_chat`、`growth_archive`、`reminder`）。
- `app/services/`：业务逻辑。
- `app/repositories/`：持久化 / 数据访问。
- `app/models/`：SQLAlchemy 模型。
- `app/schemas/`：请求与响应结构。
- `app/core/`：配置、统一响应封装、异常、鉴权 / 安全、上传等基础能力。

修改后端行为时，优先保持 router → service → repository 的职责分层，不要把业务逻辑直接堆到路由处理函数里。

### 当前数据模式

- 仓库里同时存在完整的 SQLAlchemy / 数据库结构（`app/db`、`app/models`、多个 repository），也存在一个内存 mock 数据源：`backend/app/repositories/memory_store.py`。
- 当前已提交的前端体验明显围绕一套固定 demo 流程构建：demo 账号、mock token、静态日运 / 问答 / 成长档案数据，以及提醒默认值，都能在该 memory store 和后端设置里看到。
- 在修改持久化相关逻辑前，先确认你要改的 route / service 目前到底接的是 mock store，还是数据库 repository。

### 认证与账号相关约定

- 前端默认登录和注册接口都返回 `{ token, user, hasProfile }`。
- 账号管理是独立的鉴权区域，前端已接入 `/account/me`、`/account/change-password`、`/account/avatar` 这几个接口，并在对应 store / API 模块中使用。

## 重要的前后端协作约定

- 前后端在路由名和 payload 结构上耦合较紧；如果修改后端接口，通常需要同步更新 `frontend/src/api/` 中对应文件，以及相关 Pinia store。
- 前端默认头像上传成功后，返回的头像地址应当能被浏览器直接访问。
- 这个项目不是通用聊天应用，页面结构和 schema 命名都围绕八字档案、命盘解读、今日日运、AI 问答、成长档案、提醒设置这些业务概念展开。
