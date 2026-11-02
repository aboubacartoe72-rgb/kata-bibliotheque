from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# On crée la base de données (le fichier sera créé tout seul)
DATABASE_URL = "sqlite:///./bibliotheque.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()