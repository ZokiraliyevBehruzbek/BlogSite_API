from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ⚙ bazangga mos connection URL yoz
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0000@localhost:5432/BlogDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# dependency (FastAPI uslubida, Flask'da shunchaki next(get_db()) bilan ishlatiladi)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
