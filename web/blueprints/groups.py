from flask import Blueprint, render_template, request, redirect, url_for
from flask import Flask, request, session
from flask_migrate import Migrate
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)
import os
import sys

from models import User, Group, Message, db, user_group

groups_template = Blueprint('groups', __name__, template_folder='../templates',static_folder='../static')
@groups_template.route('/groups', methods=['GET'])
@login_required
def show_groups():
    '''
    Show groups and create relationship between user and group (membership).
    '''
    groups = Group.query.all()
    membership = []
    for g in groups:

        relationship = bool(db.session.query(User).filter(user_group.c.user_id == current_user.id).filter(user_group.c.group_id == g.id).first())
        membership.append(relationship)
    return render_template('groups.html', membership=membership, groups=groups)

@groups_template.route('/groups/<group_id>/users/new', methods=['POST'])
@login_required
def join_group(group_id):
    '''
    Allow a user to join a group and redirect to homepage once done.
    '''
    # get user_id here
    group = Group.query.get(group_id)

    current_user.groups.append(group)
    group.userCount += 1

    if group.confirmed == False and group.userCount >= 5:
        group.confirmed = True
    db.session.commit()
    return render_template('mainpage.html',groups=current_user.groups)
