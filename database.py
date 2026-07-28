import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

DB_SSL = os.getenv('DB_SSL') == 'true'

connect_args = {}
if DB_SSL:
    # Equivalent to Knex's { rejectUnauthorized: false }:
    # require SSL but don't verify the server certificate
    connect_args['sslmode'] = 'require'
else:
    # Equivalent to Knex's ssl: false — no SSL negotiation at all
    connect_args['sslmode'] = 'disable'

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()