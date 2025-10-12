from pydantic import BaseModel , Field
from typing import  List


class db_base(BaseModel):
    id : int 
    session_id : str = Field(... , description = "unique_session_id")
    user_query : str = Field(... , description = "user_query")
    ai_response : str = Field(... , description = "AI generated response")
    timestamp : str = Field(... , description = "timestamp")
    class Config:
        from_attributes = True

