from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine = create_engine("postgresql://shifatazeenshaikh:shifa123@localhost:5432/pizza", pool_pre_ping=True)

Base=declarative_base()

Session=sessionmaker()

