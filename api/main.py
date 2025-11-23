"""
InnoCore API 主应用
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import uvicorn

from core.config import get_config
from core.database import db_manager
from core.vector_store import vector_store_manager
from agents.controller import agent_controller
from .routes import papers, users, tasks, analysis, writing, citations

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    logger.info("正在启动InnoCore AI...")
    
    try:
        # 初始化数据库
        await db_manager.initialize()
        logger.info("数据库初始化完成")
        
        # 初始化向量存储
        await vector_store_manager.initialize()
        logger.info("向量存储初始化完成")
        
        # 初始化智能体控制器
        await agent_controller.initialize()
        logger.info("智能体控制器初始化完成")
        
        # 启动任务处理器
        import asyncio
        asyncio.create_task(agent_controller.start_task_processor())
        logger.info("任务处理器已启动")
        
        yield
        
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        raise
    
    finally:
        # 关闭时清理
        logger.info("正在关闭InnoCore AI...")
        await agent_controller.shutdown()
        await db_manager.close()
        await vector_store_manager.close()
        logger.info("InnoCore AI已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="InnoCore AI API",
    description="智能科研创新助手API",
    version="0.1.0",
    lifespan=lifespan
)

# 配置CORS
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(papers.router, prefix="/api/v1/papers", tags=["papers"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(writing.router, prefix="/api/v1/writing", tags=["writing"])
app.include_router(citations.router, prefix="/api/v1/citations", tags=["citations"])

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to InnoCore AI API",
        "version": "0.1.0",
        "status": "running"
    }

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 检查各组件状态
        agent_status = await agent_controller.get_agent_status()
        
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "components": {
                "database": "connected",
                "vector_store": "connected",
                "agents": agent_status
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if config.debug else "Something went wrong"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "innocore_ai.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        log_level="info"
    )