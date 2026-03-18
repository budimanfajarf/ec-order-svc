from src.schemas import CustomModel


class TransactionResponse(CustomModel):
    uuid: str
    amount: int
    created_at: str
    updated_at: str


class TransactionsResponse(CustomModel):
    data: list[TransactionResponse]
