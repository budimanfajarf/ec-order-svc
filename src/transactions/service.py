from typing import Any

from sqlalchemy import insert, select

from src.database import fetch_one, fetch_all, execute, transaction

async def get_transactions_by_user_id(user_id: int) -> list[dict[str, Any]]:
    select_query = select(transaction).where(transaction.c.user_id == user_id)

    return await fetch_all(select_query)