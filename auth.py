import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import requests
from jwt.algorithms import RSAAlgorithm
import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = ["RS256"]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if "Authorization" not in request.headers:
        abort(401)
    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")
    if len(header_parts) != 2:
        abort(401)
    if header_parts[0].lower() != "bearer":
        abort(401)
    return header_parts[1]


def check_permissions(permission, payload):
    if permission not in payload["permissions"]:
        abort(403)


def verify_decode_jwt(token):
    # 1. Fetch JWKS from Auth0
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    jwks = response.json()

    # 2. Decode the JWT header to find the correct key ID (kid)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    # 3. Find the public key with the matching "kid" in JWKS
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break
    # 4. Decode and verify the JWT
    if rsa_key:
        try:
            decoded_jwt = jwt.decode(
                token,
                RSAAlgorithm.from_jwk(rsa_key),
                algorithms=["RS256"],
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
    else:
        abort(401)
    return decoded_jwt


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
