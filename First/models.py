from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Holding(Base):
    __tablename__ = 'holdings'
    
    id = Column(Integer, primary_key=True)
    main_holding_key = Column(String(50), nullable=False)
    main_holding_name = Column(String(255), nullable=False)
    holding_key = Column(String(50), nullable=False)
    holding_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    brands = relationship("Brand", back_populates="holding")

class Brand(Base):
    __tablename__ = 'brands'
    
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(255), nullable=False)
    holding_id = Column(Integer, ForeignKey('holdings.id'))
    sector_key = Column(String(50))
    sector_description = Column(String(255))
    department_key = Column(String(50))
    department_description = Column(String(255))
    group_class_key = Column(String(255))
    class_key = Column(String(255))
    ownership_status = Column(String(50))  # 'OK' ou 'NON'
    verification_date = Column(DateTime, default=datetime.utcnow)
    country = Column(String(50), default='France')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    holding = relationship("Holding", back_populates="brands")
    sub_brands = relationship("BrandHierarchy", back_populates="parent_brand")

class BrandHierarchy(Base):
    __tablename__ = 'brand_hierarchy'
    
    id = Column(Integer, primary_key=True)
    parent_brand_id = Column(Integer, ForeignKey('brands.id'))
    sub_brand_name = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent_brand = relationship("Brand", back_populates="sub_brands")

class MissingBrand(Base):
    __tablename__ = 'missing_brands'
    
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(255), nullable=False)
    holding_id = Column(Integer, ForeignKey('holdings.id'))
    sector_key = Column(String(50))
    department_key = Column(String(50))
    discovery_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))  # 'Pending', 'Added', 'Rejected'
    country = Column(String(50), default='France')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    holding = relationship("Holding") 