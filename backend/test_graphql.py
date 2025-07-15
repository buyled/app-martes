#!/usr/bin/env python3
"""
Script de prueba para verificar que la API GraphQL funciona correctamente
Incluye pruebas específicas para la funcionalidad de pedidos (MCP)
"""

import requests
import json
import sys

def test_graphql_endpoint(base_url="http://localhost:8000"):
    """Probar el endpoint GraphQL"""
    
    graphql_url = f"{base_url}/graphql"
    
    print("🧪 Iniciando pruebas de GraphQL...")
    print(f"🔗 URL: {graphql_url}")
    
    # Test 1: Verificar que el endpoint responde
    print("\n1️⃣ Verificando endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Endpoint de salud responde correctamente")
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
        else:
            print(f"❌ Error en endpoint de salud: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False
    
    # Test 2: Schema introspection
    print("\n2️⃣ Verificando schema GraphQL...")
    introspection_query = {
        "query": """
        query IntrospectionQuery {
            __schema {
                types {
                    name
                    kind
                }
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=introspection_query)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and '__schema' in data['data']:
                types = [t['name'] for t in data['data']['__schema']['types'] if not t['name'].startswith('__')]
                print(f"✅ Schema GraphQL cargado correctamente")
                print(f"   Tipos disponibles: {', '.join(types[:10])}...")
            else:
                print("❌ Error en respuesta del schema")
                return False
        else:
            print(f"❌ Error en introspección: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en introspección: {e}")
        return False
    
    # Test 3: Consultar clientes
    print("\n3️⃣ Probando consulta de clientes...")
    customers_query = {
        "query": """
        query GetCustomers {
            customers(limit: 5) {
                customerId
                businessName
                vatNumber
                email
                city
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=customers_query)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'customers' in data['data']:
                customers = data['data']['customers']
                print(f"✅ Consulta de clientes exitosa: {len(customers)} clientes")
                if customers:
                    print(f"   Ejemplo: {customers[0]['businessName']}")
            else:
                print("❌ Error en consulta de clientes")
                print(f"   Respuesta: {data}")
        else:
            print(f"❌ Error HTTP en clientes: {response.status_code}")
    except Exception as e:
        print(f"❌ Error consultando clientes: {e}")
    
    # Test 4: Consultar productos
    print("\n4️⃣ Probando consulta de productos...")
    products_query = {
        "query": """
        query GetProducts {
            products(limit: 5) {
                productId
                reference
                description
                price
                stock
                active
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=products_query)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'products' in data['data']:
                products = data['data']['products']
                print(f"✅ Consulta de productos exitosa: {len(products)} productos")
                if products:
                    print(f"   Ejemplo: {products[0]['description'][:50]}...")
            else:
                print("❌ Error en consulta de productos")
        else:
            print(f"❌ Error HTTP en productos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error consultando productos: {e}")
    
    # Test 5: Consultar pedidos (FUNCIONALIDAD PRINCIPAL)
    print("\n5️⃣ Probando consulta de pedidos (FUNCIONALIDAD PRINCIPAL)...")
    orders_query = {
        "query": """
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
                notes
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=orders_query)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'orders' in data['data']:
                orders = data['data']['orders']
                print(f"✅ Consulta de pedidos exitosa: {len(orders)} pedidos")
                if orders:
                    order = orders[0]
                    print(f"   Ejemplo: {order['reference']} - {order['customer']['businessName']} - €{order['totalAmount']}")
                    print(f"   Estado: {order['status']}")
            else:
                print("❌ Error en consulta de pedidos")
                print(f"   Respuesta: {data}")
        else:
            print(f"❌ Error HTTP en pedidos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error consultando pedidos: {e}")
    
    # Test 6: Crear un pedido nuevo
    print("\n6️⃣ Probando creación de pedido...")
    create_order_mutation = {
        "query": """
        mutation CreateTestOrder {
            createOrder(
                customerId: 1
                totalAmount: 999.99
                reference: "TEST-ORDER-001"
                status: "pending"
                notes: "Pedido de prueba desde script de testing"
            ) {
                success
                message
                order {
                    orderId
                    reference
                    totalAmount
                    status
                }
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=create_order_mutation)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'createOrder' in data['data']:
                result = data['data']['createOrder']
                if result['success']:
                    print(f"✅ Pedido creado exitosamente: {result['order']['reference']}")
                    print(f"   ID: {result['order']['orderId']}")
                    print(f"   Monto: €{result['order']['totalAmount']}")
                else:
                    print(f"❌ Error creando pedido: {result['message']}")
            else:
                print("❌ Error en mutación de pedido")
                print(f"   Respuesta: {data}")
        else:
            print(f"❌ Error HTTP creando pedido: {response.status_code}")
    except Exception as e:
        print(f"❌ Error creando pedido: {e}")
    
    # Test 7: Estadísticas del cache
    print("\n7️⃣ Probando estadísticas del cache...")
    cache_query = {
        "query": """
        query GetCacheStats {
            cacheStats {
                type
                connected
                keys
                memoryUsage
                uptime
                error
            }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=cache_query)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'cacheStats' in data['data']:
                stats = data['data']['cacheStats']
                print(f"✅ Estadísticas del cache obtenidas")
                print(f"   Tipo: {stats['type']}")
                print(f"   Conectado: {stats['connected']}")
                if stats['connected']:
                    print(f"   Claves: {stats['keys']}")
                    print(f"   Memoria: {stats['memoryUsage']}")
            else:
                print("❌ Error obteniendo estadísticas del cache")
        else:
            print(f"❌ Error HTTP en cache: {response.status_code}")
    except Exception as e:
        print(f"❌ Error consultando cache: {e}")
    
    print("\n🎉 Pruebas completadas!")
    return True

def test_render_deployment(render_url):
    """Probar despliegue en Render"""
    print(f"\n🚀 Probando despliegue en Render: {render_url}")
    return test_graphql_endpoint(render_url)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # URL personalizada (para Render)
        url = sys.argv[1]
        print(f"🌐 Probando URL personalizada: {url}")
        test_graphql_endpoint(url)
    else:
        # Desarrollo local
        print("🏠 Probando desarrollo local")
        test_graphql_endpoint()
    
    print("\n📋 Comandos útiles:")
    print("   Desarrollo local: python test_graphql.py")
    print("   Render: python test_graphql.py https://tu-app.onrender.com")
    print("   Health check: curl https://tu-app.onrender.com/health")
    print("   GraphQL Playground: https://tu-app.onrender.com/graphql")