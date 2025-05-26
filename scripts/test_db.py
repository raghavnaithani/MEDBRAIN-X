import asyncio
import os
import asyncpg
import pytest
from dotenv import load_dotenv

load_dotenv(".env.clinical")

DB_URL = os.getenv("DB_URL")

@pytest.mark.asyncio
async def test_db_connection():
    conn = await asyncpg.connect(DB_URL)
    try:
        # Check if connection works by running a simple query
        result = await conn.fetch("SELECT 1")
        assert result[0]["?column?"] == 1 or result[0]["?column?"] == 1
    finally:
        await conn.close()

@pytest.mark.asyncio
async def test_tables_exist():
    conn = await asyncpg.connect(DB_URL)
    try:
        # Check for presence of required tables
        result = await conn.fetch(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
        )
        tables = {row["tablename"] for row in result}
        expected_tables = {"patients", "prescriptions", "interactions"}
        assert expected_tables.issubset(tables)
    finally:
        await conn.close()

@pytest.mark.asyncio
async def test_gin_index_exists():
    conn = await asyncpg.connect(DB_URL)
    try:
        # Check if GIN index exists on drug_interactions table
        result = await conn.fetch(
            """
            SELECT indexname FROM pg_indexes
            WHERE tablename='interactions' AND indexdef LIKE '%gin%';
            """
        )
        assert len(result) > 0
    finally:
        await conn.close()
