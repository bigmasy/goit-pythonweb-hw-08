from sqlalchemy.ext.asyncio import AsyncSession


from src.repository.contacts import ContactRepository
from src.schemas import ContactUpdate, ContactCreate

class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)
    
    async def get_contacts(self, skip: int, limit: int):
        return await self.contact_repository.get_contacts(skip, limit)
    
    async def get_contact_by_id(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)
    
    async def create_contact(self, body: ContactCreate):
        return await self.contact_repository.create_contact(body)
    
    async def update_contact(self, contact_id: int, body: ContactUpdate):
        return await self.contact_repository.update_contact(contact_id=contact_id, body=body)

    async def remove_contact(self, contact_id: int):
        return await self.contact_repository.remove_contact(contact_id)

    async def search_contacts(self, query: str, skip: int, limit: int):
        return await self.contact_repository.search_contacts(query=query, skip=skip, limit=limit)
    
    async def get_upcoming_birthdays(self):
        return await self.contact_repository.get_upcoming_birthdays()