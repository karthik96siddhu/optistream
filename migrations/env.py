import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Add your app directory to the system path so Python can find your models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Target metadata allows Alembic to see your models
from app.core.database import Base
from app.models.order import Order # Explicitly import your models here so Alembic registers them

config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Tell Alembic to grab your live database URL from environment variables
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@localhost:3306/optistream")
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata