import logging
import logging.config
from contextlib import asynccontextmanager
import yaml
from pathlib import Path
from fastapi import FastAPI
from routes import (
    customer_routes,
    form_requests,
    requests_routes,
    login_routes,
    admin_routes,
    admin_login_routes,
    quotes_routes,
    insurance_company_routes,
    company_admin_login_routes,
)
import os


# Configure log directory:
# Local default: ./logs
# Docker override: LOG_DIR=/app/logs
log_dir = Path(os.getenv("LOG_DIR", "logs"))
log_dir.mkdir(parents=True, exist_ok=True)


# Initialize configuration inside the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Override the log file path dynamically
    config["handlers"]["file"]["filename"] = str(log_dir / "app.log")

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info("Application startup completed")

    yield

    logger.info("Application shutdown completed")


app = FastAPI(lifespan=lifespan)


# Instantiate logger after configuration is loaded
logger = logging.getLogger(__name__)


# Include routers
app.include_router(login_routes.router)
app.include_router(requests_routes.router)
app.include_router(customer_routes.router)
app.include_router(form_requests.router)
app.include_router(admin_routes.router)
app.include_router(admin_login_routes.router)
app.include_router(quotes_routes.router)
app.include_router(insurance_company_routes.router)
app.include_router(company_admin_login_routes.router)