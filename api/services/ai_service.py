"""
AI服务 - 使用OpenAI API处理简历分析
"""
import json
import re
from typing import Dict, Any, Optional
from openai import OpenAI
import config


class AIService:
    """AI服务类 - 处理所有AI相关的操作"""
    
    def __init__(self):
        """初始化OpenAI客户端"""
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your-openai-api-key-here":
            raise ValueError(
                "请在 backend/config.py 文件中配置你的 OPENAI_API_KEY！\n"
                "获取API密钥：https://platform.openai.com/api-keys"
            )
        
        # 初始化OpenAI客户端
        client_params = {
            "api_key": config.OPENAI_API_KEY,
            "timeout": config.TIMEOUT
        }
        
        if config.OPENAI_BASE_URL:
            client_params["base_url"] = config.OPENAI_BASE_URL
        
        self.client = OpenAI(**client_params)
        self.model = config.OPENAI_MODEL
    
    def extract_resume_info(self, resume_text: str) -> Dict[str, Any]:
        """
        使用AI从简历文本中提取信息
        
        Args:
            resume_text: PDF提取的简历文本
            
        Returns:
            包含简历信息的字典
        """
        try:
            # 限制文本长度，避免超过token限制
            if len(resume_text) > 8000:
                resume_text = resume_text[:8000] + "..."
            
            # 构建用户消息
            user_message = f"""请从以下简历文本中提取关键信息：

{resume_text}

请严格按照JSON格式返回数据。"""
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            
            # 提取响应内容
            result_text = response.choices[0].message.content.strip()
            
            # 解析JSON
            result = self._parse_json_response(result_text)
            
            # 验证和规范化数据
            result = self._normalize_resume_data(result)
            
            return result
            
        except Exception as e:
            print(f"AI提取失败: {str(e)}")
            raise Exception(f"AI简历分析失败: {str(e)}")
    
    def analyze_job_match(
        self, 
        resume_info: Dict[str, Any], 
        job_req: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        使用AI分析简历与岗位的匹配度
        
        Args:
            resume_info: 简历信息
            job_req: 岗位需求
            
        Returns:
            匹配度分析结果
        """
        try:
            # 格式化简历信息
            resume_summary = self._format_resume_for_matching(resume_info)
            
            # 构建提示词
            prompt = config.MATCH_PROMPT_TEMPLATE.format(
                resume_info=resume_summary,
                job_title=job_req.get('job_title', ''),
                job_description=job_req.get('job_description', ''),
                required_skills=job_req.get('required_skills', ''),
                experience_level=job_req.get('experience_level', '')
            )
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的HR助手，擅长分析简历与岗位的匹配度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            
            # 提取响应内容
            result_text = response.choices[0].message.content.strip()
            
            # 解析JSON
            result = self._parse_json_response(result_text)
            
            # 验证和规范化数据
            result = self._normalize_match_data(result)
            
            return result
            
        except Exception as e:
            print(f"AI匹配分析失败: {str(e)}")
            raise Exception(f"AI岗位匹配分析失败: {str(e)}")
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        解析AI返回的JSON响应
        
        Args:
            text: AI返回的文本
            
        Returns:
            解析后的字典
        """
        try:
            # 直接尝试解析
            return json.loads(text)
        except json.JSONDecodeError:
            # 如果失败，尝试提取JSON部分
            # 查找第一个 { 和最后一个 }
            start = text.find('{')
            end = text.rfind('}')
            
            if start != -1 and end != -1:
                json_text = text[start:end+1]
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    pass
            
            # 如果还是失败，尝试使用正则提取
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            raise ValueError("无法解析AI返回的JSON格式")
    
    def _normalize_resume_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化简历数据，确保所有必需字段存在
        
        Args:
            data: 原始数据
            
        Returns:
            规范化后的数据
        """
        normalized = {
            "basic_info": {
                "name": "",
                "phone": "",
                "email": "",
                "address": ""
            },
            "job_info": {
                "position": "",
                "salary": ""
            },
            "background": {
                "work_years": "",
                "education": "",
                "skills": [],
                "projects": []
            }
        }
        
        # 合并数据
        if "basic_info" in data:
            normalized["basic_info"].update(data["basic_info"])
        
        if "job_info" in data:
            normalized["job_info"].update(data["job_info"])
        
        if "background" in data:
            normalized["background"].update(data["background"])
        
        # 确保skills和projects是列表
        if not isinstance(normalized["background"]["skills"], list):
            normalized["background"]["skills"] = []
        
        if not isinstance(normalized["background"]["projects"], list):
            normalized["background"]["projects"] = []
        
        return normalized
    
    def _normalize_match_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化匹配数据
        
        Args:
            data: 原始数据
            
        Returns:
            规范化后的数据
        """
        normalized = {
            "skill_match": {
                "score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "details": ""
            },
            "experience_match": {
                "score": 0,
                "resume_years": "",
                "required_years": "",
                "details": ""
            },
            "position_match": {
                "score": 0,
                "details": ""
            },
            "total_score": 0,
            "recommendations": [],
            "interview_suggestion": ""
        }
        
        # 合并数据
        for key in normalized.keys():
            if key in data:
                if isinstance(normalized[key], dict):
                    normalized[key].update(data[key])
                else:
                    normalized[key] = data[key]
        
        # 确保分数在0-100之间
        normalized["total_score"] = max(0, min(100, normalized["total_score"]))
        normalized["skill_match"]["score"] = max(0, min(100, normalized["skill_match"]["score"]))
        normalized["experience_match"]["score"] = max(0, min(100, normalized["experience_match"]["score"]))
        normalized["position_match"]["score"] = max(0, min(100, normalized["position_match"]["score"]))
        
        return normalized
    
    def _format_resume_for_matching(self, resume_info: Dict[str, Any]) -> str:
        """
        格式化简历信息用于匹配分析
        
        Args:
            resume_info: 简历信息
            
        Returns:
            格式化后的文本
        """
        basic = resume_info.get("basic_info", {})
        job = resume_info.get("job_info", {})
        bg = resume_info.get("background", {})
        
        summary = f"""
姓名：{basic.get('name', '未知')}
求职意向：{job.get('position', '未明确')}
期望薪资：{job.get('salary', '未明确')}
工作年限：{bg.get('work_years', '未明确')}
学历背景：{bg.get('education', '未明确')}
技能：{', '.join(bg.get('skills', []))}
项目经验：{len(bg.get('projects', []))}个项目
"""
        
        return summary.strip()
