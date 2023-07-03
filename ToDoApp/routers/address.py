import sys
from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends
from pydantic import BaseModel
from routers.auth import get_current_user
from starlette import status as st
from models import ToDo, Address, User
from dependencies import db_dependency

sys.path.append("..")

# The responses kwarg defines the expected HTTP responses for the API endpoints in this router.
# It means that if any endpoint returns a 4004, the description will be "Not found".
router = APIRouter(prefix="/address", tags=["address"], responses={st.HTTP_404_NOT_FOUND: {"description": "Not found"}})

# Copied user dependency from routers/todos.py
# Not the best solution, but need to avoid circular imports so cannot have this in dependencies.py
user_dependency = Annotated[dict, Depends(get_current_user)]


class AddressRequest(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postal_code: str
    apt_num: str


@router.post("/", status_code=st.HTTP_201_CREATED)
async def create_address(address_request: AddressRequest, user: user_dependency, db: db_dependency):
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    address = Address()
    address.address1 = address_request.address1
    address.address2 = address_request.address2
    address.city = address_request.city
    address.state = address_request.state
    address.country = address_request.country
    address.postal_code = address_request.postal_code
    address.apt_num = address_request.apt_num

    db.add(address)
    # Flushing synchronises changes made in the current session with the database, but does not commit them.
    # It will allow the address to be assigned an ID, without yet committing the changes to the database.
    db.flush()

    # Obtaining the user from the database:
    user = db.query(User).filter(User.id == user.get("id")).first()
    # Setting the foreign key before committing:
    user.address_id = address.id
    db.add(user)

    # Finally committing everything:
    db.commit()
    return address_request
