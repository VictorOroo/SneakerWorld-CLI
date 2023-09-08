from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
from app.models import Base, SneakerBrand, SneakerModel, SneakerCollection



DATABASE_URL = "sqlite:///sneaker_collection.db"  


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Base = declarative_base()

# sneaker models

# class SneakerBrand(Base):
#     __tablename__ = 'sneaker_brand'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)

#     models = relationship('SneakerModel', back_populates='brand')

# class SneakerModel(Base):
#     __tablename__ = 'sneaker_model'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     brand_id = Column(Integer, ForeignKey('sneaker_brand.id'), nullable=False)

#     brand = relationship('SneakerBrand', back_populates='models')
#     collections = relationship('SneakerCollection', back_populates='model')

# class SneakerCollection(Base):
#     __tablename__ = 'sneaker_collection'

#     id = Column(Integer, primary_key=True)
#     size = Column(Integer, nullable=False)
#     colorway = Column(String, nullable=False)
#     purchase_date = Column(String, nullable=False)
#     purchase_price = Column(Float, nullable=False)
#     model_id = Column(Integer, ForeignKey('sneaker_model.id'), nullable=False)

#     model = relationship('SneakerModel', back_populates='collections')

# this are the functions which will interact with the database

def create_sneaker(brand, model, size, colorway, purchase_date, purchase_price):
    """Create a new sneaker in the database."""
    brand_instance = SneakerBrand(name=brand)
    model_instance = SneakerModel(name=model, brand=brand_instance)
    sneaker = SneakerCollection(
        size=size,
        colorway=colorway,
        purchase_date=purchase_date,
        purchase_price=purchase_price,
        model=model_instance
    )

    session.add(sneaker)
    session.commit()
    return sneaker

def get_sneakers():
    """Retrieve all sneakers from the database."""
    return session.query(SneakerCollection).all()

def get_sneaker_by_id(sneaker_id):
    """Retrieve a sneaker by its ID from the database."""
    return session.query(SneakerCollection).filter_by(id=sneaker_id).first()

def update_sneaker_info(sneaker, new_brand, new_model, new_size, new_colorway, new_purchase_date, new_purchase_price):
    """Update a sneaker's information in the database."""
    sneaker.model.brand.name = new_brand
    sneaker.model.name = new_model
    sneaker.size = new_size
    sneaker.colorway = new_colorway
    sneaker.purchase_date = new_purchase_date
    sneaker.purchase_price = new_purchase_price

    session.commit()

def delete_sneaker(sneaker):
    """Delete a sneaker from the database."""
    session.delete(sneaker)
    session.commit()


def initialize_database():
    Base.metadata.create_all(engine)


initialize_database()
