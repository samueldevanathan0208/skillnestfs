import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url
from pathlib import Path

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Find .env file relative to this script (backend/.env)
    env_path = Path(__file__).resolve().parent / '.env'
    if env_path.exists():
        print(f"INFO: Loading environment variables from {env_path}")
        load_dotenv(dotenv_path=env_path)
    else:
        # Fallback to root .env
        root_env = Path(__file__).resolve().parent.parent / '.env'
        if root_env.exists():
            print(f"INFO: Loading environment variables from {root_env}")
            load_dotenv(dotenv_path=root_env)
except ImportError:
    print("Warning: python-dotenv not installed. Skipping .env loading.")

DB_URL = os.getenv("DATABASE_URL")

# Fallback for local development if .env is not loaded properly or is empty
if not DB_URL:
    # Use the current Supabase URL found in .env as the reliable fallback
    DB_URL = "postgresql://postgres:SkillNest%402025Db@db.nnzorlosowawefiddyfh.supabase.co:5432/postgres"
    print("Warning: DATABASE_URL not set in environment. Using default fallback.")

# Robust Parsing using SQLAlchemy's own tools
try:
    url_obj = make_url(DB_URL)
    print(f"INFO: Database connection details parsed successfully.")
    print(f"INFO: Target Host: {url_obj.host}")
    print(f"INFO: Target Port: {url_obj.port}")
    print(f"INFO: Target Database: {url_obj.database}")
except Exception as e:
    print(f"ERROR: Failed to parse DATABASE_URL: {e}")

# Create engine with connection pooling for production
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
