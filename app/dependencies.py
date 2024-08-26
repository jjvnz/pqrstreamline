from app.database import engine, Base, SessionLocal, get_db

# Crea las tablas
Base.metadata.create_all(bind=engine)
