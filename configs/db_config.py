import os

# Get values from environment if set, otherwise fallback to defaults
DB_USER = os.environ.get("DB_USER", "demo")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "demo")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5332")
DB_NAME = os.environ.get("DB_NAME", "userdb")


class Config:
    # Build the SQLAlchemy connection string dynamically
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Export for use in other modules
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
