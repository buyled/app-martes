import graphene
import time
from graphene import ObjectType, String, Int, Float, List, Field, Boolean, DateTime
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.models import Customer as CustomerModel, Product as ProductModel, Order as OrderModel, Invoice as InvoiceModel, Notice as NoticeModel
import logging

logger = logging.getLogger(__name__)
Session = sessionmaker(bind=engine)

# Tipos GraphQL basados en SQLAlchemy
class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        load_instance = True

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        load_instance = True

class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        load_instance = True

class Invoice(SQLAlchemyObjectType):
    class Meta:
        model = InvoiceModel
        load_instance = True

class Notice(SQLAlchemyObjectType):
    class Meta:
        model = NoticeModel
        load_instance = True

class CacheStats(ObjectType):
    """Estadísticas del cache"""
    type = String()
    connected = Boolean()
    keys = Int()
    memory_usage = String()
    uptime = String()
    error = String()

# Queries principales
class Query(ObjectType):
    """Consultas GraphQL principales"""
    
    # Clientes
    customers = List(Customer, limit=Int(default_value=100), search=String())
    customer = Field(Customer, customer_id=Int(required=True))
    
    # Productos
    products = List(Product, limit=Int(default_value=100), search=String())
    product = Field(Product, product_id=String(required=True))
    
    # Pedidos - FUNCIONALIDAD PRINCIPAL
    orders = List(Order, limit=Int(default_value=50), customer_id=Int(), status=String())
    order = Field(Order, order_id=Int(required=True))
    orders_by_customer = List(Order, customer_id=Int(required=True))
    
    # Facturas
    invoices = List(Invoice, limit=Int(default_value=50), from_date=String())
    invoice = Field(Invoice, invoice_id=Int(required=True))
    
    # Avisos
    notices = List(Notice, limit=Int(default_value=50), status=String(), priority=String())
    notice = Field(Notice, notice_id=Int(required=True))
    
    # Cache
    cache_stats = Field(CacheStats)
    
    def resolve_customers(self, info, limit=100, search=None):
        """Resolver para lista de clientes"""
        try:
            session = Session()
            query = session.query(CustomerModel)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    (CustomerModel.business_name.ilike(search_term)) |
                    (CustomerModel.vat_number.ilike(search_term)) |
                    (CustomerModel.email.ilike(search_term))
                )
            
            customers = query.limit(limit).all()
            session.close()
            return customers
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo clientes: {e}")
            return []
    
    def resolve_customer(self, info, customer_id):
        """Resolver para cliente específico"""
        try:
            session = Session()
            customer = session.query(CustomerModel).filter(CustomerModel.customer_id == customer_id).first()
            session.close()
            return customer
        except Exception as e:
            logger.error(f"❌ Error obteniendo cliente {customer_id}: {e}")
            return None
    
    def resolve_products(self, info, limit=100, search=None):
        """Resolver para lista de productos"""
        try:
            session = Session()
            query = session.query(ProductModel)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    (ProductModel.reference.ilike(search_term)) |
                    (ProductModel.description.ilike(search_term))
                )
            
            products = query.filter(ProductModel.active == True).limit(limit).all()
            session.close()
            return products
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo productos: {e}")
            return []
    
    def resolve_product(self, info, product_id):
        """Resolver para producto específico"""
        try:
            session = Session()
            product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
            session.close()
            return product
        except Exception as e:
            logger.error(f"❌ Error obteniendo producto {product_id}: {e}")
            return None
    
    def resolve_orders(self, info, limit=50, customer_id=None, status=None):
        """Resolver para lista de pedidos - FUNCIONALIDAD PRINCIPAL"""
        try:
            cache_manager = info.context.get('cache_manager')
            
            # Crear clave de cache
            cache_key = f"orders_{limit}_{customer_id or 'all'}_{status or 'all'}"
            
            # Intentar obtener del cache
            if cache_manager:
                cached_orders = cache_manager.get(cache_key)
                if cached_orders:
                    logger.info(f"✅ Pedidos obtenidos del cache: {len(cached_orders)}")
                    return cached_orders
            
            session = Session()
            query = session.query(OrderModel)
            
            if customer_id:
                query = query.filter(OrderModel.customer_id == customer_id)
            
            if status:
                query = query.filter(OrderModel.status == status)
            
            orders = query.order_by(OrderModel.created_at.desc()).limit(limit).all()
            
            # Guardar en cache por 30 minutos
            if cache_manager and orders:
                cache_manager.set(cache_key, orders, ttl=1800)
                logger.info(f"💾 {len(orders)} pedidos guardados en cache")
            
            session.close()
            return orders
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo pedidos: {e}")
            return []
    
    def resolve_order(self, info, order_id):
        """Resolver para pedido específico"""
        try:
            session = Session()
            order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
            session.close()
            return order
        except Exception as e:
            logger.error(f"❌ Error obteniendo pedido {order_id}: {e}")
            return None
    
    def resolve_orders_by_customer(self, info, customer_id):
        """Resolver para pedidos de un cliente específico"""
        try:
            session = Session()
            orders = session.query(OrderModel).filter(OrderModel.customer_id == customer_id).order_by(OrderModel.created_at.desc()).all()
            session.close()
            return orders
        except Exception as e:
            logger.error(f"❌ Error obteniendo pedidos del cliente {customer_id}: {e}")
            return []
    
    def resolve_invoices(self, info, limit=50, from_date=None):
        """Resolver para lista de facturas"""
        try:
            session = Session()
            query = session.query(InvoiceModel)
            
            if from_date:
                query = query.filter(InvoiceModel.date >= from_date)
            
            invoices = query.order_by(InvoiceModel.date.desc()).limit(limit).all()
            session.close()
            return invoices
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo facturas: {e}")
            return []
    
    def resolve_invoice(self, info, invoice_id):
        """Resolver para factura específica"""
        try:
            session = Session()
            invoice = session.query(InvoiceModel).filter(InvoiceModel.invoice_id == invoice_id).first()
            session.close()
            return invoice
        except Exception as e:
            logger.error(f"❌ Error obteniendo factura {invoice_id}: {e}")
            return None
    
    def resolve_notices(self, info, limit=50, status=None, priority=None):
        """Resolver para lista de avisos"""
        try:
            session = Session()
            query = session.query(NoticeModel)
            
            if status:
                query = query.filter(NoticeModel.status == status)
            
            if priority:
                query = query.filter(NoticeModel.priority == priority)
            
            notices = query.order_by(NoticeModel.created_date.desc()).limit(limit).all()
            session.close()
            return notices
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo avisos: {e}")
            return []
    
    def resolve_notice(self, info, notice_id):
        """Resolver para aviso específico"""
        try:
            session = Session()
            notice = session.query(NoticeModel).filter(NoticeModel.notice_id == notice_id).first()
            session.close()
            return notice
        except Exception as e:
            logger.error(f"❌ Error obteniendo aviso {notice_id}: {e}")
            return None
    
    def resolve_cache_stats(self, info):
        """Resolver para estadísticas del cache"""
        try:
            cache_manager = info.context.get('cache_manager')
            if cache_manager:
                return cache_manager.get_stats()
            else:
                return {
                    "type": "None",
                    "connected": False,
                    "error": "Cache manager no disponible"
                }
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas del cache: {e}")
            return {
                "type": "Error",
                "connected": False,
                "error": str(e)
            }

