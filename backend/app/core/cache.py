import os
import redis
import json
import logging
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class CacheManager:
    """Gestor de cache con Redis"""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        """Conectar a Redis"""
        try:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.client.ping()
            self.connected = True
            logger.info("✅ Conectado a Redis")
        except Exception as e:
            logger.error(f"❌ Error conectando a Redis: {e}")
            self.connected = False
    
    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del cache"""
        if not self.connected:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"❌ Error obteniendo del cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Guardar valor en cache"""
        if not self.connected:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando en cache: {e}")
            return False
    
    def delete(self, key: str):
        """Eliminar del cache"""
        if not self.connected:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"❌ Error eliminando del cache: {e}")
            return False
    
    def get_stats(self):
        """Obtener estadísticas del cache"""
        if not self.connected:
            return {
                "type": "Redis",
                "connected": False,
                "error": "No conectado"
            }
        
        try:
            info = self.client.info()
            return {
                "type": "Redis",
                "connected": True,
                "keys": self.client.dbsize(),
                "memory_usage": f"{info.get('used_memory_human', 'N/A')}",
                "uptime": f"{info.get('uptime_in_seconds', 0)} segundos"
            }
        except Exception as e:
            return {
                "type": "Redis",
                "connected": False,
                "error": str(e)
            }