# 🚀 Despliegue en Render - Docu API

Guía completa para desplegar la aplicación Docu API en Render como web service.

## 📋 Requisitos Previos

1. Cuenta en [Render](https://render.com)
2. Repositorio Git con el código
3. Archivo `render.yaml` configurado (✅ incluido)

## 🔧 Configuración Automática

### Opción 1: Despliegue con render.yaml (Recomendado)

1. **Conectar repositorio a Render**
   - Ve a tu dashboard de Render
   - Clic en "New" → "Blueprint"
   - Conecta tu repositorio GitHub
   - Render detectará automáticamente el `render.yaml`

2. **Servicios que se crearán automáticamente:**
   - ✅ **Web Service**: `docu-api-backend` (Python/FastAPI)
   - ✅ **PostgreSQL**: `docu-api-db` (Base de datos)
   - ✅ **Redis**: `docu-api-redis` (Cache)

### Opción 2: Configuración Manual

Si prefieres configurar manualmente:

#### 1. Crear Base de Datos PostgreSQL
```
Nombre: docu-api-db
Plan: Starter (Gratis)
Región: Oregon
Database: docu_api
User: admin
```

#### 2. Crear Redis
```
Nombre: docu-api-redis
Plan: Starter (Gratis)
Región: Oregon
```

#### 3. Crear Web Service
```
Nombre: docu-api-backend
Entorno: Python 3.11
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && python start.py
```

## 🌍 Variables de Entorno

Las siguientes variables se configuran automáticamente:

```bash
DATABASE_URL=postgresql://... (automático desde PostgreSQL)
REDIS_URL=redis://... (automático desde Redis)
ENVIRONMENT=production
DEBUG=false
PYTHON_VERSION=3.11.0
```

## 📊 Funcionalidades Incluidas

### 🛒 Gestión de Pedidos (Funcionalidad Principal)
- **1,907 pedidos** disponibles (basado en archivos MCP)
- CRUD completo de pedidos
- Búsqueda por cliente
- Estados: pending, confirmed, shipped, delivered

### 👥 Gestión de Clientes
- Registro y actualización de clientes
- Búsqueda por nombre, CIF, email
- Historial de pedidos por cliente

### 📦 Gestión de Productos
- Catálogo de productos
- Control de stock
- Precios y referencias

### 💰 Gestión de Facturas
- Facturación automática
- Estados de pago
- Fechas de vencimiento

### 📢 Gestión de Avisos
- Sistema de notificaciones
- Prioridades y estados
- Asignación a empleados

## 🔗 Endpoints Principales

Una vez desplegado, tendrás acceso a:

```
https://tu-app.onrender.com/
├── /                    # Información de la API
├── /health             # Health check
├── /ready              # Readiness check
├── /stats              # Estadísticas del sistema
└── /graphql            # Endpoint GraphQL principal
```

## 📝 Consultas GraphQL de Ejemplo

### Obtener Pedidos
```graphql
query GetOrders {
  orders(limit: 10) {
    orderId
    reference
    customer {
      businessName
      email
    }
    totalAmount
    status
    orderDate
  }
}
```

### Crear Pedido
```graphql
mutation CreateOrder {
  createOrder(
    customerId: 1
    totalAmount: 1500.00
    reference: "ORD-2025-001"
    status: "pending"
  ) {
    success
    message
    order {
      orderId
      reference
      totalAmount
    }
  }
}
```

### Buscar Pedidos por Cliente
```graphql
query GetOrdersByCustomer {
  ordersByCustomer(customerId: 1) {
    orderId
    reference
    totalAmount
    status
    orderDate
  }
}
```

## 🚀 Proceso de Despliegue

1. **Push al repositorio**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Render detecta cambios automáticamente**
   - Build automático
   - Despliegue automático
   - Health checks

3. **Verificación**
   - Visita `https://tu-app.onrender.com/health`
   - Debe retornar `{"status": "healthy"}`

## 📈 Monitoreo

### Health Checks
- **Health**: `/health` - Estado general
- **Ready**: `/ready` - Listo para tráfico
- **Stats**: `/stats` - Estadísticas detalladas

### Logs
```bash
# Ver logs en tiempo real desde Render Dashboard
# O usar Render CLI
render logs -s docu-api-backend
```

## 🔧 Troubleshooting

### Problemas Comunes

1. **Error de conexión a BD**
   - Verificar que PostgreSQL esté running
   - Revisar DATABASE_URL en variables de entorno

2. **Error de Redis**
   - Verificar que Redis esté running
   - Revisar REDIS_URL en variables de entorno

3. **Build failures**
   - Verificar requirements.txt
   - Revisar logs de build en Render

### Comandos de Debug
```bash
# Verificar estado de servicios
curl https://tu-app.onrender.com/health

# Verificar GraphQL
curl -X POST https://tu-app.onrender.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

## 📚 Documentación Adicional

- [Render Docs](https://render.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [GraphQL Docs](https://graphql.org/learn/)

## 🎉 ¡Listo!

Tu aplicación Docu API estará disponible en:
`https://docu-api-backend.onrender.com`

Con todas las funcionalidades de gestión de pedidos, clientes, productos, facturas y avisos funcionando completamente.