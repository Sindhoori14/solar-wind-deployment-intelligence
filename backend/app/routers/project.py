from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate,ProjectUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Project Management"])


@router.post("/")
def create_project(
    project: ProjectCreate,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_project = Project(
        title=project.title,
        description=project.description,
        owner_id=user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "message": "Project created successfully",
        "project": new_project
    }
@router.get("/")
def view_projects(
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    projects = db.query(Project).filter(Project.owner_id == user.id).all()

    return projects
@router.put("/{project_id}")
def update_project(
    project_id: int,
    updated_project: ProjectUpdate,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == user.id
    ).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    project.title = updated_project.title
    project.description = updated_project.description

    db.commit()
    db.refresh(project)

    return {
        "message": "Project updated successfully",
        "project": project
    }

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == user.id
    ).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }