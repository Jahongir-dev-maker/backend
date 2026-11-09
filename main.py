import os
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI()


class MijozIn(BaseModel):
    phone: str
    paroll: str


def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.get("/mijozlar")
def list_mijozlar():
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, phone, paroll FROM mijozlar ORDER BY id"
        ).fetchall()
@app.get("/mijozlar/search")
def find_mijozlar(phone: str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, phone, paroll FROM mijozlar WHERE lower(phone) = lower(%s)",
            (phone,),
        ).fetchall()

@app.post("/mijozlar", status_code=201)
def add_mijoz(s: MijozIn):
    with get_conn() as conn:
        return conn.execute(
            "INSERT INTO mijozlar (phone, paroll) VALUES (%s, %s) RETURNING id, phone, paroll",
            (s.phone, s.paroll),
        ).fetchone()