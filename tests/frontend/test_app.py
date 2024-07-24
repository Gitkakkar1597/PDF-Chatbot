# Frontend unit testing
# Test the Streamlit application

import pytest
from unittest.mock import patch
import requests

# Fixture to mock the requests.post method
@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock_post:
        yield mock_post

# Test the successful upload of a PDF file
def test_upload_pdf_success(mock_requests_post):
    # Mock the response from the server
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {"message": "PDF uploaded successfully."}
    
    # Simulate the Streamlit file uploader
    response = requests.post("http://127.0.0.1:8000/upload_pdf/", files={"file": ("sample.pdf", b"pdf content", "application/pdf")})
    
    # Assert the response status code and message
    assert response.status_code == 200
    assert response.json() == {"message": "PDF uploaded successfully."}

# Test the upload of an invalid file format
def test_upload_pdf_invalid_format(mock_requests_post):
    # Mock the response from the server for invalid file format
    mock_requests_post.return_value.status_code = 400
    mock_requests_post.return_value.json.return_value = {"detail": "Invalid file format. Detected: text/plain. Please upload a PDF file."}
    
    # Simulate the upload of a text file
    response = requests.post("http://127.0.0.1:8000/upload_pdf/", files={"file": ("sample.txt", b"text content", "text/plain")})
    
    # Assert the response status code and error message
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file format. Detected: text/plain. Please upload a PDF file."}

# Test querying the PDF content successfully
def test_query_pdf_success(mock_requests_post):
    # Mock the response from the server for a query
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {"response": "Answer from the bot"}
    
    # Simulate sending a query to the server
    response = requests.post("http://127.0.0.1:8000/query/", json={"query": "What is this document about?"})
    
    # Assert the response status code and bot's answer
    assert response.status_code == 200
    assert response.json() == {"response": "Answer from the bot"}
