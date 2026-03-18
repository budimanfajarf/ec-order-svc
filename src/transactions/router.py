from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.transactions import service
from src.transactions.schemas import TransactionResponse, TransactionsResponse

router = APIRouter()

@router.get("", response_model=TransactionsResponse, include_in_schema=True)
async def get_transactions(
    user_id: int = 1, # TODO: get user_id from jwt
) -> TransactionsResponse:
    transactions = await service.get_transactions_by_user_id(user_id)

    return TransactionsResponse(
        data=[
            TransactionResponse(
                uuid=str(transaction["uuid"]),
                amount=transaction["amount"],
                created_at=transaction["created_at"].isoformat(),
                updated_at=transaction["updated_at"].isoformat(),
            )
            for transaction in transactions
        ]
    )