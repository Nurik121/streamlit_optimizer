from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base


import db_con

Base = declarative_base()


# Классы для создания таблицы в БД
class Data_Optimization(Base):
    __tablename__ = 'Table_result'
    name = Column(String, primary_key=True)
    variables = Column(String)
    matrix = Column(String)
    obj = Column(String)
    options = Column(String)

class DataOptmizers(Base):
    __tablename__ = 'Optmizers'
    name = Column(String, primary_key=True)
    description = Column(String)



Base.metadata.create_all(db_con.engine)  # Создаем таблицу, если она не создана
