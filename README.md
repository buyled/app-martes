# 🚀 Docu API - Sistema de Gestión Completo

Aplicación web completa para gestión de **pedidos**, avisos, clientes, productos y facturas con GraphQL. Basado en los datos de prueba de pedidos MCP con **1,907 pedidos** disponibles.

## ✨ Funcionalidades Principales

### 🛒 **Gestión de Pedidos** (Funcionalidad Principal)
- **1,907 pedidos** disponibles (basado en archivos MCP)
- CRUD completo de pedidos
- Estados: pending, confirmed, shipped, delivered
- Búsqueda por cliente y estado
- Historial completo de pedidos

### 👥 **Gestión de Clientes**
- Registro y actualización de clientes
- Búsqueda por nombre, CIF, email
- Historial de pedidos por cliente

### 📦 **Gestión de Productos**
- Catálogo completo de productos
- Control de stock y precios
- Referencias y descripciones

### 💰 **Gestión de Facturas**
- Facturación automática desde pedidos
- Estados de pago y vencimientos
- Historial de facturación

### 📢 **Gestión de Avisos**
- Sistema de notificaciones
- Prioridades y estados
- Asignación a empleados

## 🛠 Tecnologías

- **Backend**: FastAPI + GraphQL (Graphene)
- **Base de datos**: PostgreSQL
- **Cache**: Redis
- **Despliegue**: Render (Web Service)
- **ORM**: SQLAlchemy

## 📁 Estructura del Proyecto

```
docu-api/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints REST
│   │   ├── core/         # Configuración y DB
│   │   ├── models/       # Modelos SQLAlchemy
│   │   └── schemas/      # Esquemas GraphQL
│   ├── requirements.txt
│   ├── main.py          # Aplicación principal
│   ├── start.py         # Script de inicio para Render
│   └── seed_data.py     # Datos de ejemplo
├── render.yaml          # Configuración de Render
├── docker-compose.yml   # Desarrollo local
└── DEPLOY_RENDER.md     # Guía de despliegue
```

## 🚀 Despliegue en Render

### Opción 1: Despliegue Automático (Recomendado)
1. Fork este repositorio
2. Conecta tu repositorio a [Render](https://render.com)
3. Render detectará automáticamente el `render.yaml`
4. ¡Listo! Tu API estará disponible en minutos

### Servicios que se crean automáticamente:
- ✅ **Web Service**: Backend FastAPI + GraphQL
- ✅ **PostgreSQL**: Base de datos principal
- ✅ **Redis**: Sistema de cache

Ver [DEPLOY_RENDER.md](DEPLOY_RENDER.md) para guía completa.

## 💻 Desarrollo Local

### Con Docker (Recomendado)
```bash
# Clonar repositorio
git clone https://github.com/buyled/docu-api.git
cd docu-api

# Iniciar servicios
docker-compose up -d

# La API estará disponible en:
# http://localhost:8000/graphql
```

### Sin Docker
```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://admin:admin123@localhost:5432/docu_api"
export REDIS_URL="redis://localhost:6379"

# Poblar base de datos
python seed_data.py

# Iniciar aplicación
python main.py
```

## 📊 API GraphQL

### Endpoints Principales
- **GraphQL**: `/graphql` - Endpoint principal
- **Health**: `/health` - Estado del sistema
- **Stats**: `/stats` - Estadísticas detalladas

### Consultas de Ejemplo

#### Obtener Pedidos
```graphql
query GetOrders {
  orders(limit: 10, status: "pending") {
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

#### Crear Pedido
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

#### Pedidos por Cliente
```graphql
query GetOrdersByCustomer {
  ordersByCustomer(customerId: 1) {
    orderId
    reference
    totalAmount
    status
    orderDate
    orderItems {
      product {
        description
      }
      quantity
      unitPrice
    }
  }
}
```

## 📈 Datos de Prueba

La aplicación incluye datos de ejemplo basados en los archivos MCP:

- **👥 Clientes**: 3 empresas de ejemplo
- **📦 Productos**: 5 productos con stock
- **🛒 Pedidos**: 20 pedidos con diferentes estados
- **💰 Facturas**: 15 facturas generadas
- **📢 Avisos**: 15 avisos de diferentes prioridades

## 🔧 Configuración

### Variables de Entorno
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
ENVIRONMENT=production|development
DEBUG=true|false
PORT=8000
```

### Cache TTL (Tiempo de vida)
- Clientes: 1 hora
- Productos: 2 horas  
- Pedidos: 30 minutos
- Facturas: 30 minutos
- Avisos: 15 minutos

## 📚 Documentación

- [Guía de Despliegue en Render](DEPLOY_RENDER.md)
- [Documentación Técnica Completa](DOCUMENTACION_TECNICA_COMPLETA%20(2).pdf)
- [Esquema GraphQL](graphql_schema.py)
- [Mapeo de Tablas](TablasGraphQL_comas_utf8.txt)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🎯 Estado del Proyecto

- ✅ **Backend GraphQL**: Completamente funcional
- ✅ **Gestión de Pedidos**: Implementada con datos MCP
- ✅ **Base de datos**: PostgreSQL configurada
- ✅ **Cache**: Redis implementado
- ✅ **Despliegue**: Listo para Render
- 🔄 **Frontend**: En desarrollo
- 🔄 **Autenticación**: Planificada

---

**Desarrollado con ❤️ para gestión empresarial moderna**