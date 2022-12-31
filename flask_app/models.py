from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from flask_app import db


class Users(db.Model, SerializerMixin):
    serialize_only = ('id', 'username', 'created_date',
                      'updated_date', 'employee_id')
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employees.id'), nullable=False)

    def __repr__(self):
        return f"User(username={self.username}," \
               f"created_date={self.created_date}," \
               f"updated_date={self.updated_date})," \
               f"employee_id={self.employee_id})"


class Employees(db.Model, SerializerMixin):

    serialize_only = ('id', 'first_name', 'middle_name', 'last_name',
                      'phone', 'permanent_address', 'secondary_address',
                      'email', 'job_title', 'profile_picture_url', 'created_date',
                      'updated_date', 'user')

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    permanent_address = db.Column(db.String(255), nullable=False)
    secondary_address = db.Column(db.String(255))
    email = db.Column(db.String(60), nullable=False)
    job_title = db.Column(db.String(60), nullable=False)
    profile_picture_url = db.Column(
        db.String(255), default='./images/default.jpg')
    role = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users')

    def __repr__(self) -> str:
        return f"Employee(first_name={self.first_name},middle_name={self.middle_name}," \
            f"last_name={self.last_name},phone={self.phone},permanent_address={self.permanent_address}," \
            f"secondary_address={self.secondary_address},email={self.email}," \
            f"job_title={self.job_title}," \
            f"created_date={self.created_date},updated_date={self.updated_date})"
