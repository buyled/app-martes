"""
Endpoints de salud y monitoreo para Render
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.cache import CacheManager
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check para Render"""
    try:
        # Verificar base de datos
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Verificar cache
    cache_manager = CacheManager()
    cache_status = "healthy" if cache_manager.connected else "unhealthy"
    
    overall_status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "version": settings.app_version,
        "environment": settings.environment,
        "services": {
            "database": db_status,
            "cache": cache_status
        }
    }

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check para Render"""
    try:
        # Verificar que las tablas existen
        from app.models.models import Customer
        db.query(Customer).first()
        
        return {
            "status": "ready",
            "message": "Service is ready to accept traffic"
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {
            "status": "not_ready",
            "message": f"Service not ready: {str(e)}"
        }