from fastapi import APIRouter, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status as st
from models import ToDo
from dependencies import db_dependency

router = APIRouter()


# To Dos need to have a valid state before being saved, therefore using a request class to validate data:
class ToDoRequest(BaseModel):
    # ID won't be passed through the request since it is an autoincrement primary key:
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=0, max_length=300)
    priority: int = Field(gt=0, lt=6, default=1)
    complete: bool = Field(default=False)


@router.get("/", status_code=st.HTTP_200_OK)
async def read_all(db: db_dependency):
    # The following line queries the database for all the rows (records) in the ToDos table.
    # db.query(DoDos) creates a query object specific to the ToDos table,
    # indicating that we want to retrieve data from this table.
    # the all method called on the query object executes the query and returns all the rows as the result,
    # returning them as a list of dictionaries, similar to the Books projects.
    return db.query(ToDo).all()


@router.get("/todo/{id}", status_code=st.HTTP_200_OK)
async def read_todo(db: db_dependency, id: int = Path(gt=0)):  # Autoincrement starts from 1
    # This is essentially a WHERE clause, returning the first record that matches the id:
    result = db.query(ToDo).filter(ToDo.id == id).first()

    if result is not None: return result
    # If not returned at this point, raising an exception:
    raise HTTPException(status_code=404, detail="To Do Not Found")


@router.post("/todo", status_code=st.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: ToDoRequest):
    # Python uses ** to unpack dictionaries, * to unpack lists, tuples:
    db.add(ToDo(**todo_request.dict()))
    db.commit()


@router.put("/todo/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: ToDoRequest, id: int = Path(gt=0)):
    # Passed by reference, so must use the record itself when changing attributes:
    record = db.query(ToDo).filter(ToDo.id == id).first()
    if record is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="To Do Not Found")

    # If the record is found, modifying it:
    record.title = todo_request.title
    record.description = todo_request.description
    record.priority = todo_request.priority
    record.complete = todo_request.complete

    # This is not adding a new record, but updating the existing one
    # since we assigned the return value of the initial query to this variable:
    db.add(record)
    db.commit()


@router.delete("/todo/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, id: int = Path(gt=0)):
    record = db.query(ToDo).filter(ToDo.id == id).first()
    if record is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="To Do Not Found")
    db.delete(record)
    db.commit()
