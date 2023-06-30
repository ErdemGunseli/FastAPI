# The data models correspond to database tables.
# The data models will inherit from the Base class, which was the return value of the declarative base function.
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # Unique = True means that no two users can have the same username:
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    # Hashed password will be stored in the database:
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class ToDo(Base):
    # When we create a model in SQLAlchemy, we are essentially defining a new table in the database.
    # The Todos class represents the table and instances of this class represent records in this table.
    __tablename__ = "todos"

    # Column indicates that this attribute refers to a column of the table.
    # Specifying this is necessary because there may be some unmapped attributes.
    # e.g. Computed properties - data that is derived from other fields but itself does not need to be stored in the db.
    # First argument specifies the data type. These are imported so that they match the data types of the db.

    # Integer, Float, Boolean, String(size), Text (no size limit), DateTime (both date & time), Date, Time,
    # LargeBinary (blob), Enum, Numeric(precision, scale - representing the bits before and after the decimal point)
    # Array(Type) specific to PostgreSQL

    # Primary keys are indexed, but setting this to true anyway.
    id = Column(Integer, primary_key=True, index=True)
    # Foreign key of owner ID being used to link the To Do to the user who created it:
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
