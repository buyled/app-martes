from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Customer(Base):
    """Modelo de Cliente"""
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(100), nullable=False)
    name = Column(String(100))
    email = Column(String(60))
    vat_number = Column(String(18), unique=True)
    street_name = Column(String(55))
    postal_code = Column(Integer)
    city = Column(String(30))
    province_id = Column(Integer)
    country_id = Column(String(2), default="ES")
    phone = Column(String(18))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    orders = relationship("Order", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")

class Product(Base):
    """Modelo de Producto"""
    __tablename__ = "products"
    
    product_id = Column(String(24), primary_key=True, index=True)
    reference = Column(String(50))
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Order(Base):
    """Modelo de Pedido"""
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime(timezone=True))
    delivery_date = Column(DateTime(timezone=True))
    total_amount = Column(Float)
    status = Column(String(20), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """Modelo de Item de Pedido"""
    __tablename__ = "order_items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(String(24), ForeignKey("products.product_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    
    # Relaciones
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

class Invoice(Base):
    """Modelo de Factura"""
    __tablename__ = "invoices"
    
    invoice_id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    customer_name = Column(String(100))
    amount = Column(Float)
    date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    status = Column(String(20), default="pending")  # pending, paid, overdue, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    customer = relationship("Customer", back_populates="invoices")

class Notice(Base):
    """Modelo de Aviso/Notificación"""
    __tablename__ = "notices"
    
    notice_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    title = Column(String(100))
    description = Column(Text)
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    status = Column(String(20), default="open")  # open, in_progress, resolved, closed
    assigned_to = Column(String(50))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    resolution = Column(Text)
    resolved_date = Column(DateTime(timezone=True))
    
    # Relaciones
    customer = relationship("Customer")