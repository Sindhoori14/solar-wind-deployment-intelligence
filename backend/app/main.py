from fastapi import FastAPI
from app.database import Base, engine

from app.models.user import User
from app.models.project import Project
from app.routers.auth import router as auth_router
from app.routers.project import router as project_router
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Solar & Wind Deployment Intelligence Platform")

app.include_router(auth_router)
app.include_router(project_router)


@app.get("/")
def home():
    return {"message": "Backend is working successfully!"}