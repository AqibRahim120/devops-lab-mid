import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        submissions.clear()
        yield client

def test_valid_submission(client):
    """Test Case 1: Complete details and a valid submission URL -> Saved & displayed."""
    response = client.post('/submit', data={
        'name': 'Aqib Rahim',
        'reg_no': 'CSC-2026-001',
        'title': 'DevOps Lab Mid',
        'url': 'https://github.com/aqib/devops-lab'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Aqib Rahim' in response.data
    assert b'CSC-2026-001' in response.data
    assert b'https://github.com/aqib/devops-lab' in response.data

def test_missing_registration_number(client):
    """Test Case 2: Missing registration number -> Rejected with validation message."""
    response = client.post('/submit', data={
        'name': 'Aqib Rahim',
        'reg_no': '',
        'title': 'DevOps Lab Mid',
        'url': 'https://github.com/aqib/devops-lab'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration number is required' in response.data

def test_invalid_submission_url(client):
    """Test Case 3: Invalid submission URL -> Rejected and not saved."""
    response = client.post('/submit', data={
        'name': 'Aqib Rahim',
        'reg_no': 'CSC-2026-001',
        'title': 'DevOps Lab Mid',
        'url': 'not-a-valid-url'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid submission URL' in response.data
    assert len(submissions) == 0