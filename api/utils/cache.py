import json
import hashlib
import time
from typing import Dict, Any, Optional

class CacheManager:
    """缓存管理器（内存缓存实现）"""
    
    def __init__(self):
        self._cache = {}
        self._expire_times = {}
        self.default_ttl = 3600  # 1小时过期
    
    def cache_resume(self, extracted_info: Dict[str, Any], text_content: str) -> str:
        """缓存简历信息，返回简历ID"""
        # 生成简历ID
        resume_id = self._generate_resume_id(text_content)
        
        # 缓存数据
        cache_data = {
            "extracted_info": extracted_info,
            "text_content": text_content,
            "created_at": time.time()
        }
        
        self._cache[resume_id] = cache_data
        self._expire_times[resume_id] = time.time() + self.default_ttl
        
        return resume_id
    
    def get_resume(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """获取缓存的简历信息"""
        # 检查是否过期
        if resume_id in self._expire_times:
            if time.time() > self._expire_times[resume_id]:
                self._remove_expired(resume_id)
                return None
        
        return self._cache.get(resume_id)
    
    def _generate_resume_id(self, text_content: str) -> str:
        """生成简历ID"""
        # 使用文本内容的哈希值作为ID
        hash_object = hashlib.md5(text_content.encode())
        return hash_object.hexdigest()[:16]
    
    def _remove_expired(self, resume_id: str):
        """移除过期的缓存"""
        if resume_id in self._cache:
            del self._cache[resume_id]
        if resume_id in self._expire_times:
            del self._expire_times[resume_id]
    
    def clear_expired(self):
        """清理所有过期的缓存"""
        current_time = time.time()
        expired_keys = [
            key for key, expire_time in self._expire_times.items()
            if current_time > expire_time
        ]
        
        for key in expired_keys:
            self._remove_expired(key)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        self.clear_expired()  # 先清理过期缓存
        
        return {
            "total_items": len(self._cache),
            "memory_usage": sum(len(str(data)) for data in self._cache.values()),
            "oldest_item": min(
                (data["created_at"] for data in self._cache.values()),
                default=None
            )
        }