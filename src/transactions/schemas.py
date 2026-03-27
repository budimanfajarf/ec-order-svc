from pydantic import Field

from src.schemas import CustomModel


class TransactionResponse(CustomModel):
    uuid: str
    amount: int
    created_at: str
    updated_at: str


class TransactionsResponse(CustomModel):
    data: list[TransactionResponse]


class TransactionItemRequest(CustomModel):
    product_uuid: str
    quantity: int = Field(gt=0)


class TransactionRequest(CustomModel):
    store_uuid: str
    items: list[TransactionItemRequest] = Field(min_length=1)
