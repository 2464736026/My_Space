import pdfplumber
import PyPDF2
import io
import re

class PDFParser:
    """PDF文件解析器"""
    
    def extract_text(self, pdf_content: bytes) -> str:
        """从PDF内容中提取文本"""
        try:
            # 首先尝试使用pdfplumber
            text = self._extract_with_pdfplumber(pdf_content)
            if text.strip():
                return self._clean_text(text)
            
            # 如果pdfplumber失败，尝试PyPDF2
            text = self._extract_with_pypdf2(pdf_content)
            return self._clean_text(text)
            
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
    
    def _extract_with_pdfplumber(self, pdf_content: bytes) -> str:
        """使用pdfplumber提取文本"""
        text_parts = []
        
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return "\n".join(text_parts)
    
    def _extract_with_pypdf2(self, pdf_content: bytes) -> str:
        """使用PyPDF2提取文本"""
        text_parts = []
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        return "\n".join(text_parts)
    
    def _clean_text(self, text: str) -> str:
        """清洗和结构化文本"""
        if not text:
            return ""
        
        # 保留换行符，只合并多余的空格
        text = re.sub(r'[ \t]+', ' ', text)
        
        # 移除特殊字符但保留中文、英文、数字、基本标点和换行符
        text = re.sub(r'[^\u4e00-\u9fff\w\s\-@.()（）：:；;，,。.！!？?\n]', '', text)
        
        # 规范化多个连续换行为双换行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 移除首尾空白
        text = text.strip()
        
        return text