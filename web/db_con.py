import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Создание движка для подключения БД
engine = sqlalchemy.create_engine("sqlite:///web/database/DB.db", echo=True)
connection = engine.connect()
Session = sessionmaker(autoflush=False, bind=engine)  # Создаем сессию подключения к БД
session = Session()
