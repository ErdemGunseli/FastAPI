# SQLAlchemy allows us to interact with databases using an OOP approach,
# providing object-relational mapping (orm) that allows us to define Python classes
# (called models) that map to database tables.
from sqlalchemy import create_engine

# Session maker is a class that is used to create session objects for database interactions.
# These represent a connection to the database and provide a way to interact with the database.
from sqlalchemy.orm import sessionmaker

# The declarative_base function is used to create a base class for all data models.
# The data models will inherit from this class.
from sqlalchemy.ext.declarative import declarative_base

# This URL represents the location of the database in the FastAPI application.
# The database will be in this directory within the app.
# 'sqlite3' indicates that this is a SQLite database.
# The 3 slashes mean that it is a relative path to the todos.db from the current directory.
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todoapp.db"

# 'postgresql' indicates that this is a PostgreSQL database.
# 'erdem' is the superuser name that is set as the owner of the database.
# 'test12341' is the password for the database user.
# 'localhost' is the host of the database.
# '5432' is the port number on which PostgreSQL is listening.
# 'ToDoAppDatabase' is the name of the database.
SQLALCHEMY_DATABASE_URL = "postgresql://erdem:test12341@localhost:5432/ToDoAppDatabase"


# mysql + pymysql specifies the database dialect and driver (the program that connects the RDBMS to the app).
# 'root' is the superuser name and 'test1234!' is the password for the database user.
# 127.0.0.1:336 specifies the host IP address and port number of the database server.
# 'ToDoAppDatabase' is the name of the database.
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234!@127.0.0.1:3306/ToDoAppDatabase"


# Differences between SQLite and a production Relational DataBase Management System (RDBMS):
# SQLite is a local (serverless) database that is stored in a single file.
# It is used for development, testing and small applications.
# MYSQL and PostgreSQL focus on scalability, concurrency, and client-server architecture.
# Production DBMSs run on their own server and can be accessed by multiple clients at the same time.
# Hence, production databases need to be deployed separately to the application.

# PostgreSQL is an open-source production ORM RDBMS. It is very scalable and requires a server.

# A database engine is a way of connecting the database.
# The function creates an instance of the Engine class, which acts as an intermediary between the Python code
# and the database, handling tasks such as connection management, SQL execution and result fetching.
# The create_engine function is used to establish a connection to the database,
# taking in the URL of the database within the application as well as "connection arguments" kwargs
# which specify additional requirements that should be passed to the underlying database connection.

# SQLite by default only allows a single thread to connect to the database at a time,
# which is used to prevent concurrent access to the database file since SQLite is not thread-safe
# (using multiple threads can lead to problems).
# The dictionary keyword argument prevents this check from being made, since in FastAPI,
# there may be several threads that interact with the database at the same time.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# These kwargs are for SQLite only: connect_args={"check_same_thread": False})

# Creating a custom session class bound to the engine.
# auto commit = False means that the database will not automatically commit changes, manual commits are required.
# auto flush = False means that the session's changes to the database won't be synchronised automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Calling the declarative base function will return a new base class from which all data models inherit.
Base = declarative_base()


