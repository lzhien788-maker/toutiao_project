# toutiao_project
头条新闻全栈项目
后端：FastAPI + SQLAlchemy(异步) + MySQL + Redis
前端：Vue3 + Vite + Vant

## 项目结构
toutiao_project
├── toutiao_backend      # FastAPI 后端
├── xwzx-news            # Vue 前端
└── .gitignore


## 后端启动
```bash
cd toutiao_backend
# 创建虚拟环境
python -m venv .venv
# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 安装依赖
pip install fastapi uvicorn sqlalchemy[asyncio] aiomysql redis passlib bcrypt
# 启动服务
python -m uvicorn main:app --reload

cd xwzx-news
npm install
npm run dev
