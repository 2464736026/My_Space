"""
AI服务 - 使用OpenAI API处理简历分析
"""
import json
import re
import os
from typing import Dict, Any, Optional
from openai import OpenAI

# 直接从环境变量读取配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai-proxy.org/v1")
MAX_TOKENS = 2000
TEMPERATURE = 0.1
TIMEOUT = 30


# 提示词配置
SYSTEM_PROMPT = """你是一个专业的简历分析助手。你的任务是从简历文本中提取关键信息，并以JSON格式返回。

请严格按照以下JSON格式返回数据：
{
    "basic_info": {
        "name": "姓名",
        "phone": "电话号码",
        "email": "邮箱地址",
        "address": "居住地址"
    },
    "job_info": {
        "position": "目标职位",
        "salary": "期望薪资"
    },
    "background": {
        "work_years": "工作年限",
        "education": "学历背景",
        "skills": ["技能1", "技能2", "技能3"],
        "projects": ["项目1", "项目2", "项目3"]
    }
}

注意事项：
1. 如果某个字段在简历中找不到，请返回空字符串""或空数组[]
2. 技能和项目请提取最重要的，技能不超过10个，项目不超过8个
3. 项目名称要简洁，不要包含详细描述
4. 期望薪资只提取数字和单位，不要包含其他信息
5. 必须返回有效的JSON格式，不要包含任何其他文字
"""

MATCH_PROMPT_TEMPLATE = """你是一个专业的HR助手。请根据候选人简历和岗位需求，进行匹配度分析。

候选人简历信息：
{resume_info}

岗位需求：
职位名称：{job_title}
职位描述：{job_description}
技能要求：{required_skills}
经验要求：{experience_level}

请按照以下JSON格式返回分析结果：
{{
    "skill_match": {{
        "score": 85,
        "matched_skills": ["技能1", "技能2"],
        "missing_skills": ["技能3", "技能4"],
        "details": "技能匹配度分析"
    }},
    "experience_match": {{
        "score": 90,
        "resume_years": "3年",
        "required_years": "3年",
        "details": "经验匹配度分析"
    }},
    "position_match": {{
        "score": 80,
        "details": "职位匹配度分析"
    }},
    "total_score": 85,
    "recommendations": [
        "建议1",
        "建议2"
    ],
    "interview_suggestion": "强烈推荐/建议/不推荐"
}}

评分标准：
- 技能匹配度：候选人技能与岗位要求的匹配程度（0-100分）
- 经验匹配度：工作年限与要求的匹配程度（0-100分）
- 职位匹配度：求职意向与目标职位的匹配程度（0-100分）
- 综合评分：技能50% + 经验30% + 职位20%

面试建议：
- 80分以上：强烈推荐进入下一轮面试
- 60-79分：建议进入下一轮面试
- 60分以下：不推荐进入面试

请确保返回有效的JSON格式。
"""


class AIService:
    """AI服务类 - 处理所有AI相关的操作"""
    
    def __init__(self):
        """初始化OpenAI客户端"""
        print(f"Initializing AIService...")
        print(f"OPENAI_API_KEY exists: {bool(OPENAI_API_KEY)}")
        print(f"OPENAI_API_KEY length: {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}")
        print(f"OPENAI_MODEL: {OPENAI_MODEL}")
        print(f"OPENAI_BASE_URL: {OPENAI_BASE_URL}")
        
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
            error_msg = (
                "请配置 OPENAI_API_KEY 环境变量！\n"
                "获取API密钥：https://platform.openai.com/api-keys"
            )
            print(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
        
        try:
            # 初始化OpenAI客户端
            client_params = {
                "api_key": OPENAI_API_KEY,
                "timeout": TIMEOUT
            }
            
            if OPENAI_BASE_URL:
                client_params["base_url"] = OPENAI_BASE_URL
            
            print(f"Creating OpenAI client with params: {list(client_params.keys())}")
            self.client = OpenAI(**client_params)
            self.model = OPENAI_MODEL
            print("OpenAI client created successfully")
        except Exception as e:
            print(f"Failed to create OpenAI client: {str(e)}")
            raise
    
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
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
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
            prompt = MATCH_PROMPT_TEMPLATE.format(
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
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
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
