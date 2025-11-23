# PDF 分析功能使用指南

## 功能概述

InnoCore AI 现在支持完整的 PDF 文件解析和分析功能。系统可以：

1. **自动解析 PDF 文件**
   - 提取标题
   - 提取作者信息
   - 提取摘要
   - 提取全文内容
   - 统计页数和字数

2. **AI 深度分析**
   - 基于解析出的完整内容进行分析
   - 支持多种分析类型（摘要、创新点、对比、综合）
   - 使用 AI 模型理解论文内容

## 使用方法

### 方式一：通过前端界面

1. 访问 http://localhost:8000
2. 进入 "Miner - 论文分析" 模块
3. 点击或拖拽上传 PDF 文件
4. 系统自动解析并显示：
   - 论文标题
   - 作者列表
   - 摘要内容
   - 页数和字数
5. 选择分析类型（摘要/创新点/对比/综合）
6. 点击"开始分析"进行 AI 分析

### 方式二：通过 API

#### 1. 上传并解析 PDF

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/upload-pdf" \
  -F "file=@your_paper.pdf"
```

响应示例：
```json
{
  "success": true,
  "filename": "your_paper.pdf",
  "file_path": "/uploads/your_paper.pdf",
  "title": "Machine Learning in Computer Vision",
  "authors": ["John Doe", "Jane Smith"],
  "abstract": "This paper presents...",
  "page_count": 12,
  "word_count": 5432,
  "message": "PDF 文件上传并解析成功"
}
```

#### 2. 分析 PDF 内容

使用返回的 `file_path` 进行分析：

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "paper_url": "/uploads/your_paper.pdf",
    "analysis_type": "summary"
  }'
```

## 支持的分析类型

### 1. summary（摘要分析）
- 研究背景和动机
- 主要方法
- 核心贡献
- 实验结果
- 研究意义

### 2. innovation（创新点分析）
- 技术创新点
- 方法论创新
- 理论贡献
- 与现有工作的区别
- 潜在应用价值

### 3. comparison（对比分析）
- 与传统方法的对比
- 优势和劣势
- 适用场景
- 性能提升
- 局限性

### 4. comprehensive（综合分析）
- 研究背景和意义
- 技术方法详解
- 创新点分析
- 实验验证
- 优缺点评价
- 未来研究方向
- 实际应用价值

## 技术实现

### PDF 解析库
- **pdfplumber**: 主要解析库，支持文本提取
- **PyPDF2**: 备用解析库
- **pypdf**: 辅助解析库

### 解析流程
1. 接收 PDF 文件（文件路径或字节流）
2. 使用 pdfplumber 逐页提取文本
3. 智能识别标题（通常在前几行）
4. 提取作者信息（通过邮箱、机构等关键词）
5. 定位并提取摘要（通过 Abstract 关键词）
6. 统计页数和字数
7. 返回结构化数据

### AI 分析流程
1. 获取 PDF 解析结果
2. 限制文本长度（前 8000 字符，避免超出 token 限制）
3. 根据分析类型生成专业提示词
4. 调用 LLM 进行深度分析
5. 返回 Markdown 格式的分析结果

## 文件存储

上传的 PDF 文件保存在：
```
innocore_ai/downloads/
```

文件路径格式：
```
/uploads/filename.pdf
```

## 注意事项

1. **文件大小限制**
   - 建议单个 PDF 文件不超过 50MB
   - 过大的文件可能导致解析超时

2. **文本提取质量**
   - 扫描版 PDF 可能无法提取文本
   - 建议使用文字版 PDF 以获得最佳效果
   - 如果 PDF 包含图片或公式，可能无法完整提取

3. **分析时间**
   - PDF 解析通常在 1-5 秒内完成
   - AI 分析需要 10-30 秒，取决于论文长度和模型速度

4. **Token 限制**
   - 系统自动限制分析文本为前 8000 字符
   - 对于超长论文，建议使用 ArXiv URL（可获取完整摘要）

## 示例工作流

### 完整的论文分析流程

1. **上传 PDF**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/analysis/upload-pdf" \
     -F "file=@research_paper.pdf"
   ```

2. **查看解析结果**
   ```json
   {
     "title": "Deep Learning for Image Recognition",
     "authors": ["Alice Wang", "Bob Chen"],
     "abstract": "We propose a novel deep learning architecture...",
     "page_count": 15,
     "word_count": 7890
   }
   ```

3. **进行摘要分析**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "paper_url": "/uploads/research_paper.pdf",
       "analysis_type": "summary"
     }'
   ```

4. **获取分析结果**
   - 研究背景
   - 主要方法
   - 核心贡献
   - 实验结果
   - 研究意义

5. **进行创新点分析**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "paper_url": "/uploads/research_paper.pdf",
       "analysis_type": "innovation"
     }'
   ```

## 故障排除

### 问题：无法提取文本
**解决方案**：
- 确认 PDF 不是扫描版
- 尝试使用 PDF 编辑器重新保存
- 使用 ArXiv URL 代替本地 PDF

### 问题：解析结果不准确
**解决方案**：
- 检查 PDF 格式是否标准
- 确认标题和作者信息在前几页
- 手动编辑解析结果后再分析

### 问题：分析超时
**解决方案**：
- 检查网络连接
- 确认 AI 模型配置正确
- 尝试使用更快的模型

## 未来改进

- [ ] 支持 OCR 识别扫描版 PDF
- [ ] 支持提取图表和公式
- [ ] 支持批量 PDF 分析
- [ ] 支持自定义解析规则
- [ ] 支持更多文件格式（Word、LaTeX 等）

## 相关文档

- [使用指南](USAGE_GUIDE.md)
- [API 文档](http://localhost:8000/docs)
- [系统状态](system_status.md)
