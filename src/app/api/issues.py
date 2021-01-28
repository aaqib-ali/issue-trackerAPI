from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.db_factory import SessionLocal, get_db
from fastapi import APIRouter, Depends, HTTPException, Path
from app.db import issue_crud, product_crud

from app.api.models import IssueResponse, IssueSchema

router = APIRouter()

@router.get("/{productId}/issues/", response_model=List[IssueResponse])
def get_all_by_product(*, db: Session = Depends(get_db), productId: int = Path(..., gt=0)):
   issues = issue_crud.get_all_by_product(db_session=db, productId=productId)
   return issues

@router.get("/{productId}/issues/{id}/")
def get(*, db: Session = Depends(get_db), productId: int = Path(..., gt=0), id: int = Path(..., gt=0)):
    issue = issue_crud.get_by_id(db_session=db, productId=productId, id=id)
    if not issue:
        raise HTTPException(status_code=404, detail="issue not found")
    return issue

@router.post("/{productId}/issues/", response_model=IssueResponse, status_code=201)
def create_issue(*, db: Session = Depends(get_db), productId: int = Path(..., gt=0), payload: IssueSchema):
    payload.productId = productId
    product = product_crud.get(db, productId)
    if not product:
        raise HTTPException(status_code=404, detail="product not found! Must create product first")

    issue = issue_crud.post(db_session=db, payload=payload)
    return issue

@router.put("/{productId}/issues/{id}/", response_model=IssueResponse)
def update_issue(
    *, db: Session = Depends(get_db), productId: int = Path(..., gt=0), id: int = Path(..., gt=0), payload: IssueSchema
):
    issue = issue_crud.get_by_id(db_session=db, productId=productId, id=id)
    if not issue:
        raise HTTPException(status_code=404, detail="issue not found")
    
    issue = issue_crud.put(
        db_session=db, issue=issue, title=payload.title, description=payload.description,
        productId=payload.productId, createdBy=payload.createdBy, updatedBy=payload.updatedBy, 
        updatedDate=payload.updatedDate, assignedTo=payload.assignedTo, status=payload.status
    )
    return issue

@router.delete("/{productId}/issues/{id}/", response_model=IssueResponse)
def delete_issue(
    *, db: Session = Depends(get_db), productId: int = Path(..., gt=0), id: int = Path(..., gt=0),
):
    issue = issue_crud.get_by_id(db_session=db, productId=productId, id=id)
    if not issue:
        raise HTTPException(status_code=404, detail="issue not found")
    issue = issue_crud.delete(db_session=db, productId=productId, id=id)
    return issue
