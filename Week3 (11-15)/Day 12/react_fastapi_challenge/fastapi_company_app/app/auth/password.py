# CryptContext is used to manage password hashing algorithms
from passlib.context import CryptContext

# Create a password hashing context
# - bcrypt is the hashing algorithm
# - deprecated="auto" allows upgrading old hashes automatically
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    """
    Converts a plain text password into a secure hashed password.

    :param password: Plain text password entered by the user
    :return: Hashed password (safe to store in database)
    """

    # Hash the plain password using bcrypt
    return pwd_context.hash(password)


def verify_password(password, hashed):
    """
    Verifies whether a plain password matches the stored hashed password.

    :param password: Plain text password entered during login
    :param hashed: Hashed password stored in the database
    :return: True if password matches, False otherwise
    """

    # Compare plain password with hashed password
    return pwd_context.verify(password, hashed)