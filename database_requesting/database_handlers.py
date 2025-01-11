from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert, update, delete, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from .models import Statistic, Base

DATABASE_URL = "postgresql://postgres@localhost:5432/TestTask"
#DATABASE_URL = "mysql+mysqlconnector://user:password@host:port/database"  # MySQL
#DATABASE_URL = "sqlite:///my_database.db" # SQLite

engine = create_engine(DATABASE_URL)

metadata = MetaData()
Session = sessionmaker(bind=engine)

def create_tables_if_not_exist():
    """
    Создает таблицы, если они не существуют.
    """
    inspector = inspect(engine)
    if not inspector.has_table("statistic"):
        Base.metadata.create_all(engine)
        print("Table created")
    else:
        print("Table 'statistic' already exists")


def add_statistic(statistic_data:dict):
    """
    
    Добавить новой статистики в базу данных

    Args:
        statistic_data: Данные новой статистики
    
    """
    with Session() as session:
        try:
           new_statistic = Statistic(**statistic_data)
           session.add(new_statistic)
           session.commit()
           
           return new_statistic
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

            return None

if __name__ == '__main__':
    create_tables_if_not_exist()
    add_statistic({'CPU': '13.6%', 'RAM': '6.3ГБ / 15.8ГБ', 'ROM': '62.9ГБ / 365.8ГБ'})