from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Countries, FormRequests 
from schemas import countries_schema, requests_schema
import uuid
import logging
from security.password import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_country(
    session: Session,
    country: countries_schema.countryCreateInterface
) -> Countries:

    try:
        db_country = Countries(**country.dict())

        session.add(db_country)
        session.commit()
        session.refresh(db_country)

        logger.info(
            f"Country created with ID: {db_country.id}"
        )

        return db_country

    except Exception as e:
        logger.error(
            f"Error occurred while creating country: {e}"
        )
        session.rollback()
        raise

def get_country(session: Session, country_id: uuid.UUID) -> Optional[Countries]:
    try:
        country = session.query(Countries).filter(Countries.id == country_id).first()
        if country:
            logger.info(f"Country fetched with ID: {country_id}")
        else:
            logger.warning(f"No country found with ID: {country_id}")
        return country
    except Exception as e:
        logger.error(f"Error occurred while fetching country: {e}")
        session.rollback()
        raise


def update_country(session: Session, country_id: uuid.UUID, updates: countries_schema.countryUpdateInterface) -> Optional[Countries]:
    try:
        country = session.query(Countries).filter(Countries.id == country_id).first()
        if not country:
            logger.warning(f"No country found with ID: {country_id}")
            return None

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(country, key, value)

        session.commit()
        session.refresh(country)

        logger.info(f"Country updated with ID: {country_id}")
        return country

    except Exception as e:
        logger.error(f"Error occurred while updating country: {e}")
        session.rollback()
        raise


def delete_country(session: Session, country_id: uuid.UUID) -> bool:
    try:
        country = session.query(Countries).filter(Countries.id == country_id).first()
        if not country:
            logger.warning(f"No country found with ID: {country_id}")
            return False

        session.delete(country)
        session.commit()

        logger.info(f"Country deleted with ID: {country_id}")
        return True

    except Exception as e:
        logger.error(f"Error occurred while deleting country: {e}")
        session.rollback()
        raise

def get_all_countries(session: Session) -> List[Countries]:
    try:
        countries = session.query(Countries).all()
        logger.info(f"Fetched {len(countries)} countries")
        return countries
    except Exception as e:
        logger.error(f"Error occurred while fetching countries: {e}")
        session.rollback()
        raise