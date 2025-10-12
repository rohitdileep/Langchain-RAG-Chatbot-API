from schema.models import user
from schema.db_schema import db_base
from sqlalchemy.orm import Session

def create_user(db: Session , user_data : dict):
    db_user = user(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user


def get_user_by_session_id(db: Session , session_id : str):
    records = ( 
        db.query(user).filter(user.session_id == session_id).order_by(user.timestamp.desc()).all()
        )
    
    messages = []
    for record in records:
        messages.extend([
            {"role": "user", "content": record.user_query},
            {"role": "assistant", "content": record.ai_response}
        ])

    return messages

