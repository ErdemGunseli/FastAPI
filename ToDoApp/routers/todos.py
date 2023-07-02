from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends
from routers.auth import get_current_user
from pydantic import BaseModel, Field
from starlette import status as st
from models import ToDo
from dependencies import db_dependency

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# To Dos need to have a valid state before being saved, therefore using a request class to validate data:
class ToDoRequest(BaseModel):
    # ID won't be passed through the request since it is an autoincrement primary key:
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=0, max_length=300)
    priority: int = Field(gt=0, lt=6, default=1)
    complete: bool = Field(default=False)


@router.get("/", status_code=st.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    # The following line queries the database for all the rows (records) in the ToDos table.
    # db.query(DoDos) creates a query object specific to the ToDos table,
    # indicating that we want to retrieve data from this table.
    # the all method called on the query object executes the query and returns all the rows as the result,
    # returning them as a list of dictionaries, similar to the Books projects.
    return db.query(ToDo).filter(ToDo.owner_id == user.get("id")).all()


@router.get("/todo/{id}", status_code=st.HTTP_200_OK)
async def read_todo(db: db_dependency, user: user_dependency, id: int = Path(gt=0)):  # Autoincrement starts from 1
    # Need to have this everywhere where user is None:
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # This is essentially a WHERE clause, returning the first record that matches the id:
    # The brackets are NECESSARY, otherwise the & operator will be evaluated first, causing an error.
    result = db.query(ToDo).filter((ToDo.id == id) & (user.get("id") == ToDo.owner_id)).first()

    if result is not None: return result
    # If not returned at this point, raising an exception:
    raise HTTPException(status_code=404, detail="To Do Not Found")


@router.post("/todo", status_code=st.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: ToDoRequest):
    # Ensuring that the user is valid:
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # Python uses ** to unpack dictionaries, * to unpack lists, tuples:
    # The user data is in a dictionary, so get method is used:
    db.add(ToDo(**todo_request.dict(), owner_id=user.get("id")))
    db.commit()


@router.put("/todo/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, user: user_dependency, todo_request: ToDoRequest, id: int = Path(gt=0)):
    # Ensuring that the user is valid:
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # Passed by reference, so must use the record itself when changing attributes:
    todo = db.query(ToDo).filter((ToDo.id == id) & (ToDo.owner_id == user.get("id"))).first()
    if todo is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="To Do Not Found")

    # If the record is found, modifying it:
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    # This is not adding a new record, but updating the existing one
    # since we assigned the return value of the initial query to this variable:
    db.add(todo)
    db.commit()


@router.delete("/todo/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, id: int = Path(gt=0)):
    # Ensuring that the user is valid:
    if user is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    record = db.query(ToDo).filter((ToDo.id == id) & (ToDo.owner_id == user.get("id"))).first()
    if record is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="To Do Not Found")
    db.delete(record)
    db.commit()
