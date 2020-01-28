from datetime import datetime

import bcrypt
import jwt

from ..postgres import psql
from ..settings import JWT_SECRET, TOKEN_EXPIRY


# -----------------------------
# Authorization levels
# -----------------------------
AUTH_LEVEL_UNAUTHED = -10
AUTH_LEVEL_READ_ONLY = 0
AUTH_LEVEL_UNCONFIRMED = 10
AUTH_LEVEL_BASIC = 20
AUTH_LEVEL_PAID = 30
AUTH_LEVEL_TRAINER = 40
# -----------------------------


def issue_token(user_id, password):
    """ Returns tuple: (token, auth_level, error) """

    # TODO - report/handle:   jwt.exceptions.InvalidSignatureError

    # Get hash
    pg_result = psql("SELECT passwd FROM users WHERE id=%s", [user_id])

    #
    # Compare password
    passwd = pg_result.row["passwd"]
    result = bcrypt.checkpw(password.encode(), passwd.encode())

    # Invalid password
    if not result:
        return None, AUTH_LEVEL_READ_ONLY, "Invalid password/username combination"

    #
    # Create token
    try:
        # token = jwt.decode(token, secret)
        return auth_level(user_id)
    except Exception as e:
        return None, AUTH_LEVEL_READ_ONLY, repr(e)


def auth_level(user_id):
    """ Returns same tuple: (token, auth_level, error) """

    auth_level = AUTH_LEVEL_UNCONFIRMED

    #
    # Check if email activated
    pg_result = psql("SELECT email FROM users WHERE id=%s", [user_id])
    email = pg_result.row["email"]
    if not email:
        return jwt_token(user_id, auth_level), auth_level, None
    # pass: email active
    auth_level = AUTH_LEVEL_BASIC

    #
    # Check if paid member
    pass

    #
    # Check if paid trainer
    pass

    # Made it this far.. create token
    return jwt_token(user_id, auth_level), auth_level, None

    # return {'id': user_id, 'auth-level': auth_level}


def jwt_token(user_id, auth_level):
    """ Creates a JWT (token) for subsequent authorized requests """

    expires_at = datetime.now() + TOKEN_EXPIRY
    token = jwt.encode(
        {
            "id": user_id,
            "auth-level": AUTH_LEVEL_BASIC,
            "expires": int(expires_at.timestamp()),
        },
        JWT_SECRET,
        algorithm="HS256",
    ).decode()

    return token
