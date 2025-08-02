import json
from app.models import User, Page

def test_api_flow(client):
    # Sign up and log in a user
    client.post('/signup', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)

    # Get the user object
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None

    # Create a page for the user
    page = Page(user_id=user.id)
    from app import db
    db.session.add(page)
    db.session.commit()

    # Test saving page content
    response = client.post('/api/save_page', json={
        'content': [{'type': 'link', 'title': 'My Website', 'url': 'https://example.com'}]
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

    # Verify that the page content was saved
    page = Page.query.filter_by(author=user).first()
    assert page is not None
    content = json.loads(page.content)
    assert len(content) == 1
    assert content[0]['type'] == 'link'

    # Test tracking a click
    response = client.post('/api/track_click', json={'user_id': user.id})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

    # Verify that the click was tracked
    page = Page.query.filter_by(author=user).first()
    assert page.clicks == 1
