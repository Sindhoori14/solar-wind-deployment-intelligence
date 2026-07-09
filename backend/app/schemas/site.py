from pydantic import BaseModel


class SiteCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    solar_irradiance: float
    wind_speed: float
    project_id: int


class SiteUpdate(BaseModel):
    name: str
    latitude: float
    longitude: float
    solar_irradiance: float
    wind_speed: float