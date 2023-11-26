from fastapi import FastAPI, Body

# The following line allows Uvicorn (the web server used to start a FastAPI application)
# to identify that we are creating a new application, and initialise the resources that were imported:
# Instantiating the class FastAPI and assigning it to the variable app:
app = FastAPI()

# Creating a list of books to be returned in this application:

# Constants to avoid string references:
TITLE = "title"
AUTHOR = "author"
CATEGORY = "category"

BOOKS = [
    {TITLE: "A", AUTHOR: "A", CATEGORY: "A"},
    {TITLE: "Harry Potter", AUTHOR: "J. K. Rowling", CATEGORY: "Fantasy"},
    {TITLE: "12 Rules for Life", AUTHOR: "Jordan B. Peterson", CATEGORY: "Self-help"},
    {TITLE: "The Selfish Gene", AUTHOR: "Richard Dawkins", CATEGORY: "Science"},
    {TITLE: "The Little Prince", AUTHOR: "Antoine de Saint-Exupéry", CATEGORY: "Children's"},
    {TITLE: "The Da Vinci Code", AUTHOR: "Dan Brown", CATEGORY: "Thriller"},
    {TITLE: "The Great Gatsby", AUTHOR: "F. Scott Fitzgerald", CATEGORY: "Fiction"},
    {TITLE: "The Fault in Our Stars", AUTHOR: "John Green", CATEGORY: "Fiction"},
    {TITLE: "The Hunger Games", AUTHOR: "Suzanne Collins", CATEGORY: "Young Adult"},
    {TITLE: "The Help", AUTHOR: "Kathryn Stockett", CATEGORY: "Historical Fiction"},
    {TITLE: "The Book Thief", AUTHOR: "Markus Zusak", CATEGORY: "Historical Fiction"},
    {TITLE: "The Hobbit", AUTHOR: "J. R. R. Tolkien", CATEGORY: "Fantasy"},
    {TITLE: "A Game of Thrones", AUTHOR: "George R. R. Martin", CATEGORY: "Fantasy"},
    {TITLE: "The Catcher in the Rye", AUTHOR: "J. D. Salinger", CATEGORY: "Fiction"},
    {TITLE: "The Chronicles of Narnia", AUTHOR: "C. S. Lewis", CATEGORY: "Fantasy"},
    {TITLE: "Lord of the Flies", AUTHOR: "William Golding", CATEGORY: "Fiction"},
    {TITLE: "Animal Farm", AUTHOR: "George Orwell", CATEGORY: "Fiction"},
    {TITLE: "The Kite Runner", AUTHOR: "Khaled Hosseini", CATEGORY: "Historical Fiction"},
    {TITLE: "Life of Pi", AUTHOR: "Yann Martel", CATEGORY: "Adventure"}
]

"""
Data Operations & HTTP Request Method Equivalents
C - CREATE --> POST 
R - READ --> GET
U - UPDATE --> PUT
D - DELETE --> DELETE
"""


# <!!!> GET HTTP REQUEST METHOD (READ) <!!!>

# Need FastAPI to recognise that this is an endpoint - the point where clients will interact with the application.
# An endpoint is like a function that returns something to a client using a URL.
# Async function means that it can run concurrently with other code,
# allowing the program to perform other tasks while waiting for operations to complete.
# The 'await' keyword is used to tell the program to wait for the operation to complete before continuing.

# The decorator argument refers to the URL path that will trigger the function.
# This function will be associated with the  URL http://127.0.0.1:8000/books.
@app.get("/books")
async def read_all_books():
    # The function returns the dictionary BOOKS.
    # This will be converted to JSON format and returned to the client.
    return BOOKS


# Notice that the decorator argument of the above function is a static path.
# Dynamic path parameters allow us to change the URL path of the endpoint depending on the value of an argument.

# If we have a function that leads to "books/{title}", then the title argument can be used to change the URL path.
# But underneath this function, we would not be able to have a function that leads to "books/mybook" since
# the above function would be called first. This is because FastAPI will always look for the first function
# that matches the URL path.
# To avoid this, we can ALWAYS have the static path above the dynamic path in the code.


# URLs cannot have spaces, and the %20 is a URL encoding for a space. For example, "books/The%20Hobbit".


# THe identifier of the dynamic parameter must match the parameter of the function:
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # Linear searching the dictionary of books:
    result = []
    for book in BOOKS:
        # The case fold method compares the strings without considering their case.
        # It is more aggressive than the lower method, because it removes distinctions in uppercase/lowercase
        # including special characters that are not in ASCII.
        if book.get(TITLE).casefold() == book_title.casefold():
            result.append(book)
    return result


@app.get("/books/{author}")
async def read_book_by_author(author: str):
    result = []
    for book in BOOKS:
        if book.get(AUTHOR).casefold() == author.casefold():
            result.append(book)
    return result


# The same endpoint can be written using query parameters by simply removing '{author}'

# Query parameters are key-value pairs appended to the end of a URL, after a "?" and separated by "&".
# They provide additional information to the server such as filters and sorting criteria.
# FastAPI knows that anything passed after "/books/" that is not a dynamic path parameter - it is a query parameter.
@app.get("/books/")
async def read_book_by_category(category: str):
    result = []
    for book in BOOKS:
        if book.get(CATEGORY).casefold() == category.casefold():
            result.append(book)
    return result


# Path parameters & query parameters can be used simultaneously:
@app.get("/books/{author}/")
# In the following example, 'category' is automatically detected as a query parameter
# since it is not explicitly used in the path:
async def read_book_by_author_and_category(author: str, category: str):
    result = []
    for book in BOOKS:
        if (book.get(AUTHOR).casefold() == author.casefold()) and \
                (book.get(CATEGORY).casefold() == category.casefold()):
            result.append(book)
    return result


# <!!!> POST HTTP REQUEST METHOD (Create) <!!!>

@app.post("/books/create_book")
# A Body refers to the data being sent in a request. Get requests do not have a body.
async def create_book(book=Body()):
    BOOKS.append(book)


# <!!!> PUT HTTP REQUEST METHOD (Update) <!!!>

# The body of a put request looks like a post request.
@app.put("/books/update_book")
async def update_book(book=Body()):
    for index, current_book in enumerate(BOOKS):
        if current_book.get(TITLE).casefold() == book.get(TITLE).casefold():
            BOOKS[index] = book


# <!!!> DELETE HTTP REQUEST METHOD <!!!>
@app.delete("/books/delete_book/{title}")
async def delete_book(title: str):
    for index, current_book in enumerate(BOOKS):
        if current_book.get(TITLE).casefold() == title.casefold():
            BOOKS.remove(current_book)


if __name__ == "__main__":
    # The following lines of code will only be executed if the file is run directly.
    # Uvicorn is a fast web server for running Python web applications.
    import uvicorn

    # Initiating the Uvicorn server to run the FastAPI application:
    # The first argument is the app which should be run:
    # Uvicorn server starts and listens for incoming requests on the host "0.0.0.0" and port 8000.
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Running the application using the following command in the terminal will reload the application
    # whenever changes are made to the code:
    # uvicorn books:app --reload

    # Use the following URL to access the application using Swagger UI:
    # http://127.0.0.1:8000/docs