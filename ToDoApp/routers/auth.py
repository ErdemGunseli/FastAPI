from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status as st
from passlib.context import CryptContext
from dependencies import db_dependency
from models import User
from typing import Annotated, Optional
from jose import jwt, JWTError
# The following will allow us to handle authentication requests,
# where the user will enter their username and password directly into the request:
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Router is a way of combining FastAPI applications - we can have a main application,
# and several sub-applications that are combined.
# The prefix kwarg means that all routes defined in this router will have "/auth" prefix appended to their path.
# For "create_user" becomes "/auth/create_user":
# The tags kwarg is used to group the routes in the documentation.
# SwaggerUI will group endpoints within a router using the tag name.
router = APIRouter(prefix="/auth", tags=["auth"])

# A JWT needs an algorithm and secret key:
# Secret key should be a random string. This was generated using opensl rand -hex 32:
SECRET_KEY = "4a1221568c7bee38337d142b1d3033e8ca513f1a74411c65cc787889037ac2cd"
ALGORITHM = "HS256"
# The time to live for the JWT:
TOKEN_TTL = timedelta(minutes=30)

# Indicating that we want to use the bcrypt hashing algorithm.
# Setting deprecated to "auto" means that any password hashes that are not using bcrypt will be automatically updated:
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
# The argument contains the URL that the client will send to the application:
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
token_dependency = Annotated[str, Depends(oauth2_bearer)]


class CreateUserRequest(BaseModel):
    # ID will be auto incremented by the database, so it won't be passed through the request:
    username: str
    email: str
    first_name: str
    last_name: str
    # The request password will not be hashed yet:
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


# No need for dependency injection of the database, since it will be called from within the create_user function:
def authenticate_user(username: str, password: str, db):
    # Obtaining the first (and only) user with the entered username from the database:
    user = db.query(User).filter(User.username == username).first()

    # If the user is found, we use the verify method of the bcrypt context to check if the password matches:
    if (user is not None) and bcrypt_context.verify(password, user.hashed_password): return user


# This function generates a Json Web Token used for secure information exchange between the client and server.
# We want to include the username and user ID within the token.

def create_access_token(id: int, username: str, role: str, expires_delta: timedelta):
    # The time at which the token expires is the current time plus time to live:
    expires = datetime.utcnow() + expires_delta

    # The payload is the data that we want to encode within the token.
    # This is so that the server can understand which user is making the requests.
    # "sub" stands for subject, and is the user that the token is for.
    payload = {"sub": username, "id": id, "exp": expires, "role": role}

    # Creating the JWT, using the secret key and algorithm to encode the payload:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: token_dependency):
    # Wrapping in try-catch block, in case the token is invalid:
    try:
        # Attempting to decode the token using the secret key and algorithm.
        # If successful, this will return a dictionary that contains the encoded user data.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extracting the username and user ID from the payload dictionary:
        username: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("id")
        role: Optional[str] = payload.get("role")

    # If the decoding fails for any reason, it would raise this error, so catching it:
    except JWTError:
        username = None
        user_id = None
        role = None

    if None in (username, user_id, role):
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    return {"username": username, "id": user_id, "role": role}


@router.post("/create_user", status_code=st.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    # The following commented line would not work, because the user has hashed_password,
    # but the create user request has password, so dictionaries are not the same:
    # user = User(**create_user_request.dict())
    user = User(username=create_user_request.username,
                email=create_user_request.email,
                first_name=create_user_request.first_name,
                last_name=create_user_request.last_name,
                # Hashing the user request password:
                hashed_password=bcrypt_context.hash(create_user_request.password),
                is_active=True,
                role=create_user_request.role,
                phone_number=create_user_request.phone_number
                )

    # Saving the user to the database:
    db.add(user)
    db.commit()


# A JWT is a self-contained way to securely transmit information between parties as a JSON object.

# The security of JWT comes from the fact that it is signed. Someone could easily decrypt the token
# and read the payload, but they can't just alter the data and re-sign the token without knowing the secret key.

# Once the user logs in, we will create a JWT that contains the user's username and role.
# The client will then send this token with every request to the API, and the server will verify the token.

# JSON Web Tokens consist of three parts, separated by a dot:
# 1. Header - contains the algorithm used to sign the token and the type of token.
#             It is then base64 encoded to create the first part of the JWT token.

# 2. Payload - contains the data that is being transmitted.
#              The data contains claims, which can be of 3 types:
#              1) Registered: Pre-defined claims that are not mandatory, but recommended.
#              2) Public: Custom claims that can be defined by those using JWTs.
#              3) Private: Custom claims that are only defined by those using them.
# The payload is then base64 encoded to create the second part of the JWT token.

# 3. Signature - used to verify that the token has not been changed.

# Response model specifies that the returned data should be in the form of the Token model:
@router.post("/token", status_code=st.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: auth_dependency, db: db_dependency):
    # OAuth2PasswordRequestForm has the username and password attributes, and form_data is an instance of this class.
    user = authenticate_user(form_data.username, form_data.password, db)

    if user is not None:
        token = create_access_token(user.id, user.username, user.role, TOKEN_TTL)
        # This convention for the return value is used due to the OAUTH2.0 Bearer Token Specification.
        # Bearer indicates a request should be authenticated by the provided access token
        # i.e. it is a hint about how to use the token.
        return {"access_token": token, "token_type": "bearer"}
    # if user is None:
    raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

