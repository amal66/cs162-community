import requests
from web.templates import

def test_basic_request():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

def test_routing_mainpage():
    r = requests.get('http://127.0.0.1:5000/mainpage')
    assert r.status_code == 200
