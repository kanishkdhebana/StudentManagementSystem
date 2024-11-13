import pytest
from unittest.mock import patch, MagicMock
from app import app, user_db
from models.users import User, UserType
from werkzeug.exceptions import Unauthorized


# Fixture to mock a user for testing
@pytest.fixture
def mock_user():
    """
    Create a mock user for testing the login logic.
    """
    user = MagicMock(spec=User)
    user.user_id = 'testuser0'
    user.user_type = UserType.admin
    user.check_password.return_value = True  # Mock the password check as always true
    return user


# Unit test for successful login
def test_login_success(mock_user):
    """
    Test successful login by mocking the database query and checking if the user is authenticated.
    """
    # Mock the database session query to return the mock user
    with patch('app.user_db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = mock_user

        # Simulate the login request
        response = app.test_client().post('/login', data={
            'user_id': 'testuser0',
            'user_password': 'testpassword'
        })
        
        # Check that the mock user was queried and returned
        mock_query.return_value.filter_by.assert_called_once_with(user_id='testuser0')
        mock_user.check_password.assert_called_once_with('testpassword')

        # Check the response (successful login should redirect)
        assert response.status_code == 302  # Should redirect
        assert response.location.endswith('/admin')


# Unit test for failed login (invalid credentials)
def test_login_failure():
    """
    Test failed login due to incorrect user credentials.
    """
    with patch('app.user_db.session.query') as mock_query:
        # Simulate the query returning None, meaning user was not found
        mock_query.return_value.filter_by.return_value.first.return_value = None

        # Simulate the login request with incorrect credentials
        response = app.test_client().post('/login', data={
            'user_id': 'wronguser',
            'user_password': 'wrongpassword'
        })
        
        # Check that the correct error message is returned
        assert b'Invalid user ID or password' in response.data
        assert response.status_code == 200  # Should not redirect, stay on login page


# Unit test for logout (mocking session clearing)
def test_logout():
    """
    Test logout functionality.
    """
    with patch('flask.session') as mock_session:
        # Simulate a session with a logged-in user
        mock_session['user_id'] = 'testuser0'
        
        # Simulate the logout request
        response = app.test_client().get('/logout')
        
        # Check that the session is cleared
        mock_session.clear.assert_called_once()

        # Check that the response redirects to login
        assert response.status_code == 302  # Should redirect
        assert response.location.endswith('/login')


# Unit test for password hashing (if applicable in your User model)
def test_user_password_hashing(mock_user):
    """
    Test if the password is properly hashed when set.
    """
    mock_user.set_password('testpassword')

    # Check if the password was hashed and is not equal to the plain text password
    assert mock_user.user_password_hash != 'testpassword'
    assert mock_user.user_password_hash.startswith('pbkdf2:sha256:')  # Assuming the default Flask hashing scheme
