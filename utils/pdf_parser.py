"""
InnoCore AI PDF解析工具
"""

import asyncio
import fitz  # PyMuPDF
from typing import Dict, List, Optional, Any, Tuple
import re
import os
from pathlib import Path
import hashlib

from ..core.exceptions import PDFParsingException

class PDFParser:
    """PDF解析器"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    async def parse_pdf(self, file_path: str, extract_images: bool = False) -> Dict[str, Any]:
        """解析PDF文件"""
        if not os.path.exists(file_path):
            raise PDFParsingException(f"文件不存在: {file_path}")
        
        try:
            doc = fitz.open(file_path)
            
            # 提取基本信息
            metadata = self._extract_metadata(doc)
            
            # 提取文本内容
            text_content = await self._extract_text(doc)
            
            # 结构化解析
            structured_content = await self._parse_structure(text_content, metadata)
            
            # 提取表格
            tables = await self._extract_tables(doc)
            
            # 提取图片（可选）
            images = []
            if extract_images:
                images = await self._extract_images(doc, file_path)
            
            doc.close()
            
            return {
                "metadata": metadata,
                "text_content": text_content,
                "structured_content": structured_content,
                "tables": tables,
                "images": images,
                "file_info": {
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "pages": len(structured_content.get("pages", [])),
                    "parsing_method": "pymupdf"
                }
            }
            
        except Exception as e:
            raise PDFParsingException(f"PDF解析失败: {str(e)}")
    
    def _extract_metadata(self, doc: fitz.Document) -> Dict[str, Any]:
        """提取PDF元数据"""
        metadata = doc.metadata
        
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", ""),
            "page_count": doc.page_count,
            "is_encrypted": doc.is_encrypted
        }
    
    async def _extract_text(self, doc: fitz.Document) -> str:
        """提取文本内容"""
        text_content = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text_content += page.get_text()
            text_content += "\n\n"  # 页面分隔符
        
        return text_content.strip()
    
    async def _parse_structure(self, text_content: str, metadata: Dict) -> Dict[str, Any]:
        """解析文档结构"""
        lines = text_content.split('\n')
        
        # 初始化结构
        structure = {
            "title": metadata.get("title", ""),
            "abstract": "",
            "sections": {},
            "pages": [],
            "references": []
        }
        
        current_section = "introduction"
        current_page_content = []
        page_num = 1
        
        # 解析逻辑
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # 检测章节标题
            section_match = self._detect_section(line)
            if section_match:
                # 保存上一页内容
                if current_page_content:
                    structure["pages"].append({
                        "page_number": page_num,
                        "content": "\n".join(current_page_content)
                    })
                    current_page_content = []
                    page_num += 1
                
                current_section = section_match.lower().replace(" ", "_")
                structure["sections"][current_section] = []
                continue
            
            # 检测摘要
            if line.lower().startswith("abstract") or "摘要" in line:
                current_section = "abstract"
                continue
            
            # 检测参考文献
            if line.lower().startswith("references") or "参考文献" in line:
                current_section = "references"
                continue
            
            # 添加到当前章节
            if current_section in structure["sections"]:
                structure["sections"][current_section].append(line)
            elif current_section == "abstract":
                structure["abstract"] += line + " "
            elif current_section == "references":
                structure["references"].append(line)
            else:
                current_page_content.append(line)
        
        # 保存最后一页
        if current_page_content:
            structure["pages"].append({
                "page_number": page_num,
                "content": "\n".join(current_page_content)
            })
        
        # 清理章节内容
        for section in structure["sections"]:
            structure["sections"][section] = "\n".join(structure["sections"][section])
        
        return structure
    
    def _detect_section(self, line: str) -> Optional[str]:
        """检测章节标题"""
        # 常见的章节标题模式
        section_patterns = [
            r'^\d+\.\s+(.+)$',  # 1. Introduction
            r'^[A-Z][A-Z\s]+$',  # INTRODUCTION (全大写)
            r'^[IVX]+\.\s+(.+)$',  # I. Introduction
            r'^\d+\.\d+\s+(.+)$',  # 1.1 Background
        ]
        
        for pattern in section_patterns:
            match = re.match(pattern, line)
            if match:
                return match.group(1) if match.groups() else line
        
        # 检查常见章节关键词
        section_keywords = [
            "introduction", "related work", "methodology", "method", 
            "experiment", "results", "discussion", "conclusion", 
            "abstract", "references", "acknowledgments"
        ]
        
        line_lower = line.lower()
        for keyword in section_keywords:
            if keyword in line_lower and len(line) < 100:
                return line
        
        return None
    
    async def _extract_tables(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """提取表格"""
        tables = []
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # 查找表格
            table_finder = page.find_tables()
            
            for table_idx, table in enumerate(table_finder.tables):
                try:
                    table_data = table.extract()
                    
                    # 转换为更易处理的格式
                    formatted_table = {
                        "page_number": page_num + 1,
                        "table_index": table_idx,
                        "bbox": table.bbox,
                        "rows": len(table_data),
                        "cols": len(table_data[0]) if table_data else 0,
                        "data": table_data,
                        "caption": ""
                    }
                    
                    tables.append(formatted_table)
                    
                except Exception as e:
                    print(f"表格提取失败 page {page_num + 1}, table {table_idx}: {str(e)}")
        
        return tables
    
    async def _extract_images(self, doc: fitz.Document, pdf_path: str) -> List[Dict[str, Any]]:
        """提取图片"""
        images = []
        
        # 创建图片保存目录
        pdf_dir = Path(pdf_path).parent
        images_dir = pdf_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_idx, img in enumerate(image_list):
                try:
                    # 获取图片数据
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    if pix.n - pix.alpha < 4:  # 确保不是CMYK
                        # 生成文件名
                        img_filename = f"page_{page_num + 1}_img_{img_idx + 1}.png"
                        img_path = images_dir / img_filename
                        
                        # 保存图片
                        pix.save(str(img_path))
                        
                        # 记录图片信息
                        image_info = {
                            "page_number": page_num + 1,
                            "image_index": img_idx,
                            "filename": img_filename,
                            "path": str(img_path),
                            "width": pix.width,
                            "height": pix.height,
                            "colorspace": pix.colorspace.name if pix.colorspace else "unknown",
                            "size": os.path.getsize(img_path)
                        }
                        
                        images.append(image_info)
                    
                    pix = None  # 释放内存
                    
                except Exception as e:
                    print(f"图片提取失败 page {page_num + 1}, img {img_idx}: {str(e)}")
        
        return images
    
    async def extract_citations(self, text_content: str) -> List[Dict[str, Any]]:
        """提取引用信息"""
        citations = []
        
        # 常见的引用模式
        citation_patterns = [
            r'\[(\d+)\]',  # [1], [2-3]
            r'\(([A-Za-z]+(?:\s+et\s+al\.)?,\s*\d{4})\)',  # (Smith et al., 2020)
            r'([A-Za-z]+\s+et\s+al\.\s*\(\d{4}\))',  # Smith et al. (2020)
            r'([A-Za-z]+\s*\(\d{4}\))',  # Smith (2020)
        ]
        
        for pattern in citation_patterns:
            matches = re.finditer(pattern, text_content)
            for match in matches:
                citation_text = match.group(0)
                
                citation_info = {
                    "text": citation_text,
                    "start_pos": match.start(),
                    "end_pos": match.end(),
                    "type": self._classify_citation_type(citation_text)
                }
                
                citations.append(citation_info)
        
        return citations
    
    def _classify_citation_type(self, citation_text: str) -> str:
        """分类引用类型"""
        if citation_text.startswith('[') and citation_text.endswith(']'):
            return "numeric"
        elif "et al." in citation_text.lower():
            return "author_et_al"
        elif '(' in citation_text and ')' in citation_text:
            return "author_year"
        else:
            return "unknown"
    
    async def extract_formulas(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """提取数学公式"""
        formulas = []
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # 查找数学公式（这是一个简化的实现）
            text = page.get_text()
            
            # 常见的公式模式
            formula_patterns = [
                r'\$[^$]+\$',  # $formula$
                r'\\\[.*?\\\]',  # \[formula\]
                r'\\\(.*?\\\)',  # \(formula\)
                r'\\begin\{equation\}.*?\\end\{equation\}',  # LaTeX equation
            ]
            
            for pattern in formula_patterns:
                matches = re.finditer(pattern, text, re.DOTALL)
                for match in matches:
                    formula_text = match.group(0)
                    
                    formula_info = {
                        "page_number": page_num + 1,
                        "text": formula_text,
                        "start_pos": match.start(),
                        "end_pos": match.end(),
                        "type": self._classify_formula_type(formula_text)
                    }
                    
                    formulas.append(formula_info)
        
        return formulas
    
    def _classify_formula_type(self, formula_text: str) -> str:
        """分类公式类型"""
        if formula_text.startswith('$') and formula_text.endswith('$'):
            return "inline"
        elif '\\[' in formula_text and '\\]' in formula_text:
            return "display"
        elif '\\begin{equation}' in formula_text:
            return "equation"
        else:
            return "unknown"
    
    async def calculate_content_hash(self, file_path: str) -> str:
        """计算文件内容哈希"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception as e:
            raise PDFParsingException(f"计算文件哈希失败: {str(e)}")
    
    async def extract_key_sentences(self, text_content: str, max_sentences: int = 10) -> List[str]:
        """提取关键句子"""
        sentences = re.split(r'[.!?]+', text_content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 简单的关键句子提取逻辑
        key_sentences = []
        
        # 优先选择包含特定关键词的句子
        keywords = [
            "propose", "method", "approach", "result", "conclusion",
            "contribute", "novel", "significant", "improve", "achieve"
        ]
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                key_sentences.append(sentence)
                if len(key_sentences) >= max_sentences:
                    break
        
        # 如果关键句子不够，补充长句子
        if len(key_sentences) < max_sentences:
            remaining_sentences = [s for s in sentences if s not in key_sentences]
            remaining_sentences.sort(key=len, reverse=True)
            
            for sentence in remaining_sentences:
                if len(key_sentences) >= max_sentences:
                    break
                key_sentences.append(sentence)
        
        return key_sentences[:max_sentences]