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

pages_template = Blueprint('pages', __name__, template_folder='../templates',static_folder='../static')

@pages_template.route('/mainpage')
#@login_required
def mainpage():
    '''
    Render mainpage with group data from user logged in.
    '''
    return render_template('mainpage.html')

@pages_template.route('/mgevents')
@login_required
def manage_events():
    '''
    Render event management page for user logged in.
    '''
    return render_template('manage_events.html')

@pages_template.route('/profile', methods=["GET"])
@login_required
def profile():
    '''
    Render profile page for user logged in.
    '''
    return render_template('profile.html', name=current_user.name, email=current_user.email, createdAt=current_user.createdAt)
