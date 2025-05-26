# src/data_layer/database.py

import os
import asyncpg
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path=".env.clinical")
DB_URL = os.getenv("DB_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=DB_URL, min_size=1, max_size=5)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def get_patient(self, patient_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM patients WHERE id = $1", patient_id)

    async def insert_prescription(self, patient_id, drug_name, dose):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO prescriptions (patient_id, drug_name, dose)
                VALUES ($1, $2, $3)
                """,
                patient_id, drug_name, dose
            )