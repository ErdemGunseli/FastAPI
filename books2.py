from typing import Optional
# Path allows us to validate path parameters, and Query allows us to validate Query parameters.
# These are similar to FastAPI Field:
# HTTPException can be raised when an error or exceptional condition occurs
# to indicate that an error should be returned to the client.
# The HTTP status code (default 500) can be returned as well as an optional detail message.
from fastapi import FastAPI, Path, Query, HTTPException
# Pydantic is a data validation library:
from pydantic import BaseModel, Field
# FastAPI is based on Starlette. Status is a module that contains
# a set of pre-defined constants that represent HTTP status codes.
# Just using an integer would lead to the same effect, but starlette constants are more readable:
from starlette import status as st

# Note: OPT+SHIFT+CMD+O to enable/disable GitHub Copilot
# OPT+[] to toggle between copilot suggestions

app = FastAPI()

# Status Codes:
# 1xx: Information responses that a request was received and understood.
# 2xx: Successful responses that the request was successfully received, understood, and accepted.
#    200: Successful Request (Typically used for GET requests)
#    201: Successfully Created (Typically used for POST requests)
#    204: Successful Request But Did Not Create Entity / Return Anything (Typically used for PUT requests)
# 3xx: Redirection responses that further action needs to be taken in order to complete the request.
# 4xx: Client error responses that the client request contains incorrect syntax or cannot be fulfilled.
#    400: Bad Client Request
#    401: Unauthorized Client Request
#    404: Client Requested Resource That Does Not Exist
#    422: Client Request Contains Incorrect Data Type
# 5xx: Server error responses that the server failed to fulfill an apparently valid request.
#    500: Internal Server Error (Typically used for unhandled exceptions on the server side)


class Book:
    # Optional indicates that ID can be an integer, or it can be None
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_year: int

    def __init__(self, id, title, author, description, rating, publish_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_year = publish_year


# Books need to have a valid state (i.e. a positive integer ID, rating between 1-5, etc.)
# Therefore, using a BookRequest class to validate the data before converting it to a Book instance:

# BaseModel is a core class in Pydantic, used to create data classes,
# allowing the expected data types of attributes to be defined:
class BookRequest(BaseModel):
    # Field is used to provide extra information about a model field,
    # such as a description (to be used with documentation) or add constraints.
    # If the data does not meet the constraints, a validation error is raised.
    # gt = Greater Than; lt = Less Than (exclusive)

    # The title attribute specifies the title of the field in the JSON schema:
    id: Optional[int] = Field(gt=-1, title="ID not required")
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=300)
    rating: int = Field(gt=-1, lt=6)
    publish_year: int = Field(gt=0)

    # Having a subclass Config inside a class that inherits from Pydantic BaseModel allows us to modify
    # the behaviour of the model and its JSON schema.
    class Config:
        title = "Custom Config"
        # Setting up a new schema and removing the ID attribute,
        # such that every time the schema in the docs is copied to add a new book,
        # it will not expect an ID in the example value:
        schema_extra = {
            "example": {
                "title": "New Book",
                "author": "New Author",
                "description": "New Description",
                "rating": 5,
                "publish_year": 2000
            }
        }


BOOKS = [
    Book(0, "The Great Gatsby", "F. Scott Fitzgerald",
         "A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.", 5, 1925),
    Book(1, "Title 1", "Author 1", "Description 1", 1, 2000),
    Book(2, "Title 2", "Author 2", "Description 2", 2, 2000),
    Book(3, "Title 3", "Author 3", "Description 3", 3, 2003),
    Book(4, "Title 4", "Author 4", "Description 4", 4, 2004),
    Book(5, "Title 5", "Author 5", "Description 5", 5, 2004)
]


# !!!!! PUT SPECIFIC ROUTES BEFORE GENERAL ONES !!!!!

@app.get("/books", status_code=st.HTTP_200_OK)
async def read_all_books():
    # Note that objects are automatically converted to JSON responses by FastAPI, so they will resemble dictionaries:
    return BOOKS


@app.get("/books/{id}", status_code=st.HTTP_200_OK)
async def read_book(id: int = Path(gt=-1)):
    for book in BOOKS:
        if book.id == id:
            return book
    # If the book is not found, raising exception
    raise HTTPException(status_code=404, detail="Book of this ID does not exist.")


# Need the URL to end with "/" if using query parameters:
@app.get("/books/", status_code=st.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(gt=-1, lt=6)):
    result = []
    for book in BOOKS:
        if book.rating >= rating:
            result.append(book)
    return result


@app.get("/books/publish/", status_code=st.HTTP_200_OK)
async def read_books_by_publish_year(publish_year: int = Query(gt=-1)):
    result = []
    for book in BOOKS:
        if book.publish_year == publish_year:
            result.append(book)
    return result


@app.post("/create_book", status_code=st.HTTP_201_CREATED)
# Using Body does not add validation to the application.
# Therefore, a BookRequest class is used to validate the data before converting it to a Book instance.
# This only works due to the BaseModel inheritance:
async def create_book(book_request: BookRequest):
    # If we appended the book_request to the list, we would have instance of both Book and BookRequest in the list.
    # We only want to have instances of a single class in the list.

    # The following line of code first converts the book_request into a dictionary
    # which has the structure attribute identifier : attribute value, for all the attributes of the object.
    # This does not include any of the methods of the object.
    # "**" unpacks the dictionary into keyword arguments when calling the constructor of Book.
    # Each key-value pair becomes a separate keyword argument in the constructor call:
    new_book = Book(**book_request.dict())
    BOOKS.append(set_next_id(new_book))


# Just a normal Python function to make the ID autoincrement:
def set_next_id(book: Book):
    # If this is not the first book, accessing the ID of the last book and adding 1 to that.
    # Otherwise, the ID of the book is 0.
    # if len(BOOKS) > 0: book.id = BOOKS[-1].id + 1
    # else: book.id = 0

    # Using a ternary operator to simplify the logic syntax:
    book.id = 0 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=st.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    found = False
    for index, current_book in enumerate(BOOKS):
        if current_book.id == book.id:
            BOOKS[index] = Book(**book.dict())
            found = True
    # If the book is not found, raising exception
    if not found:
        raise HTTPException(status_code=404, detail="Book of this ID does not exist.")


@app.delete("/books/{id}", status_code=st.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt=-1)):
    found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            found = True
            # Need to break now since after removing an item,
            # the list becomes shorter, so index will be out of bounds:
            break
    # If the book is not found, raising exception
    if not found:
        raise HTTPException(status_code=404, detail="Book of this ID does not exist.")
