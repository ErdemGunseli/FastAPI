from fastapi import FastAPI
from routers import auth, todos
from database import engine
import models

app = FastAPI()

# Creating all the tables represented by the models using the engine.
# The database URL was used when creating the engine.
# This will only be run if the database doesn't already exist.
models.Base.metadata.create_all(bind=engine)

# Stating that the auth.py file is a sub-application of the main application:
app.include_router(auth.router)
app.include_router(todos.router)


# Instead of creating our API endpoints in main.py, we can create them in separate sub-applications,
# categorised by their purpose.
