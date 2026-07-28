from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import countries_repo
from schemas import countries_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/countries", tags=["countries"])

@router.post("/")
async def create_country(country: countries_schema.countryCreateInterface, db: Session = Depends(get_db)):
    logger.info(f"Creating country with data: {country.dict()}")
    return countries_repo.create_country(db, country)

@router.get("/{country_id}")
async def get_country(country_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info(f"Fetching country with ID: {country_id}")
    return countries_repo.get_country(db, country_id)

@router.put("/updates/{country_id}")
async def update_country(country_id: uuid.UUID, updates: countries_schema.countryUpdateInterface, db: Session = Depends(get_db)):
    logger.info(f"Updating country with ID: {country_id}")
    return countries_repo.update_country(db, country_id, updates)


@router.delete("/delete/{country_id}")
async def delete_country(country_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info(f"Deleting country with ID: {country_id}")
    return countries_repo.delete_country(db, country_id)

@router.get("/")
async def get_all_countries(db: Session = Depends(get_db)):
    logger.info("Fetching all countries")
    return countries_repo.get_all_countries(db)