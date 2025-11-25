from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db

from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.services.contacts import ContactService, DuplicateContactError

router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    query: str = Query(min_length=3, description="Search string by first name, last name, or email."),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
Search contacts by name, surname, or email.
    """
    contact_service = ContactService(db)
    return await contact_service.search_contacts(query= query, skip= skip, limit= limit)

@router.get('/birthdays', response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.get_upcoming_birthdays()

@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip=skip, limit=limit)
    return contacts

@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact_by_id(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact_by_id(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    try:
        return await contact_service.create_contact(body)
    except DuplicateContactError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    try:
        contact = await contact_service.update_contact(body=body, contact_id=contact_id)
    except DuplicateContactError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    result = await contact_service.remove_contact(contact_id)
    if result is None:
        raise HTTPException(404)
    return result

