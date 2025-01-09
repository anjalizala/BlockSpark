from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DatabaseURL = "mysql+pymysql://root:@localhost:3308/bookstore"

Base = declarative_base()
engine = create_engine(DatabaseURL)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

