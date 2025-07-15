import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.core.database import engine, Base
from app.core.cache import CacheManager
from app.schemas.graphql_schema import schema
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Docu API - Sistema de Gestión de Avisos y Pedidos",
    description="API GraphQL completa para gestión de avisos, clientes, productos, pedidos y facturas",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar cache
cache_manager = CacheManager()

# Contexto para GraphQL
def get_context():
    return {
        'cache_manager': cache_manager,
        'db': engine
    }

# Configurar GraphQL
graphql_app = GraphQLApp(
    schema=schema,
    context_value=get_context,
    on_get=make_playground_handler()
)

app.mount("/graphql", graphql_app)

@app.get("/")
async def root():
    return {
        "message": "Docu API - Sistema de Gestión Completo",
        "description": "API GraphQL para gestión de avisos, clientes, productos, pedidos y facturas",
        "graphql_endpoint": "/graphql",
        "version": "2.0.0",
        "features": [
            "✅ Gestión de Clientes",
            "✅ Gestión de Productos", 
            "✅ Gestión de Pedidos (Funcionalidad Principal)",
            "✅ Gestión de Facturas",
            "✅ Gestión de Avisos/Notificaciones",
            "✅ Sistema de Cache con Redis",
            "✅ API GraphQL Completa"
        ]
    }

@app.get("/health")
async def health_check():
    cache_status = "connected" if cache_manager.connected else "disconnected"
    return {
        "status": "healthy",
        "database": "connected",
        "cache": cache_status,
        "version": "2.0.0"
    }

@app.get("/stats")
async def get_stats():
    """Endpoint para obtener estadísticas del sistema"""
    try:
        cache_stats = cache_manager.get_stats()
        return {
            "system": "Docu API",
            "version": "2.0.0",
            "cache": cache_stats,
            "endpoints": {
                "graphql": "/graphql",
                "health": "/health",
                "stats": "/stats"
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)