import re

import bcrypt
import stripe

from .libserver import Response
from .postgres import psql
from .settings import STRIPE_API_KEY

# Set Stripe API key
stripe.api_key = STRIPE_API_KEY


def POST_register(request):

    # Parse incoming request
    body = request.json
    username = body["username"]
    email = body["email"]
    password = body["password"]
    password_confirm = body["password-confirm"]

    """
    -------------------------------------
    Registration validation checks
    -------------------------------------

    Python regex:
        https://www.tutorialspoint.com/How-to-match-any-one-uppercase-character-in-python-using-Regular-Expression
        https://www.tutorialspoint.com/How-to-check-if-a-string-contains-only-upper-case-letters-in-Python
    """

    #
    # Username
    if (
        len(username) < 6
        or len(username) > 218
        or not re.match("^[0-9a-z_]+$", username)
    ):
        return Response(
            data={
                "error": "Username must be between 6 an 18 characters and contain only lowercase letters, numbers, and underscores"
            },
            code=400,
        )
    #
    # Password
    elif password_confirm != password:
        return Response(data={"error": "Passwords do NOT match"}, code=400)
    elif (
        len(password) < 6
        or len(password) > 18
        or not re.findall(r"""[~`!#$%\^&*+=\-\[\]\\',/{}|\\":<>\?]""", password)
        or not re.findall("[a-z]", password)
        or not re.findall("[A-Z]", password)
    ):
        return Response(
            data={
                "error": "Password must be 6-18 chars long, and contain both uppercase, lowercase, and a special character",
            },
            code=400,
        )

    #
    # Email
    elif not re.match(
        r"""^(([^<>()\[\]\\.,:\s@"]+(\.[^<>()\[\]\\.,:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$""",
        email,
    ):
        return Response(data={"error": "Email invalid"}, code=400)

    """
    -------------------------------------
    Attempt to SQL insert user
    -------------------------------------
    """

    # TODO: transactional `block()`
    try:
        stripe_id = stripe.Customer.create(email=email).id
        passwd = bcrypt.hashpw(password, bcrypt.gensalt(12))
        result = psql(
            "INSERT INTO users (username, passwd, unverified_email, stripe_id) VALUES (%s, %s, %s, %s )",
            [username, passwd, email, stripe_id],
        )
        print(result)
        
    except Exception as e:
        return Response(data={"error": f"Register Failed\n{e.__repr__}"}, code=400)


def POST_login(request):
    pass
