from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pdfplumber
from gemini_client import GeminiClient
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

# Allow CORS for Streamlit to interact with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this if you want to restrict the origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = GeminiClient()
pdf_texts = {}

class UserQuery(BaseModel):
    query: str

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_texts

    # Debug: Print content type
    content_type = file.content_type
    print(f"Content-Type: {content_type}")

    # Check content type
    if content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=f"Invalid file format. Detected: {content_type}. Please upload a PDF file.")
    
    # Check file extension (fallback method)
    file_extension = file.filename.split(".")[-1]
    if file_extension.lower() != "pdf":
        raise HTTPException(status_code=400, detail=f"Invalid file format. Detected extension: {file_extension}. Please upload a PDF file.")
    
    try:
        file_bytes = await file.read()
        with io.BytesIO(file_bytes) as pdf_file:
            with pdfplumber.open(pdf_file) as pdf:
                pdf_texts[file.filename] = ""
                for page in pdf.pages:
                    pdf_texts[file.filename] += page.extract_text() + "\n"
        return {"message": "PDF uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the PDF file: {str(e)}")

@app.post("/query/")
async def query_pdf(user_query: UserQuery):
    if not pdf_texts:
        raise HTTPException(status_code=400, detail="No PDF content available. Please upload a PDF first.")
    
    # For simplicity, using text from the first uploaded PDF
    pdf_text = next(iter(pdf_texts.values()))

    # Simple retrieval mechanism: use the full text as context
    context = pdf_text
    
    try:
        response = client.generate_response(context, user_query.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while querying the AI: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Chatbot API! Use /docs for API documentation."}
