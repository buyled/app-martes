"""
Script para poblar la base de datos con datos de ejemplo
Incluye datos de prueba para pedidos basados en los archivos MCP
"""

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Customer, Product, Order, OrderItem, Invoice, Notice
from datetime import datetime, timedelta
import random

Session = sessionmaker(bind=engine)

def seed_database():
    """Poblar base de datos con datos de ejemplo"""
    session = Session()
    
    try:
        print("🌱 Iniciando población de base de datos...")
        
        # Limpiar datos existentes
        session.query(OrderItem).delete()
        session.query(Order).delete()
        session.query(Invoice).delete()
        session.query(Notice).delete()
        session.query(Product).delete()
        session.query(Customer).delete()
        session.commit()
        
        # 1. Crear clientes de ejemplo
        customers_data = [
            {
                "business_name": "SUÑE SOLUCIONES INTEGRALES SL",
                "vat_number": "B12345678",
                "name": "Juan Suñe",
                "email": "info@sune.es",
                "street_name": "Calle Mayor 123",
                "postal_code": 28001,
                "city": "Madrid",
                "phone": "912345678"
            },
            {
                "business_name": "TECNOLOGÍA AVANZADA SA",
                "vat_number": "A87654321",
                "name": "María García",
                "email": "contacto@tecavanzada.com",
                "street_name": "Avenida Tecnología 45",
                "postal_code": 8001,
                "city": "Barcelona",
                "phone": "934567890"
            },
            {
                "business_name": "DISTRIBUCIONES LÓPEZ SL",
                "vat_number": "B11223344",
                "name": "Carlos López",
                "email": "pedidos@distlopez.es",
                "street_name": "Polígono Industrial 67",
                "postal_code": 41001,
                "city": "Sevilla",
                "phone": "954123456"
            }
        ]
        
        customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            session.add(customer)
            customers.append(customer)
        
        session.commit()
        print(f"✅ Creados {len(customers)} clientes")
        
        # 2. Crear productos de ejemplo
        products_data = [
            {
                "product_id": "PROD001",
                "reference": "REF-001",
                "description": "Sistema de gestión empresarial completo",
                "price": 1500.00,
                "stock": 10
            },
            {
                "product_id": "PROD002", 
                "reference": "REF-002",
                "description": "Módulo de facturación electrónica",
                "price": 750.00,
                "stock": 25
            },
            {
                "product_id": "PROD003",
                "reference": "REF-003", 
                "description": "Licencia software de inventario",
                "price": 450.00,
                "stock": 50
            },
            {
                "product_id": "PROD004",
                "reference": "REF-004",
                "description": "Servicio de consultoría técnica",
                "price": 120.00,
                "stock": 100
            },
            {
                "product_id": "PROD005",
                "reference": "REF-005",
                "description": "Mantenimiento anual del sistema",
                "price": 300.00,
                "stock": 30
            }
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            session.add(product)
            products.append(product)
        
        session.commit()
        print(f"✅ Creados {len(products)} productos")
        
        # 3. Crear pedidos de ejemplo (basado en los 1,907 pedidos de MCP)
        orders_data = []
        statuses = ["pending", "confirmed", "shipped", "delivered"]
        
        for i in range(20):  # Crear 20 pedidos de ejemplo
            customer = random.choice(customers)
            order_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            order = Order(
                reference=f"ORD-{2025}-{1000 + i}",
                customer_id=customer.customer_id,
                order_date=order_date,
                delivery_date=order_date + timedelta(days=random.randint(3, 15)),
                total_amount=random.uniform(500, 5000),
                status=random.choice(statuses),
                notes=f"Pedido de ejemplo #{i+1} para {customer.business_name}"
            )
            session.add(order)
            orders_data.append(order)
        
        session.commit()
        print(f"✅ Creados {len(orders_data)} pedidos")
        
        # 4. Crear items de pedidos
        order_items = []
        for order in orders_data:
            # Cada pedido tendrá entre 1 y 4 items
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                quantity = random.randint(1, 5)
                unit_price = product.price
                total_price = quantity * unit_price
                
                item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                session.add(item)
                order_items.append(item)
        
        session.commit()
        print(f"✅ Creados {len(order_items)} items de pedidos")
        
        # 5. Crear facturas de ejemplo
        invoices_data = []
        for i, order in enumerate(orders_data[:15]):  # Facturar 15 pedidos
            if order.status in ["delivered", "shipped"]:
                invoice = Invoice(
                    reference=f"FAC-{2025}-{2000 + i}",
                    customer_id=order.customer_id,
                    customer_name=order.customer.business_name,
                    amount=order.total_amount,
                    date=order.delivery_date + timedelta(days=1),
                    due_date=order.delivery_date + timedelta(days=31),
                    status="paid" if random.choice([True, False]) else "pending"
                )
                session.add(invoice)
                invoices_data.append(invoice)
        
        session.commit()
        print(f"✅ Creadas {len(invoices_data)} facturas")
        
        # 6. Crear avisos de ejemplo
        notices_data = []
        priorities = ["low", "medium", "high", "urgent"]
        statuses = ["open", "in_progress", "resolved", "closed"]
        
        for i in range(15):
            customer = random.choice(customers)
            created_date = datetime.now() - timedelta(days=random.randint(1, 30))
            
            notice = Notice(
                customer_id=customer.customer_id,
                title=f"Aviso #{i+1} - {customer.business_name}",
                description=f"Descripción del aviso de ejemplo para {customer.business_name}. Requiere atención.",
                priority=random.choice(priorities),
                status=random.choice(statuses),
                assigned_to=f"empleado{random.randint(1, 5)}",
                created_date=created_date,
                due_date=created_date + timedelta(days=random.randint(1, 14))
            )
            session.add(notice)
            notices_data.append(notice)
        
        session.commit()
        print(f"✅ Creados {len(notices_data)} avisos")
        
        print("\n🎉 Base de datos poblada exitosamente!")
        print(f"📊 Resumen:")
        print(f"   👥 Clientes: {len(customers)}")
        print(f"   📦 Productos: {len(products)}")
        print(f"   🛒 Pedidos: {len(orders_data)}")
        print(f"   📋 Items de pedidos: {len(order_items)}")
        print(f"   💰 Facturas: {len(invoices_data)}")
        print(f"   📢 Avisos: {len(notices_data)}")
        
    except Exception as e:
        print(f"❌ Error poblando base de datos: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()