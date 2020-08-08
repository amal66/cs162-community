from flask import Blueprint, render_template
from flask import current_app as app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)
from web.models import db, User, Group, Message

chat_template = Blueprint('chat', __name__, template_folder='../templates',static_folder='../static')

@chat_template.route('/chat/<group_id>')
@login_required
def chat(group_id):
    '''
    Direct user to different chat template/mainpage/login
    depending on stage of user.
    '''
    # if not logged in, redirect to login
    if not current_user.is_authenticated:
        return render_template('index.html')

    group = Group.query.get(group_id)
    if not group.confirmed:
        # TODO: flash error message that group doesn't have enough people
        return render_template('mainpage.html', name=current_user.name, email=current_user.email, groups=current_user.groups)

    if group in current_user.groups:

        msgs_w_name = db.session.query(Message, User.name).filter(Message.group_id==group_id).order_by(Message.id.desc()).limit(10)[::-1]
        return render_template('chat.html', user=current_user, group=group, messages = msgs_w_name)
    else:
        return render_template('mainpage.html', name=current_user.name, email=current_user.email, groups=current_user.groups)
