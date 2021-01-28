from fastapi import FastAPI
from app.db.db_factory import engine
from app.api import status, products, issues
from app.api.models import Base

Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(status.router)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(issues.router, prefix="/products", tags=["issues"])



