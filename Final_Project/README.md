# CAG Project: AI-Powered PDF Q&A

**CAG Project** is an intelligent API that transforms static PDF documents into a dynamic, conversational knowledge base. Built using **Python** and **FastAPI**, this application enables users to upload PDF files, ask natural language questions, and receive contextual answers powered by **Google's Gemini 2.0 Flash** model.

This project serves as the capstone of my studies in the **Awfera Python Programming Series**, showcasing skills in backend development, AI integration, and RESTful API design.

Built with FastAPI and Gemini 2.0 Flash, the app allows seamless uploading, parsing, and managing of PDF files.

---

---

## Core Functionalities

- **AI-Powered Q&A**: Uses Google Gemini 2.0 Flash to understand document content and respond to user queries.
- **PDF Upload with UUID**: Automatically assigns a unique UUID to every PDF uploaded for secure identification.
- **Metadata Tracking**: Captures uploader’s name, UUID, filename, and timestamp for every document.
- **Document Management**:
  - View metadata for one or all uploaded documents.
  - Delete individual documents securely.
- **Interactive API Documentation**: Built-in Swagger UI for easy testing and exploration.


---

## 🗂️ Project Structure

cag-project/

├── main.py # Entry point of the FastAPI app

├── app/

│ ├── init.py

│ ├── database.py # Handles metadata storage (UUID, name, timestamp)

│ ├── services/

│ │ ├── init.py

│ │ ├── pdf_extractor.py # Extracts text from uploaded PDFs

│ │ └── gemini_handler.py # Sends extracted text to Gemini model

│ └── core/

│ ├── init.py

│ └── config.py # Environment and API key management
│
├── uploads/

│ └── .gitkeep # Keeps the uploads folder tracked in Git
│
├── metadata.json # Automatically created metadata file

├── .env # Environment variables (e.g., Gemini API key)

├── requirements.txt # Project dependencies

└── README.md # You're here!

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **AI Model**: Google Gemini 2.0 Flash
- **Server**: Uvicorn
- **PDF Parsing**: PyPDF2
- **Data Storage**: Local JSON (`metadata.json`)

---

## ⚙️ Setup and Installation

### ✅ Prerequisites

- Python 3.8+
- Google API Key with access to Gemini 2.0 Flash

---

### 📥 Installation Steps

1. **Clone the Repository**:
```bash
git clone <your-repository-url>
cd CAG-Project
```
Create & Activate a Virtual Environment:
```
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
Install Dependencies:

```
pip install -r requirements.txt
```

Add API Key to .env File:

Create a .env file in the root directory and add:

```
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
```

🚀 Run the Application

From the project root:

```
uvicorn main:app --reload
```
Visit the Welcome Page: http://127.0.0.1:8000/

Access Swagger UI: http://127.0.0.1:8000/docs

