from flask_app.utililty import generate_username_suffix
from flask_app.models import Employees, Users
from flask_app import app, bcrypt, db
import json
from datetime import datetime
from flask import request
from flask_app.auth_service import generate_access_token, \
    genrate_refresh_token, validate_access_token, \
    validate_refresh_token, check_refresh_token


@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = json.loads(request.data)
    existed_employee = Employees.query.filter_by(
        first_name=data.get('first_name'),
        middle_name=data.get('middle_name'),
        last_name=data.get('last_name')
    ).first()

    if existed_employee and not data.get('is_override'):
        return {
            'message': 'Employee is existed'
        }, 500

    if existed_employee and data.get('is_override'):
        username = f"{str(data.get('first_name')+'.'+data.get('last_name')).lower()}.{generate_username_suffix()}"

    username = f"{str(data.get('first_name')+'.'+data.get('last_name')).lower()}.{generate_username_suffix()}"
    user = Users(
        username=username,
        password=bcrypt.generate_password_hash(data.get('password'), 10),
        refresh_token=genrate_refresh_token(username),
        created_date=datetime.now(),
        updated_date=datetime.now(),
    )
    if not data.get('profile_picture_url'):
        profile_picture_url = None
    else:
        profile_picture_url = data.get('profile_picture_url')
    employee = Employees(
        first_name=data.get('first_name'),
        middle_name=data.get('middle_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        permanent_address=data.get('permanent_address'),
        secondary_address=data.get('secondary_address'),
        email=data.get('email'),
        job_title=data.get('job_title'),
        profile_picture_url=profile_picture_url,
        role=data.get('role'),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
    )
    try:
        employee.user.append(user)
        db.session.add(employee)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return {
            'err': str(e)
        }, 500
    return {
        'message': 'Created',
        'employee': employee.to_dict()
    }, 200


@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = json.loads(request.data)
    if not data.get('username'):
        return {'message': 'Username is required'}, 500
    if not data.get('password'):
        return {'message': 'Password is required'}, 500
    user = Users.query.filter_by(username=data.get('username')).first()
    if not user:
        return {'message': 'User is not existed'}, 500
    if not bcrypt.check_password_hash(user.password, data.get('password')):
        return {'message': 'Wrong password'}, 500
    user_info = {
        'id': user.id,
        'username': user.username
    }
    access_token = generate_access_token(user_info)
    refresh_token = user.refresh_token
    print(check_refresh_token(user.refresh_token))
    if not check_refresh_token(user.refresh_token):
        refresh_token = genrate_refresh_token(username=user.username)
        user.refresh_token = refresh_token
        db.session.commit()

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }, 200


@app.route('/refresh-token', methods=['POST'])
@validate_refresh_token
def refresh_token(decoded_data):
    user = Users.query.filter_by(username=decoded_data.get('username')).first()
    if (not user):
        return {
            'message': 'Invalid refresh token',
        }, 500
    user_info = {
        'id': user.id,
        'username': user.username
    }
    access_token = generate_access_token(user_info)
    return {
        'access_token': access_token,
    }, 200


@app.route('/my-info')
@validate_access_token
def get_my_info(decoded_data):
    id = decoded_data.get('user').get('id')
    employee = Employees.query.filter_by(id=id).first()
    return {
        'employee': employee.to_dict()
    }, 200
