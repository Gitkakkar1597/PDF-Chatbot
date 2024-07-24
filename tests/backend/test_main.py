# Backend unit testing
# Test the FastAPI endpoints

from fastapi.testclient import TestClient
from main import app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)

# Test the successful upload of a PDF file
def test_upload_pdf_success():
    # Open a sample PDF file in binary read mode
    with open("sample.pdf", "rb") as f:
        # Send a POST request to the /upload_pdf/ endpoint with the PDF file
        response = client.post("/upload_pdf/", files={"file": ("sample.pdf", f, "application/pdf")})
    # Assert the response status code and message
    assert response.status_code == 200
    assert response.json() == {"message": "PDF uploaded successfully."}

# Test the upload of an invalid file format
def test_upload_pdf_invalid_format():
    # Send a POST request to the /upload_pdf/ endpoint with a text file
    response = client.post("/upload_pdf/", files={"file": ("sample.txt", ("text", "text/plain"))})
    # Assert the response status code and error message
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file format. Detected: text/plain. Please upload a PDF file."}

# Test querying without any PDF content uploaded
def test_query_pdf_no_content():
    # Send a POST request to the /query/ endpoint with a query
    response = client.post("/query/", json={"query": "What is this document about?"})
    # Assert the response status code and error message
    assert response.status_code == 400
    assert response.json() == {"detail": "No PDF content available. Please upload a PDF first."}

# Test querying the PDF content successfully
def test_query_pdf_success():
    # Open a sample PDF file in binary read mode and upload it
    with open("sample.pdf", "rb") as f:
        client.post("/upload_pdf/", files={"file": ("sample.pdf", f, "application/pdf")})
    # Send a POST request to the /query/ endpoint with a query
    response = client.post("/query/", json={"query": "What is this document about?"})
    # Assert the response status code and check if the response contains the key "response"
    assert response.status_code == 200
    assert "response" in response.json()
