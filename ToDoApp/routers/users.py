from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from routers.auth import get_current_user
from starlette import status as st
from models import User
from dependencies import db_dependency
from routers.auth import bcrypt_context

router = APIRouter(prefix="/user", tags=["user"])

# Copied user dependency from routers/todos.py
# Not the best solution, but need to avoid circular imports so cannot have this in dependencies.py
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=st.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    return db.query(User).filter(User.id == user.get("id")).first()


class UserVerification(BaseModel):
    password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)


@router.put("/change_password", status_code=st.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    user_result = db.query(User).filter(User.id == user.get("id")).first()
    if user_result is None:
        raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="User Not Found")
    if not bcrypt_context.verify(user_verification.password, user_result.hashed_password):
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

    user_result.hashed_password = bcrypt_context.hash(user_verification.new_password)

    # This is not adding a new record, but updating the existing one
    # since we assigned the return value of the initial query to this variable:
    db.add(user_result)
    db.commit()
