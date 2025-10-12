from fastapi import FastAPI , HTTPException , Depends
from pydantic import BaseModel, Field
from typing import List , Optional
from schema.response import get_response
from schema.chroma_utils import get_vectorstore , delete_vectorstore 
from schema.service import get_user_by_session_id , create_user
from schema.db_utils import get_db 
from sqlalchemy.orm import Session
import os
from schema.models import user
from uuid import uuid4
import logging

logging.basicConfig(filename = 'app.log' , level = logging.INFO)
app = FastAPI()

## Pydantic models ##
class QueryRequest(BaseModel):
    session_id: Optional[str] = Field(..., description="Unique session identifier")
    query: str = Field(..., description="The user's query")



## creating Chroma vector store from the folder path ##
@app.post("/create_db")
def create_db(folder_path : str  , file_id : int  ):
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=400, detail="Folder path does not exist")
    try:
        sucess = get_vectorstore(folder_path , file_id)
        if sucess:
            logging.info(f"Vector store created successfully {file_id} from {folder_path}")
            return {"message": f"Vector store created successfully {file_id}"}
            
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating vector store: {e}")

## QA endpoint ##
@app.post("/query")
def ask_que(req: QueryRequest , db : Session = Depends(get_db)):
    session_id = req.session_id or str(uuid4()) 
    question = req.query


    chat_history = get_user_by_session_id(db = db , session_id = session_id )
    


    # Get response
    answer, updated_history = get_response(chat_history, question)
    if not answer:
        raise HTTPException(status_code=500, detail="Failed to get response")
    
    create_user(db = db , user_data = {
        "session_id" : session_id,
        "user_query" : question,
        "ai_response" : answer
    })

    logging.info(f"Session ID: {session_id}, Question: {question}, Answer: {answer}")
    return {"answer": answer, "chat_history": updated_history}

## Delete vector store ##
@app.delete("/delete_db")
def delete_db(file_id):
    success = delete_vectorstore(file_id)
    if success:
        return {"message": f"Vector store deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete vector store")

## Clear chat session ##   
@app.delete("/clear_session/{session_id}")
def clear_session(session_id : str , db : Session = Depends(get_db)):
    try:
        db.query(user).filter(user.session_id == session_id).delete()
        db.commit()
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {e}")