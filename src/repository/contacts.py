from typing import List
from datetime import date, timedelta

from sqlalchemy import select, or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactUpdate, ContactCreate

class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())
    
    async def get_contact_by_id(self, contact_id: int ) -> Contact | None:
        stmt = select(Contact).filter_by(id = contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()
        
    async def create_contact(self, body: ContactCreate) -> Contact:
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact
    
    async def update_contact(self,contact_id: int, body: ContactUpdate) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.dict().items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact
    
    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(self, query: str, skip: int, limit: int) -> List[Contact]:
        stmt = select(Contact).filter(or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())


    async def get_upcoming_birthdays(self) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=7)
        
        today_str = today.strftime('%m-%d')
        end_date_str = end_date.strftime('%m-%d')
        
        stmt = select(Contact)

        if today.year == end_date.year:
            stmt = stmt.filter(
                func.to_char(Contact.birthday, 'MM-DD').between(today_str, end_date_str)
            )
        else:
            stmt = stmt.filter(
                or_(
                    func.to_char(Contact.birthday, 'MM-DD') >= today_str,
                    func.to_char(Contact.birthday, 'MM-DD') <= end_date_str
                )
            )

        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())