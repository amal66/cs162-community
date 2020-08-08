#! Not functional! only frontend

from flask import Blueprint, render_template
from flask import current_app as app

user_template = Blueprint('user', __name__, template_folder='../templates',static_folder='../static')


@user_template.route('/register')
def register():
    '''
    Render the registration page.
    '''
    return render_template('register.html')



@user_template.route('/forgotpassword')
def forgot_password():
    '''
    Render the forgot password screen.
    '''
    return render_template('forgot_password.html')
