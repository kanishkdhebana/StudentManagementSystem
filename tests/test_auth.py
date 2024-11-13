import pytest
from app import app, user_db
from models.users import User, UserType
from sqlalchemy import text

@pytest.fixture(autouse=True)
def rollback_session():
    """Ensure that database changes are rolled back after each test."""
    with app.app_context():
        user_db.session.begin()

        user_db.session.execute(text("TRUNCATE TABLE users"))

        yield  

        user_db.session.rollback()
        user_db.session.remove()  

@pytest.fixture
def test_user():
    """
    Fixture to create a test user, ensuring no duplicates.
    """
    with app.app_context():
        user = User(
            user_id='testuser0',
            user_type=UserType.admin
        )
        user.set_password('testpassword')
        user_db.session.add(user)
        user_db.session.commit()

    return user


@pytest.fixture
def test_client():
    """
    Fixture for setting up a test client for Flask with a MariaDB database.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1324@db/studentmanagementsystem'

    # Create the tables 
    with app.app_context():
        user_db.create_all()

    with app.test_client() as client:
        yield client


def test_login_success(test_client, test_user):
    """
    Test successful login.
    """
    response = test_client.post('/login', data={
        'user_id': 'testuser0',
        'user_password': 'testpassword'
    })
    assert response.status_code == 302  # Should redirect
    assert response.location.endswith('/admin')


def test_logout(test_client, test_user):
    """
    Test successful logout.
    """
    # Login first
    test_client.post('/login', data={
        'user_id': 'testuser0',
        'user_password': 'testpassword'
    })
    
    # Then test the logout
    response = test_client.get('/logout')
    assert response.status_code == 302  # Should redirect
    assert response.location.endswith('/login')


def test_login_failure(test_client):
    """
    Test failed login due to incorrect user credentials.
    """
    response = test_client.post('/login', data={
        'user_id': 'wronguser',
        'user_password': 'wrongpassword'
    })
    assert b'Invalid user ID or password' in response.data
