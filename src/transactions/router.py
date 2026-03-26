from fastapi import APIRouter, Depends

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.transactions import service
from src.transactions.schemas import TransactionResponse, TransactionsResponse

router = APIRouter()


@router.get("", response_model=TransactionsResponse, include_in_schema=True)
async def get_transactions(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> TransactionsResponse:
    transactions = await service.get_transactions_by_user_id(jwt_data.user_id)

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
