import datetime
from flask_login import LoginManager, UserMixin
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# groups <> users: many to many
# groups <> messages: one to many

# initiate SQLAlchemy db
db = SQLAlchemy()

# create user_group table
user_group = db.Table('user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('createdAt', db.DateTime, default=datetime.datetime.utcnow)
)

class User(UserMixin, db.Model):
    '''
    User table. 
    Columns:
    - user ID, email, createdAt (date of creation), groups
    '''
    __tablename__ = 'user'
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
    groups = db.relationship('Group', secondary='user_group', backref=db.backref('user'), lazy=True) # many to many w association table, lazy load

class Group(db.Model):
    '''
    Group table.
    Columns:
    - name, description, userCount, confirmed (sets if established or not)
    '''
    __tablename__ = 'group'
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.userCount = 0
        self.confirmed = False

    # way to confirm boolean confirmed value
    def confirm(self):
        self.confirmed = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String)
    userCount = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean)
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
    messages = db.relationship('Message', backref='group', lazy=True)

class Message(db.Model):
    '''
    Message table.
    Columns:
    - content, groupid, createdAt (datetime of message sent)
    each message is stored here.
    '''
    __tablename__ = 'message'
    def __init__(self, content, group_id, user_id):
        self.content = content
        self.group_id = group_id
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    createdAt = db.Column(DateTime, default=datetime.datetime.utcnow) # calc independently
