# main.py
import os
import uuid
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Path as FastApiPath
# Import HTMLResponse to be able to return HTML content
from fastapi.responses import JSONResponse, HTMLResponse

from app.services.pdf_extractor import extract_text_from_pdf
from app.services.data_handler import generate_answer_from_text
from app.database import add_file_record, get_file_record, delete_file_record, get_all_records


app = FastAPI(title="CAG Project API",
              description="API for uploading PDF documents and querying them using Google's Gemini model.",
              version="1.0.0")

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_pdf(
    username: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Endpoint to upload a PDF file.
    Accepts a username and saves file metadata.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
        
    file_id = str(uuid.uuid4())
    file_path = UPLOADS_DIR / f"{file_id}.pdf"
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        add_file_record(file_id, username, file.filename)
            
        return JSONResponse(
            status_code=200, 
            content={
                "message": "File uploaded successfully.",
                "file_id": file_id,
                "username": username
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

@app.post("/query/")
async def query_pdf(file_id: str = Form(...), query: str = Form(...)):
    """
    Endpoint to ask a question about a previously uploaded PDF.
    """
    file_path = UPLOADS_DIR / f"{file_id}.pdf"
    
    if not get_file_record(file_id) or not file_path.exists():
        raise HTTPException(status_code=404, detail="File ID not found.")
        
    try:
        with open(file_path, "rb") as f:
            pdf_text = extract_text_from_pdf(f)
        
        if not pdf_text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        answer = generate_answer_from_text(context=pdf_text, query=query)
        
        return JSONResponse(
            status_code=200,
            content={"question": query, "llm response": answer}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@app.get("/details/all/")
async def get_all_document_details():
    """
    Retrieves metadata for all uploaded documents.
    """
    all_records = get_all_records()
    # We return the values of the dictionary to get a list of records
    return JSONResponse(status_code=200, content=list(all_records.values()))

@app.get("/details/{file_id}")
async def get_document_details(file_id: str = FastApiPath(..., description="The UUID of the file to retrieve details for.")):
    """
    Retrieves metadata for a specific document.
    """
    record = get_file_record(file_id)
    if not record:
        raise HTTPException(status_code=404, detail="File ID not found.")
    return JSONResponse(status_code=200, content=record)


@app.delete("/delete/{file_id}")
async def delete_document(file_id: str = FastApiPath(..., description="The UUID of the file to delete.")):
    """
    Deletes a document and its metadata.
    """
    file_path = UPLOADS_DIR / f"{file_id}.pdf"

    deleted_record = delete_file_record(file_id)
    
    if not deleted_record:
        raise HTTPException(status_code=404, detail="File ID not found in metadata.")
        
    if file_path.exists():
        os.remove(file_path)

    return JSONResponse(
        status_code=200, 
        content={"message": f"Successfully deleted file and its metadata.", "details": deleted_record}
    )

# --- MODIFIED SECTION ---
# The decorator specifies that the default response will be HTML.
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Root endpoint that provides a simple HTML page with a link to the API docs.
    """
    html_content = """
    <html>
    <head>
        <title>CAG Project</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                text-align: center; 
                margin: 40px; 
                background-color: #f7f7f7;
                color: #333;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            h1 { color: #0056b3; }
            p { font-size: 1.1em; line-height: 1.6; }
            a.button { 
                display: inline-block; 
                padding: 12px 24px; 
                margin-top: 25px; 
                background-color: #007BFF; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            a.button:hover { background-color: #0056b3; }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                font-size: 0.9em;
                color: #777;
            }
            .footer p {
                font-size: 1em;
                line-height: 1.5;
                margin: 5px 0;
            }
            .footer a {
                color: #007BFF;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
            /* Special styling for your name */
            .developer-name {
                background: linear-gradient(135deg, #6e8efb, #a777e3);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                font-weight: 700;
                font-size: 1.2em;
                padding: 2px 6px;
                border-radius: 4px;
                display: inline-block;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            .developer-title {
                font-size: 1.1em;
                margin-top: 5px;
                font-weight: 500;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to My CAG Project</h1>
            <p>This API allows you to upload PDF documents and ask questions about them using Google's Gemini model.</p>
            <p>Click the button below to go to the interactive API documentation (Swagger UI) where you can test all the endpoints.</p>
            <a href="/docs" class="button">Go to API Docs</a>
            
            <div class="footer">
                <p class="developer-title">Project Developed by</p>
                <span class="developer-name">Ashna Imtiaz</span>
                <p>Final project for the Awfera LMS Python Programming Course</p>
                <p>
                    Built with FastAPI & Google Gemini.
                </p>
                <p>
                    <a href="https://github.com/AshnaXhaikh/Awfera_python_project" target="_blank">View Source on GitHub</a> | 
                    <a href="https://linkedin.com/in/ashna-imtiaz-538335284" target="_blank">LinkedIn</a>
                </p>
            </div>
        </div>
    </body>
</html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)