from sqlalchemy.orm import Session
from datetime import datetime

from app.api.models import Issue, IssueSchema

def get_all_by_product(db_session: Session, productId: int):
    return db_session.query(Issue).filter(Issue.productId == productId).all()

def post(db_session: Session, payload: IssueSchema):
    issue = Issue(title=payload.title, description=payload.description, productId=payload.productId, createdBy=payload.createdBy, updatedBy=payload.updatedBy, updatedDate=payload.updatedDate, assignedTo=payload.assignedTo, status=payload.status)
    db_session.add(issue)
    db_session.commit()
    db_session.refresh(issue)
    return issue

def get_by_id(db_session: Session, productId: int, id: int):
    return db_session.query(Issue).filter(Issue.id == id, Issue.productId == productId).first()

def put(db_session: Session, issue: Issue, title: str, description: str, productId: int, createdBy: str, updatedBy: str, updatedDate: datetime, assignedTo: str, status: str):
    issue.title = title
    issue.description = description
    issue.productId = productId
    issue.createdBy = createdBy
    issue.updatedBy = updatedBy,
    issue.updatedDate = updatedDate
    issue.assignedTo = assignedTo
    issue.status = status
    db_session.commit()
    return issue

def delete(db_session: Session, productId: int, id: int):
    issue = db_session.query(Issue).filter(Issue.id == id, Issue.productId == productId).first()
    db_session.delete(issue)
    db_session.commit()
    return issue

