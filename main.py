import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "EDU")

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)


app = FastAPI(title="Notification app")


class Notification(BaseModel):
    user_id: int = Field(..., ge=1)
    message: str = Field(..., min_length=1, max_length=500)
    send_at: datetime


@app.post("/notify/create")
def create_notification(payload: Notification):
    query = text(
        """
        INSERT INTO Notification(user_id, message, send_at)
        VALUES (:user_id, :message, :send_at)
    """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "user_id": payload.user_id,
                "message": payload.message,
                "send_at": payload.send_at,
            },
        )

    return {"status": "created"}


@app.get("/notify/get")
def get_notification():
    now = datetime.now()

    select_query = text(
        """
        SELECT * FROM Notification
        WHERE send_at <= :now
    """
    )

    delete_query = text(
        """
        DELETE FROM Notification
        WHERE send_at <= :now
    """
    )

    with engine.begin() as conn:
        result = conn.execute(select_query, {"now": now})
        rows = [dict(row._mapping) for row in result]

        conn.execute(delete_query, {"now": now})

    return rows
