from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Statistic(Base):
  """
  Определение модели статистики нагрузки
  """
  __tablename__ = 'statistic'

  id = Column(Integer, primary_key=True)
  CPU = Column(Integer)
  RAM = Column(String)
  ROM = Column(String)