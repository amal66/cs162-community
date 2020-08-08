import os
import tempfile

import pytest

from web import app, db


# _____ fake Identity Provider ______

# _____________

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_main_page(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert rv.status_code == 200

def test_users_page(client):
    rv = client.get('/users')
    assert rv.status_code == 200

# TBD: mock out google provider???
# def test_login_page(client):
#     rv = client.get('/login', follow_redirects=True)
#     assert rv.status_code == 200
#
# def test_logged_in_page(client):
#     rv = client.get('/', follow_redirects=True)
#     assert rv.status_code == 200
#     assert rv.assert_template_used('logged_in.html')
