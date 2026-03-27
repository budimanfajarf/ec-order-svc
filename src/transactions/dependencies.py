from src.transactions.schemas import TransactionRequest


async def valid_transaction(request: TransactionRequest) -> TransactionRequest:
    # TODO: validate store_id and product_id
    if not request.items:
        raise ValueError("Transaction must have at least one item")

    return request
