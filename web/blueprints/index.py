from flask import Blueprint, render_template
from flask import current_app as app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)

index_template = Blueprint('index', __name__, template_folder='../templates',static_folder='../static')

@index_template.route('/', methods=["GET"])
def index():
    '''
    Display home page based on authentication status.
    '''
    if current_user.is_authenticated:
        # If authenticated should render mainpage.html
        return render_template('mainpage.html', name=current_user.name, email=current_user.email)
    else:
        return render_template('index.html')
