from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.site import Site
from app.models.project import Project
from app.models.user import User
from app.schemas.site import SiteCreate,SiteUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/sites", tags=["Site Management"])


@router.post("/")
def create_site(
    site: SiteCreate,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    project = db.query(Project).filter(
        Project.id == site.project_id,
        Project.owner_id == user.id
    ).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    new_site = Site(
        name=site.name,
        latitude=site.latitude,
        longitude=site.longitude,
        solar_irradiance=site.solar_irradiance,
        wind_speed=site.wind_speed,
        project_id=site.project_id
    )

    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    return {
        "message": "Site created successfully",
        "site": new_site
    }
@router.get("/")
def view_sites(
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sites = (
        db.query(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(Project.owner_id == user.id)
        .all()
    )

    return sites
@router.get("/search")
def search_sites(
    keyword: str = Query(...),
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sites = (
        db.query(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(
            Project.owner_id == user.id,
            Site.name.ilike(f"%{keyword}%")
        )
        .all()
    )

    return sites
@router.put("/{site_id}")
def update_site(
    site_id: int,
    updated_site: SiteUpdate,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    site = (
        db.query(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(
            Site.id == site_id,
            Project.owner_id == user.id
        )
        .first()
    )

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    site.name = updated_site.name
    site.latitude = updated_site.latitude
    site.longitude = updated_site.longitude
    site.solar_irradiance = updated_site.solar_irradiance
    site.wind_speed = updated_site.wind_speed

    db.commit()
    db.refresh(site)

    return {
        "message": "Site updated successfully",
        "site": site
    }
@router.delete("/{site_id}")
def delete_site(
    site_id: int,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    site = (
        db.query(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(
            Site.id == site_id,
            Project.owner_id == user.id
        )
        .first()
    )

    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    db.delete(site)
    db.commit()

    return {
        "message": "Site deleted successfully"
    }