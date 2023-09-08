import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, SneakerCollection, SneakerModel, SneakerBrand




DATABASE_URL = "sqlite:///sneaker_collection.db"  


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

@click.group()
def cli():
    """SneakerWorld."""
    pass

@cli.command()
def browse():
    """Browse and display available sneakers."""
    
    sneakers = session.query(SneakerCollection).all()
    if sneakers:
        print("These are the sneakers in Your Collection:")
        for sneaker in sneakers:
            print(f"{sneaker.id}. {sneaker.model.brand.name} {sneaker.model.name}")
    else:
        print("There are no sneakers in your collection.")

@cli.command()
@click.argument('sneaker_id', type=int)
def view(sneaker_id):
    """View details of a specific sneaker."""
    
    sneaker = session.query(SneakerCollection).filter_by(id=sneaker_id).first()
    if sneaker:
        print(f"Sneaker ID: {sneaker.id}")
        print(f"Brand: {sneaker.model.brand.name}")
        print(f"Model: {sneaker.model.name}")
        print(f"Size: {sneaker.size}")
        print(f"Colorway: {sneaker.colorway}")
        print(f"Purchase Date: {sneaker.purchase_date}")
        print(f"Purchase Price: Ksh {sneaker.purchase_price:.2f}")
    else:
        print("Sneaker not found.")

@cli.command()
def add():
    """Add a new sneaker to your collection."""
    
    try:
        brand = input("Enter the brand of the new sneaker: ")
        model = input("Enter the model of the new sneaker: ")
        size = float(input("Enter the size of the new sneaker: "))
        colorway = input("Enter the colorway of the new sneaker: ")
        purchase_date = input("Enter the purchase date of the new sneaker (YYYY-MM-DD): ")
        purchase_price = float(input("Enter the purchase price of the new sneaker: "))

        if size <= 0 or purchase_price < 0:
            raise ValueError("Invalid size or purchase price.")

        brand_instance = session.query(SneakerBrand).filter_by(name=brand).first()
        if not brand_instance:
            brand_instance = SneakerBrand(name=brand)
            session.add(brand_instance)
            session.commit()

        model_instance = session.query(SneakerModel).filter_by(name=model, brand_id=brand_instance.id).first()
        if not model_instance:
            model_instance = SneakerModel(name=model, brand_id=brand_instance.id)
            session.add(model_instance)
            session.commit()

        sneaker = SneakerCollection(
            size=size,
            colorway=colorway,
            purchase_date=purchase_date,
            purchase_price=purchase_price,
            model_id=model_instance.id
        )

        session.add(sneaker)
        session.commit()
        print("New sneaker added to your collection.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Invalid input. Please enter valid data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@cli.command()
@click.argument('sneaker_id', type=int)
def delete(sneaker_id):
    """Delete a sneaker from the collection."""
    
    try:
        sneaker = session.query(SneakerCollection).filter_by(id=sneaker_id).first()
        if sneaker:
            session.delete(sneaker)
            session.commit()
            print("Sneaker deleted from your collection.")
        else:
            print("Sneaker not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    cli()
