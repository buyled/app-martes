import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Base de datos
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://admin:admin123@localhost:5432/docu_api"
    )
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Aplicación
    app_name: str = "Docu API"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Render específico
    port: int = int(os.getenv("PORT", 8000))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS
    allowed_origins: list = ["*"]
    
    # Cache TTL (en segundos)
    cache_ttl_customers: int = 3600  # 1 hora
    cache_ttl_products: int = 7200   # 2 horas
    cache_ttl_orders: int = 1800     # 30 minutos
    cache_ttl_invoices: int = 1800   # 30 minutos
    cache_ttl_notices: int = 900     # 15 minutos
    
    class Config:
        env_file = ".env"

settings = Settings()