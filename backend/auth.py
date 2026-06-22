import bcrypt
import hashlib
from models import db, User

# Username hashing
def hash_username(username):
    # Deterministically hash a normalized username using SHA-256.
    normalized = username.strip().lower()
    bytes_input = normalized.encode("utf-8")
    hash_bytes = hashlib.sha256(bytes_input).digest()
    hash_string = hash_bytes.hex()
    return hash_string

# Password hashing
def hash_password(password):
    # Hash a plaintext password using bcrypt and return a UTF-8 string.
    password_bytes = password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_string = hashed_bytes.decode("utf-8")
    return hashed_string

def verify_password(password, stored_hash):
    # Verify a plaintext password against a stored bcrypt hash string.
    password_bytes = password.encode("utf-8")
    stored_hash_bytes = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, stored_hash_bytes)

# Data access layer
def get_user_by_hashed_username(hashed_username):
    # Fetch a user by their hashed username.
    # Must be called inside an app context.
    return User.query.filter_by(username=hashed_username).first()

def create_user(hashed_username, hashed_password):
    # Create and persist a new user with hashed username and password.
    # Must be called inside an app context.
    new_user = User(username=hashed_username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# Authentication logic
AUTH_SUCCESS = "AUTH SUCCESS"
AUTH_FAIL_USER_NOT_FOUND = "AUTH FAIL USER NOT FOUND"
AUTH_FAIL_BAD_PASSWORD = "AUTH FAIL BAD PASSWORD"
REGISTER_SUCCESS = "REGISTER SUCCESS"
REGISTER_FAIL_USER_EXISTS = "REGISTER FAIL USER EXISTS"

def authenticate(username, password):
    # Authenticate a user given plaintext username and password.
    # Returns a tuple: (status_code, user_or_none)
    hashed_username = hash_username(username)
    user = get_user_by_hashed_username(hashed_username)
    if user is None:
        return AUTH_FAIL_USER_NOT_FOUND, None
    if not verify_password(password, user.password):
        return AUTH_FAIL_BAD_PASSWORD, None
    return AUTH_SUCCESS, user

def register(username, password):
    # Register a new user with hashed username and password.
    # Returns a tuple: (status_code, user_or_none)
    hashed_username = hash_username(username)
    existing = get_user_by_hashed_username(hashed_username)
    if existing is not None:
        return REGISTER_FAIL_USER_EXISTS, None
    hashed_password = hash_password(password)
    new_user = create_user(hashed_username, hashed_password)
    return REGISTER_SUCCESS, new_user
