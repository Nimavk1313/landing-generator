from app.models import User, Page

def test_user_model(client):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('password') is True
    assert user.check_password('wrongpassword') is False

def test_page_model(client):
    user = User(username='testuser', email='test@example.com')
    page = Page(author=user, impressions=10, clicks=5)
    assert page.author == user
    assert page.impressions == 10
    assert page.clicks == 5
