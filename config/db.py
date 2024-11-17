#Configuración de la Base de Datos
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

#Se crea la instancia
engine = create_engine(DATABASE_URL)

#Se crea la sesión de forma local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Se obtiene la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()