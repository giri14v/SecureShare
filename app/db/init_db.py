from app.db.database import engine, Base
from app.models import File


def init_db():
    Base.metadata.create_all(bind=engine)