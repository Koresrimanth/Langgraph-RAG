from sqlalchemy import text
from RAG.Backend.config import SessionLocal

# class MessageHistory:

def get_last_message(user_id,session_id,limit=5):
    db=SessionLocal()
    try:
        result=db.execute(
            text("""
                SELECT role, message
                FROM chat_messages
                WHERE user_id = :user_id AND session_id = :session_id
                ORDER BY created_at DESC
                LIMIT :limit
            """),
            {
            "user_id":user_id,
            "session_id":session_id,
            "limit":limit

            }
        )
        rows=result.fetchall()
        return [
            {"role":r[0],"content":r[1]} for r in reversed(rows)
        ]
    finally:
        db.close()



def save_message(user_id, session_id, role, message):
    db = SessionLocal()
    try:
        db.execute(
            text("""
                INSERT INTO chat_messages (user_id, session_id, role, message)
                VALUES (:user_id, :session_id, :role, :message)
            """),
            {
                "user_id": user_id,
                "session_id": session_id,
                "role": role,
                "message": message
            }
        )
        db.commit()
    finally:
        db.close()


