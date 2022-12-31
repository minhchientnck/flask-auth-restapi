from functools import wraps
from flask import request
import jwt
import json
from datetime import datetime, timezone, timedelta
from flask_app import app, config


def validate_access_token(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        access_token = None
        if 'Authorization' in request.headers:
            access_token = request.headers['Authorization']

        if not access_token:
            return {
                'message': 'Authentication Token is missing!',
                'error': 'Unauthorized'
            }, 401
        try:
            secret_key = app.config['SECRET_KEY']
            decoded_data = jwt.decode(
                access_token, secret_key, algorithms=['HS256'])
        except Exception as e:
            return {
                'err': str(e)
            }, 500
        return fn(decoded_data, *args, **kwargs)
    return decorator


def validate_refresh_token(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            secret_key = app.config['SECRET_KEY']
            refresh_token = json.loads(request.data).get('refresh_token')
            decoded_data = jwt.decode(
                refresh_token, secret_key, algorithms=['HS256'])
        except Exception as e:
            return {
                'err': str(e)
            }, 500
        return fn(decoded_data, *args, **kwargs)
    return decorator


def check_refresh_token(refresh_token):
    try:
        secret_key = app.config['SECRET_KEY']
        jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
        return True
    except Exception as e:
        print(str(e))
        return False


def genrate_refresh_token(username, alg='HS256'):
    payload = {
        'username': username,
        'sub': 'refresh_token',
        'iat': datetime.now(tz=timezone.utc),
        'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=int(config.get('REFRESH_TOKEN_EXPIRED')))
    }
    secret_key = app.config['SECRET_KEY']
    return jwt.encode(payload, secret_key, alg)


def generate_access_token(user_info, alg='HS256'):
    payload = {
        'user': user_info,
        'sub': user_info.get('username'),
        'iat': datetime.now(tz=timezone.utc),
        'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=int(config.get('ACCESS_TOKEN_EXPIRED')))
    }
    secret_key = app.config['SECRET_KEY']
    return jwt.encode(payload, secret_key, alg)
