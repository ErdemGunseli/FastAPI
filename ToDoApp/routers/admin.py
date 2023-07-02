from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends
from routers.auth import get_current_user
from starlette import status as st
from models import ToDo
from dependencies import db_dependency

router = APIRouter(prefix="/admin", tags=["auth"])

# Copied user dependency from routers/todos.py
# Not the best solution, but need to avoid circular imports so cannot have this in dependencies.py
user_dependency = Annotated[dict, Depends(get_current_user)]


# Basically the same as in todos.py, but without ID filtering:
@router.get("/todo", status_code=st.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    # Returning all todos if the user is a valid admin:
    return db.query(ToDo).all()


@router.delete("/todo/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    # Deleting the to do if the user is a valid admin:
    todo = db.query(ToDo).filter(ToDo.id == id).first()
    if todo is None: raise HTTPException(status_code=404, detail="To Do Not Found")
    db.delete(todo)
    db.commit()
