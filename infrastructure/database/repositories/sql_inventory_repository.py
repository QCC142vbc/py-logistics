from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.inventory.models import Item, StockLevel, InventoryTransaction, TransactionType
from src.domain.inventory.repository import InventoryRepository, ItemFilter
from src.infrastructure.database.models import ItemModel, StockLevelModel


class SQLInventoryRepository(InventoryRepository):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    async def get_item(self, item_id: str) -> Optional[Item]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.id == item_id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None

    async def get_item_by_sku(self, sku: str) -> Optional[Item]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.sku == sku)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None

    async def save_item(self, item: Item) -> None:
        async with self._session_factory() as session:
            model = await session.get(ItemModel, item.id)
            if model:
                # Update existing
                model.sku = item.sku
                model.name = item.name
                model.quantity = item.quantity
                model.unit_cost = item.unit_cost
                model.location = item.location
                model.category = item.category
                model.reorder_point = item.reorder_point
                model.lead_time_days = item.lead_time_days
                model.description = item.description
                model.weight_kg = item.weight_kg
                model.volume_m3 = item.volume_m3
                model.supplier_id = item.supplier_id
                model.active = item.active
            else:
                # Create new
                model = ItemModel(
                    id=item.id,
                    sku=item.sku,
                    name=item.name,
                    quantity=item.quantity,
                    unit_cost=item.unit_cost,
                    location=item.location,
                    category=item.category,
                    reorder_point=item.reorder_point,
                    lead_time_days=item.lead_time_days,
                    description=item.description,
                    weight_kg=item.weight_kg,
                    volume_m3=item.volume_m3,
                    supplier_id=item.supplier_id,
                    active=item.active,
                )
                session.add(model)
            await session.commit()

    async def delete_item(self, item_id: str) -> None:
        async with self._session_factory() as session:
            model = await session.get(ItemModel, item_id)
            if model:
                await session.delete(model)
                await session.commit()

    async def get_stock_level(self, item_id: str) -> Optional[StockLevel]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(StockLevelModel).where(StockLevelModel.item_id == item_id)
            )
            model = result.scalar_one_or_none()
            if model:
                return StockLevel(
                    item_id=model.item_id,
                    available=model.available,
                    reserved=model.reserved,
                    in_transit=model.in_transit,
                    on_order=model.on_order,
                    last_updated=model.last_updated,
                )
            return None

    async def update_stock_level(
        self,
        item_id: str,
        available_delta: int = 0,
        reserved_delta: int = 0,
        in_transit_delta: int = 0,
        on_order_delta: int = 0,
    ) -> StockLevel:
        async with self._session_factory() as session:
            model = await session.get(StockLevelModel, item_id)
            if not model:
                model = StockLevelModel(
                    item_id=item_id,
                    available=available_delta,
                    reserved=reserved_delta,
                    in_transit=in_transit_delta,
                    on_order=on_order_delta,
                )
                session.add(model)
            else:
                model.available += available_delta
                model.reserved += reserved_delta
                model.in_transit += in_transit_delta
                model.on_order += on_order_delta
                model.last_updated = model.last_updated.__class__.utcnow()
            
            await session.commit()
            await session.refresh(model)
            
            return StockLevel(
                item_id=model.item_id,
                available=model.available,
                reserved=model.reserved,
                in_transit=model.in_transit,
                on_order=model.on_order,
                last_updated=model.last_updated,
            )

    async def list_items(self, filter: ItemFilter) -> List[Item]:
        async with self._session_factory() as session:
            query = select(ItemModel)
            
            if filter.sku:
                query = query.where(ItemModel.sku == filter.sku)
            if filter.category:
                query = query.where(ItemModel.category == filter.category)
            if filter.location:
                query = query.where(ItemModel.location == filter.location)
            if filter.active_only:
                query = query.where(ItemModel.active == True)
            if filter.supplier_id:
                query = query.where(ItemModel.supplier_id == filter.supplier_id)
            
            result = await session.execute(query)
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]

    async def record_transaction(self, transaction: InventoryTransaction) -> None:
        # In a real implementation, this would save to a transactions table
        pass

    async def get_transactions(
        self,
        item_id: Optional[str] = None,
        transaction_type: Optional[TransactionType] = None,
        from_date: Optional = None,
        to_date: Optional = None,
        limit: int = 100,
    ) -> List[InventoryTransaction]:
        # In a real implementation, this would query a transactions table
        return []

    async def get_low_stock_items(self, threshold: Optional[int] = None) -> List[Item]:
        async with self._session_factory() as session:
            from sqlalchemy import and_, or_

            if threshold is None:
                # Use item's reorder point
                query = select(ItemModel).where(
                    and_(
                        ItemModel.quantity <= ItemModel.reorder_point,
                        ItemModel.active == True,
                    )
                )
            else:
                # Use provided threshold
                query = select(ItemModel).where(
                    and_(
                        ItemModel.quantity <= threshold,
                        ItemModel.active == True,
                    )
                )
            
            result = await session.execute(query)
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]

    async def get_items_by_category(self, category: str) -> List[Item]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.category == category)
            )
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]

    async def get_items_by_location(self, location: str) -> List[Item]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.location == location)
            )
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]

    async def get_items_by_supplier(self, supplier_id: str) -> List[Item]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ItemModel).where(ItemModel.supplier_id == supplier_id)
            )
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]

    def _model_to_domain(self, model: ItemModel) -> Item:
        return Item(
            id=str(model.id),
            sku=model.sku,
            name=model.name,
            quantity=model.quantity,
            unit_cost=model.unit_cost,
            location=model.location,
            category=model.category,
            reorder_point=model.reorder_point,
            lead_time_days=model.lead_time_days,
            description=model.description,
            weight_kg=model.weight_kg,
            volume_m3=model.volume_m3,
            supplier_id=str(model.supplier_id) if model.supplier_id else None,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
