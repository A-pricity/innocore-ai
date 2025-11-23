# InnoCore AI 快速参考

## 🚀 启动系统

```bash
python run.py
```

访问: http://localhost:8000

## 📚 核心功能

### 1. 论文搜索 (Hunter)
```bash
POST /api/v1/papers/search
{
  "keywords": "machine learning",
  "source": "arxiv",
  "limit": 10
}
```

### 2. PDF 上传与解析 (Miner)
```bash
POST /api/v1/analysis/upload-pdf
Content-Type: multipart/form-data
file: <PDF文件>
```

### 3. 论文分析 (Miner)
```bash
POST /api/v1/analysis/analyze
{
  "paper_url": "https://arxiv.org/abs/2301.00001",
  "analysis_type": "summary"  # summary/innovation/comparison/comprehensive
}
```

或使用上传的 PDF:
```bash
POST /api/v1/analysis/analyze
{
  "paper_url": "/uploads/paper.pdf",
  "analysis_type": "summary"
}
```

### 4. 写作助手 (Coach)
```bash
POST /api/v1/writing/coach
{
  "text": "Your text here",
  "style": "academic",  # academic/technical/popular
  "task": "improve"     # improve/polish/translate/check
}
```

### 5. 引用校验 (Validator)
```bash
POST /api/v1/citations/validate
{
  "citation": "Your citation here",
  "format": "bibtex"  # bibtex/apa/ieee/mla
}
```

## 📖 分析类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `summary` | 摘要分析 | 快速了解论文 |
| `innovation` | 创新点分析 | 研究创新性 |
| `comparison` | 对比分析 | 方法对比 |
| `comprehensive` | 综合分析 | 深度研究 |

## 🔧 配置文件

`.env` 文件配置:
```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-3.5-turbo
```

## 📁 文件路径

- **上传文件**: `downloads/`
- **前端**: `frontend/`
- **API**: `api/routes/`
- **工具**: `utils/`

## 🐛 常见问题

### PDF 无法解析
- 确认是文字版 PDF（非扫描版）
- 检查文件大小 < 50MB

### API 返回 503
- 检查 `.env` 中的 API 密钥
- 确认 LLM 服务可用

### 分析超时
- 使用更快的模型
- 减小 PDF 文件大小

## 📊 系统状态

```bash
# 健康检查
GET /health

# API 文档
GET /docs
```

## 🔗 相关文档

- [使用指南](USAGE_GUIDE.md)
- [PDF 分析指南](PDF_ANALYSIS_GUIDE.md)
- [实现总结](IMPLEMENTATION_SUMMARY.md)
