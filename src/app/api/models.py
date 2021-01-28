from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.db_factory import Base


# SQLAlchemy Model
class Product(Base):

    __tablename__ = "products"
    issues = relationship("Issue", cascade="all, delete-orphan")

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    productOwner = Column(String(100))
    createdDate = Column(DateTime, default=func.now(), nullable=False)
    updatedDate = Column(DateTime, default=func.now(), nullable=False)
    createdBy = Column(String(100))
    updatedBy = Column(String(100))

    def __init__(self, title, description, productOwner, createdBy, updatedBy, updatedDate):
        self.title = title
        self.description = description
        self.productOwner = productOwner
        self.createdBy = createdBy
        self.updatedBy = updatedBy,
        self.updatedDate = updatedDate


class Issue(Base):

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    productId = Column(Integer, ForeignKey('products.id'))
    createdDate = Column(DateTime, default=func.now(), nullable=False)
    updatedDate = Column(DateTime, default=func.now(), nullable=False)
    createdBy = Column(String(100))
    updatedBy = Column(String(100))
    assignedTo = Column(String(100))
    status = Column(String(10))

    def __init__(self, title, description, productId, createdBy, updatedBy, updatedDate, assignedTo, status):
        self.title = title
        self.description = description
        self.productId = productId
        self.createdBy = createdBy
        self.updatedBy = updatedBy,
        self.updatedDate = updatedDate
        self.assignedTo = assignedTo
        self.status = status


# Pydantic Model
class ProductSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    productOwner: str = Field(..., min_length=3, max_length=100)
    updatedBy: str = Field(..., min_length=3, max_length=100)
    updatedDate: datetime = Field(...)
    createdBy: str = Field(..., min_length=3, max_length=100)
    

class IssueSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    productId: int = Field(...)
    updatedBy: str = Field(..., min_length=3, max_length=100)
    updatedDate: datetime = Field(...)
    assignedTo: str = Field(..., min_length=3, max_length=100)
    status: str = Field(..., min_length=3, max_length=10)
    createdBy: str = Field(..., min_length=3, max_length=100)


class ProductResponse(ProductSchema):
    id: int
    createdDate: datetime

    class Config:
        orm_mode = True

class IssueResponse(IssueSchema):
    id: int
    createdDate: datetime

    class Config:
        orm_mode = True
