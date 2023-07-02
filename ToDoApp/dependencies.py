from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal


# The following is a generator function - a special function that uses the yield keyword instead of return.
# Typically, generators are used to create iterators which produce a series of values,
# used in scenarios where it is necessary to generate a sequence of values dynamically,
# rather than generating the entire sequence upfront. The next value can be obtained from
# the iterator by calling the next method on it.

# In this case, we are using it to create a context manager.
# A context manager is a way of managing resources that need to be cleaned up after use
# i.e. a closing the database connection after it is no longer needed.

# When generators are used to produce iterators, the fact that the code stops after the yield keyword
# is used to repeatedly return values each time the next method is called.
# In this case, it is being used to keep the database connection open
# until the read_all function completes after which the database can be closed.

def get_db():
    # Using the custom session class to connect to the database.
    # db represents a database connection.
    db = SessionLocal()
    try:
        # Returning the database connection that we just created.
        # Doing this using the "yield" keyword means that the database will not be closed too early.
        yield db
    finally:
        # The code following the yield statement will only be run once the read_all function finishes.
        db.close()


# "Depends" relates to dependency injection - the execution of the read_all function
# depends on the availability of a database connection.

# The argument of "Depends" specifies which function should be called for the dependency injection.
# When the read_all function is called and needs a value for the db parameter, FastAPI will
# invoke the get_db function to obtain the database session as the value for the dependency.

# The Annotated class is from the typing module and allows us to add additional metadata to type hints.
# In this case, we are indicating that the database Session object
# is a dependency that should be injected into the function.

# Session, imported from SQLAlchemy is the type of the dependency, i.e. the type of db.
db_dependency = Annotated[Session, Depends(get_db)]

