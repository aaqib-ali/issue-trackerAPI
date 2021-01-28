from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from app.db.db_factory import SessionLocal, get_db
from app.db import product_crud
from app.api.models import ProductResponse, ProductSchema


router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(*, db: Session = Depends(get_db), payload: ProductSchema):
    product = product_crud.post(db_session=db, payload=payload)
    return product

@router.get("/{id}/", response_model=ProductResponse)
def read_product(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    product = product_crud.get(db_session=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@router.get("/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    return product_crud.get_all(db_session=db)


@router.put("/{id}/", response_model=ProductResponse)
def update_product(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0), payload: ProductSchema
):
    product = product_crud.get(db_session=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    product = product_crud.put(
        db_session=db, product=product, title=payload.title, description=payload.description,
        productOwner=payload.productOwner, createdBy=payload.createdBy, updatedBy=payload.updatedBy, 
        updatedDate=payload.updatedDate
    )
    return product


@router.delete("/{id}/", response_model=ProductResponse)
def delete_product(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    product = product_crud.get(db_session=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    product = product_crud.delete(db_session=db, id=id)
    return product
