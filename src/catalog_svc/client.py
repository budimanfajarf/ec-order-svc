from dataclasses import dataclass

import grpc

from src.catalog_svc import catalog_svc_pb2, catalog_svc_pb2_grpc
from src.config import settings


@dataclass
class Store:
    uuid: str
    name: str


@dataclass
class Product:
    uuid: str
    name: str
    price: int  # IDR


class CatalogClient:
    def __init__(self) -> None:
        self._channel: grpc.aio.Channel | None = None
        self._stub: catalog_svc_pb2_grpc.CatalogServiceStub | None = None

    async def connect(self) -> None:
        self._channel = grpc.aio.insecure_channel(settings.CATALOG_SVC_URL)
        self._stub = catalog_svc_pb2_grpc.CatalogServiceStub(self._channel)

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()

    @property
    def stub(self) -> catalog_svc_pb2_grpc.CatalogServiceStub:
        if self._stub is None:
            raise RuntimeError("CatalogClient not connected. Call connect() first.")
        return self._stub

    async def get_store_by_uuid(self, store_uuid: str) -> Store | None:
        request = catalog_svc_pb2.GetStoreByUuidRequest(store_uuid=store_uuid)
        response = await self.stub.GetStoreByUuid(request)
        if not response.HasField("store"):
            return None
        return Store(
            uuid=response.store.uuid,
            name=response.store.name,
        )

    async def get_products_by_uuids(
        self, store_uuid: str, product_uuids: list[str]
    ) -> list[Product]:
        request = catalog_svc_pb2.GetProductsByUuidsRequest(
            store_uuid=store_uuid,
            product_uuids=product_uuids,
        )
        response = await self.stub.GetProductsByUuids(request)
        return [
            Product(
                uuid=p.uuid,
                name=p.name,
                price=p.price,
            )
            for p in response.products
        ]

    async def reserve_stocks(self, items: list[dict[str, int]]) -> tuple[bool, str]:
        """
        items: list of {"product_uuid": str, "quantity": int}
        returns: (success, message)
        """
        stock_items = [
            catalog_svc_pb2.StockItem(
                product_uuid=item["product_uuid"],
                quantity=item["quantity"],
            )
            for item in items
        ]
        request = catalog_svc_pb2.ReserveStocksRequest(items=stock_items)
        response = await self.stub.ReserveStocks(request)
        return response.success, response.message


catalog_client = CatalogClient()
