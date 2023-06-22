import json
from flask import request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv, find_dotenv
from os import environ as env
import os

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN", 'fsnd-sony-dev.us.auth0.com')
API_IDENTIFIER = env.get("API_IDENTIFIER",'library')
ALGORITHMS =  env.get('ALGORITHMS',['RS256'])
# AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'fsnd-sony-dev.us.auth0.com')
# API_IDENTIFIER = os.getenv("API_IDENTIFIER",'library')
# ALGORITHMS =  os.getenv('ALGORITHMS',['RS256'])
## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header


def get_token_auth_header() -> str:
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    if len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(403)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError as jwt_error:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Invalid header. "
                         "Use an RS256 signed JWT Access Token"}, 401) from jwt_error
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Invalid header. "
                             "Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer="https://" + AUTH0_DOMAIN + "/"
            )
            return payload

        except jwt.ExpiredSignatureError as expired_sign_error:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401) from expired_sign_error
        except jwt.JWTClaimsError as jwt_claims_error:
            raise AuthError({"code": "invalid_claims",
                             "description":
                             "incorrect claims,"
                             " please check the audience and issuer"}, 401) from jwt_claims_error
        except Exception as exc:
            raise AuthError({"code": "invalid_header",
                             "description":
                             "Unable to parse authentication"
                             " token."}, 401) from exc
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        wrapper.__name__= f.__name__
        return wrapper
    return requires_auth_decorator