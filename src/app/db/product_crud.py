from sqlalchemy.orm import Session
from datetime import datetime

from app.api.models import Product, ProductSchema


def post(db_session: Session, payload: ProductSchema):
    product = Product(title=payload.title, description=payload.description, productOwner=payload.productOwner, createdBy=payload.createdBy, updatedBy=payload.updatedBy, updatedDate=payload.updatedDate)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def get(db_session: Session, id: int):
    return db_session.query(Product).filter(Product.id == id).first()


def get_all(db_session: Session):
    return db_session.query(Product).all()


def put(db_session: Session, product: Product, title: str, description: str, productOwner: str, createdBy: str, updatedBy: str, updatedDate: datetime):
    product.title = title
    product.description = description
    product.productOwner = productOwner
    product.createdBy = createdBy
    product.updatedBy = updatedBy,
    product.updatedDate = updatedDate
    db_session.commit()
    return product


def delete(db_session: Session, id: int):
    product = db_session.query(Product).filter(Product.id == id).first()
    db_session.delete(product)
    db_session.commit()
    return product
