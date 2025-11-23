#!/usr/bin/env python3
"""系统诊断脚本 - 检查所有配置和依赖"""

import sys
import os
from pathlib import Path

def check_env_file():
    """检查 .env 文件"""
    print("\n" + "="*60)
    print("1. 检查环境配置文件")
    print("="*60)
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env 文件不存在")
        return False
    
    print("✅ .env 文件存在")
    
    # 读取关键配置
    with open(env_path) as f:
        content = f.read()
        
    required_keys = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
    for key in required_keys:
        if key in content:
            print(f"✅ {key} 已配置")
        else:
            print(f"⚠️  {key} 未配置")
    
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n" + "="*60)
    print("2. 检查依赖包")
    print("="*60)
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain_openai",
        "arxiv",
        "httpx",
        "asyncpg",
        "qdrant_client",
        "feedparser",
        "beautifulsoup4"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 缺失")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  缺失的包: {', '.join(missing)}")
        print(f"安装命令: pip install {' '.join(missing)}")
        return False
    
    return True

def check_config():
    """检查配置加载"""
    print("\n" + "="*60)
    print("3. 检查配置加载")
    print("="*60)
    
    try:
        from core.config import get_config
        config = get_config()
        
        print(f"✅ 配置加载成功")
        print(f"   - API Key: {'已设置' if config.llm.api_key else '未设置'}")
        print(f"   - Base URL: {config.llm.base_url or '未设置'}")
        print(f"   - Model: {config.llm.model_name}")
        print(f"   - Debug: {config.debug}")
        
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {str(e)}")
        return False

def check_api_routes():
    """检查 API 路由"""
    print("\n" + "="*60)
    print("4. 检查 API 路由")
    print("="*60)
    
    try:
        from api.main import app
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"✅ API 加载成功，共 {len(routes)} 个路由")
        
        # 检查关键路由
        key_routes = ["/", "/health", "/api/v1/papers/search", "/api/v1/analysis/analyze"]
        for route in key_routes:
            if route in routes:
                print(f"   ✅ {route}")
            else:
                print(f"   ❌ {route} - 缺失")
        
        return True
    except Exception as e:
        print(f"❌ API 加载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_frontend():
    """检查前端文件"""
    print("\n" + "="*60)
    print("5. 检查前端文件")
    print("="*60)
    
    frontend_files = [
        "frontend/index.html",
        "frontend/static/css/style.css",
        "frontend/static/js/app.js"
    ]
    
    all_exist = True
    for file_path in frontend_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} - 不存在（可选）")
    
    return True

def check_llm_connection():
    """检查 LLM 连接"""
    print("\n" + "="*60)
    print("6. 检查 LLM 连接")
    print("="*60)
    
    try:
        import asyncio
        from langchain_openai import ChatOpenAI
        from core.config import get_config
        
        config = get_config()
        
        if not config.llm.api_key:
            print("⚠️  API Key 未设置，跳过连接测试")
            return True
        
        async def test():
            llm = ChatOpenAI(
                model=config.llm.model_name,
                temperature=0.7,
                api_key=config.llm.api_key,
                base_url=config.llm.base_url
            )
            
            response = await llm.ainvoke("测试")
            return response.content
        
        print("正在测试 LLM 连接...")
        result = asyncio.run(test())
        print(f"✅ LLM 连接成功")
        print(f"   模型响应: {result[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ LLM 连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("\n" + "="*60)
    print("InnoCore AI 系统诊断")
    print("="*60)
    
    results = []
    
    results.append(("环境配置", check_env_file()))
    results.append(("依赖包", check_dependencies()))
    results.append(("配置加载", check_config()))
    results.append(("API 路由", check_api_routes()))
    resul)
 main(__":
    "__main __name__ ==\n")

if"*60 + ""=   print(
    
 )修复问题。"未通过，请根据上述提示⚠️  部分检查print("\n         else:
n.py")
   thon ru: py("\n启动命令      print")
  行。以正常运所有检查通过！系统可rint("\n🎉        pd:
 seasll_p   if a
    
 lts) r in resufor1] all(r[sed = all_pas  
      status}")
me}: {print(f"{na       "
 "❌ 失败e lsif result e" 通过us = "✅         statts:
sul in resultname, re    for    
="*60)
     print("总结")
int("诊断0)
    pr + "="*6\n"rint("结
    p# 总       

 ion()))nnecteck_llm_co, ch(("LLM 连接"s.append
    resultend()))nt_fro", checkd(("前端文件ts.appen