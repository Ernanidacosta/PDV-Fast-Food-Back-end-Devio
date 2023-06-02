from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.client_model import ClientsModel
from schemas.client_schema import ClientSchema

router = APIRouter()


# POST Client
@router.post(
    '/client',
    status_code=status.HTTP_201_CREATED,
    response_model=ClientSchema,
)
async def post_person(
    client: ClientSchema, db: AsyncSession = Depends(get_session)
):
    new_client = ClientsModel(
        name=client.name,
    )
    db.add(new_client)
    await db.commit()
    return new_client


# GET Clients List
@router.get('/clients', response_model=List[ClientSchema])
async def get_persons(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClientsModel)
        result = await session.execute(query)
        persons: List[ClientsModel] = result.scalars().all()

        return persons
