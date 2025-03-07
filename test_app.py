import pytest
from app import app, db
from db import URL

# Create a fixture that sets up the app and db context
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()  # Keeps context active during test
        db.drop_all()

# Test case for valid URL shortening
def test_shorten_url_valid(client):
    response = client.post('/shorten', json={'url': 'http://example.com'})
    json_data = response.get_json()

    # Check if the response status code is 200 OK
    assert response.status_code == 200
    # Check if the response contains the shortened URL
    assert 'short_url' in json_data
    assert json_data['short_url'].startswith("http://localhost:5000/")

# Test case for exceeding the request limit
def test_request_limit(client):    
    # Simulate the first five requests that should pass
    for i in range(5):
        client.post('/shorten', json={'url': 'http://example.com'})
    
    # Simulate the sixt request that should redirect to delay website
    response = client.post('/shorten', json={'url': 'http://example.com'})
    
    # Check if the rate-limited response is returned
    assert response.status_code == 302  # Redirect should happen
    assert response.location == "https://httpbin.org/delay/5"

# Test case for valid redirection
def test_redirect_url(client):
    # Insert a test URL into the database
    short_code = 'abc123'
    url_entry = URL(original_url='http://example.com', short_code=short_code)
    db.session.add(url_entry)
    db.session.commit()
    
    # Test the redirection
    response = client.get(f'/{short_code}')
    
    # Check if it redirects to the original URL
    assert response.status_code == 302
    assert response.location == 'http://example.com'

# Test case for short code not found (404)
def test_redirect_url_not_found(client):
    response = client.get('/nonexistent')
    json_data = response.get_json()

    # Check if the response status code is 404 for not found
    assert response.status_code == 404
    assert json_data['error'] == "Short URL not found"