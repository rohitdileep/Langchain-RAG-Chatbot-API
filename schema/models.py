from schema.db_utils import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP , text

class user(Base):
    __tablename__ = "users"
    id =  Column(Integer , primary_key = True , index = True , autoincrement = True)
    session_id = Column(String  , index = True)
    user_query =  Column(String , index = True)
    ai_response = Column(String , index = True)
    timestamp = Column(TIMESTAMP , server_default = text("CURRENT_TIMESTAMP") , nullable = False)

