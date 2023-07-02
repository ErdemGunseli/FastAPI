from fastapi import FastAPI
from routers import auth, todos, admin, users
from database import engine
import models

app = FastAPI()

# Creating all the tables represented by the models using the engine.
# The database URL was used when creating the engine.
# This will only be run if the database doesn't already exist.
models.Base.metadata.create_all(bind=engine)

# Stating that the auth.py file is a sub-application of the main application:
# Need to do this for each router that we want to use in the application:
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# Instead of creating our API endpoints in main.py, we can create them in separate sub-applications,
# categorised by their purpose.




# Alembic is a lightweight database migration tool for SQLAlchemy.
# It helps manage real-time migrations - changes to the db schema (structures and connections within tables).
# It allows version control of the db schema. Works with different database backends.
# It provides scripts to generate migrations, and apply them to the db.
# Whilst it is risky to change the db schema in production, Alembic allows us to roll back changes if necessary.
# alembic init <folder_name> - creates a new environment with the necessary files to use Alembic.
# alembic revision -m <message> - creates a new migration script.
# alembic upgrade <revision#> - applies the migration to the db.
# alembic downgrade <revision#> - rolls back the migration.
# To initialise the Alembic environment, we need to run the following command:
# alembic init alembic (the second 'alembic' is the folder name and can be changed).


