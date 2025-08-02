import pytest
from app.models import User

def test_auth_flow(client):
    # Test signup
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been created!' in response.data
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None

    # Test login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome, testuser!' in response.data

    # Test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