# Mutaciones
class CreateCustomer(graphene.Mutation):
    """Mutación para crear cliente"""
    
    class Arguments:
        business_name = String(required=True)
        vat_number = String(required=True)
        name = String()
        email = String()
        street_name = String()
        postal_code = Int()
        city = String()
        province_id = Int()
        country_id = String()
        phone = String()
    
    customer = Field(Customer)
    success = Boolean()
    message = String()
    
    def mutate(self, info, business_name, vat_number, **kwargs):
        try:
            session = Session()
            
            # Verificar si ya existe
            existing = session.query(CustomerModel).filter(CustomerModel.vat_number == vat_number).first()
            if existing:
                session.close()
                return CreateCustomer(
                    success=False,
                    message=f"Ya existe un cliente con CIF {vat_number}"
                )
            
            # Crear nuevo cliente
            customer = CustomerModel(
                business_name=business_name,
                vat_number=vat_number,
                name=kwargs.get('name', business_name),
                email=kwargs.get('email', ''),
                street_name=kwargs.get('street_name', ''),
                postal_code=kwargs.get('postal_code'),
                city=kwargs.get('city', ''),
                province_id=kwargs.get('province_id'),
                country_id=kwargs.get('country_id', 'ES'),
                phone=kwargs.get('phone', '')
            )
            
            session.add(customer)
            session.commit()
            session.refresh(customer)
            
            # Limpiar cache
            cache_manager = info.context.get('cache_manager')
            if cache_manager:
                cache_manager.delete('customers_100_all')
            
            session.close()
            return CreateCustomer(
                customer=customer,
                success=True,
                message="Cliente creado exitosamente"
            )
                
        except Exception as e:
            logger.error(f"❌ Error creando cliente: {e}")
            return CreateCustomer(
                success=False,
                message=f"Error: {str(e)}"
            )

class CreateOrder(graphene.Mutation):
    """Mutación para crear pedido - FUNCIONALIDAD PRINCIPAL"""
    
    class Arguments:
        customer_id = Int(required=True)
        reference = String()
        total_amount = Float(required=True)
        status = String()
        notes = String()
    
    order = Field(Order)
    success = Boolean()
    message = String()
    
    def mutate(self, info, customer_id, total_amount, **kwargs):
        try:
            session = Session()
            
            # Verificar que existe el cliente
            customer = session.query(CustomerModel).filter(CustomerModel.customer_id == customer_id).first()
            if not customer:
                session.close()
                return CreateOrder(
                    success=False,
                    message=f"No existe cliente con ID {customer_id}"
                )
            
            # Crear nuevo pedido
            order = OrderModel(
                customer_id=customer_id,
                reference=kwargs.get('reference', f"ORD-{customer_id}-{int(time.time())}"),
                total_amount=total_amount,
                status=kwargs.get('status', 'pending'),
                notes=kwargs.get('notes', '')
            )
            
            session.add(order)
            session.commit()
            session.refresh(order)
            
            # Limpiar cache de pedidos
            cache_manager = info.context.get('cache_manager')
            if cache_manager:
                cache_manager.delete('orders_50_all_all')
                cache_manager.delete(f'orders_50_{customer_id}_all')
            
            session.close()
            return CreateOrder(
                order=order,
                success=True,
                message="Pedido creado exitosamente"
            )
                
        except Exception as e:
            logger.error(f"❌ Error creando pedido: {e}")
            return CreateOrder(
                success=False,
                message=f"Error: {str(e)}"
            )

class Mutations(ObjectType):
    """Mutaciones disponibles"""
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()

# Schema principal
schema = graphene.Schema(query=Query, mutation=Mutations)