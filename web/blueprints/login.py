# Based on https://realpython.com/flask-google-login/
from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from models import User, db
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
import os
import json
from oauthlib.oauth2 import WebApplicationClient
import requests

# _____ CONFIG _____

# Identity Provider vars
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Helper method to get user URL
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

login_template = Blueprint('login', __name__, template_folder='../templates',static_folder='../static')

# _____ ROUTES + CONTROLLERS _____
@login_template.route('/login')
def login():
    '''
    On login, redirect to Google authentication.
    '''

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@login_template.route("/login/callback")
def callback():
    '''
    On Google authentication callback, get user information and log user in
    create new user in database if does not exist.
    '''
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Query URL from Google that gives user's profile information, including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified, then get their information.

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User.query.filter_by(email=users_email).first()

    # if user doesn't exist before, add to db
    if user is None:
        user = User(email=users_email, name=users_name) # not dealing w picture for now
        #db.session.merge(user)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    #return render_template('logged_in.html', name=users_name, email=users_email)
    return render_template('mainpage.html', name=users_name, email=users_email, groups=user.groups)


@login_template.route("/logout")
@login_required
def logout():
    '''
    Redirect user to homepage on logout.
    '''
    logout_user()
    return render_template('index.html')
