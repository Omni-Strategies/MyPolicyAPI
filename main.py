import logging
import logging.config
from contextlib import asynccontextmanager
import yaml
from fastapi import FastAPI, Form, Request, UploadFile, File, Query
from routes import customer_routes, form_requests, requests_routes, login_routes, admin_routes, admin_login_routes

# 1. Initialize configuration inside the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    yield

app = FastAPI(lifespan=lifespan)

# 2. Instantiate your logger *after* the configuration is loaded
logger = logging.getLogger(__name__)

# 3. Include your routers cleanly
app.include_router(login_routes.router)
app.include_router(requests_routes.router)
app.include_router(customer_routes.router)
app.include_router(form_requests.router)
app.include_router(admin_routes.router)
app.include_router(admin_login_routes.router)