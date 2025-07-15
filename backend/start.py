#!/usr/bin/env python3
"""
Script de inicio para Render
Configura la base de datos y inicia la aplicación
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from app.core.database import Base, engine
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Configurar base de datos en Render"""
    try:
        logger.info("🔧 Configurando base de datos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Conexión a base de datos verificada")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error configurando base de datos: {e}")
        return False

def populate_sample_data():
    """Poblar con datos de ejemplo si es necesario"""
    try:
        from sqlalchemy.orm import sessionmaker
        from app.models.models import Customer
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Verificar si ya hay datos
        customer_count = session.query(Customer).count()
        session.close()
        
        if customer_count == 0:
            logger.info("📊 Base de datos vacía, poblando con datos de ejemplo...")
            from seed_data import seed_database
            seed_database()
        else:
            logger.info(f"📊 Base de datos ya contiene {customer_count} clientes")
            
    except Exception as e:
        logger.error(f"⚠️ Error poblando datos de ejemplo: {e}")

def main():
    """Función principal de inicio"""
    logger.info("🚀 Iniciando Docu API en Render...")
    logger.info(f"🌍 Entorno: {settings.environment}")
    logger.info(f"🔌 Puerto: {settings.port}")
    
    # Configurar base de datos
    if not setup_database():
        logger.error("❌ Fallo en configuración de base de datos")
        sys.exit(1)
    
    # Poblar datos de ejemplo en desarrollo
    if settings.environment == "development":
        populate_sample_data()
    
    logger.info("✅ Configuración completada")
    
    # Iniciar aplicación
    import uvicorn
    from main import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.port,
        log_level="info" if settings.debug else "warning"
    )

if __name__ == "__main__":
    main()