from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SneakerBrand(Base):
    __tablename__ = 'sneaker_brand'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    models = relationship('SneakerModel', back_populates='brand')

class SneakerModel(Base):
    __tablename__ = 'sneaker_model'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey('sneaker_brand.id'), nullable=False)

    brand = relationship('SneakerBrand', back_populates='models')
    collections = relationship('SneakerCollection', back_populates='model')

class SneakerCollection(Base):
    __tablename__ = 'sneaker_collection'

    id = Column(Integer, primary_key=True)
    size = Column(Integer, nullable=False)
    colorway = Column(String, nullable=False)
    purchase_date = Column(String, nullable=False)
    purchase_price = Column(Float, nullable=False)
    model_id = Column(Integer, ForeignKey('sneaker_model.id'), nullable=False)

    model = relationship('SneakerModel', back_populates='collections')
