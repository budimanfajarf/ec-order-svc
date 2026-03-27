from typing import Any

from sqlalchemy import select

from src.database import fetch_all, transaction


async def get_transactions_by_user_id(user_id: str) -> list[dict[str, Any]]:
    select_query = select(transaction).where(transaction.c.user_id == user_id)

    return await fetch_all(select_query)
