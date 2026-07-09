from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    solar_irradiance = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"))