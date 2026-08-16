# 🚀 Enterprise AI Workspace

An enterprise-grade AI workspace for document intelligence, conversational AI, data analytics, and intelligent agent workflows.

The project is being developed as a full-stack AI application with a FastAPI backend and a React frontend.

---

## ✨ Current Features

### 🔐 Authentication
- User registration
- JWT-based authentication
- Protected API routes
- User-specific resource authorization

### 📄 Document Management
- Document upload
- Local file storage
- Document metadata management
- Document listing
- Document deletion
- Ownership-based authorization
- File type validation
- File size validation

### 📑 Document Processing
- PDF text extraction
- DOCX text extraction
- CSV parsing
- XLSX parsing
- Configurable text chunking
- Overlapping chunks
- Sentence Transformer embeddings

---

### 🔎 Current AI  / RAG Pipeline

```text
Document
    ↓
File Upload
    ↓
Document Parser
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Store
    ↓
Semantic Retrieval
    ↓
User-specific Filtering
    ↓
Context Construction
    ↓
Prompt Construction
    ↓
Azure OpenAI
    ↓
Grounded Answer + Sources
```
### 🤖 RAG Capabilities
- Document indexing
- Semantic document retrieval
- User-specific document filtering
- Context construction
- Prompt construction
- Azure OpenAI integration
- Grounded answer generation
- Source metadata returned with answers

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### AI / ML
- Sentence Transformers
- Hugging Face
- ChromaDB
- Azure OpenAI
- GPT-4.1-mini

### Document Processing
- PyPDF
- python-docx
- Pandas
- OpenPyXL

### Frontend
- React
- TypeScript

### AI Infrastructure
- ChromaDB
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Azure OpenAI

### Planned AI Infrastructure
- LangChain
- LangGraph
- Azure AI Search

### Deployment
- Docker
- Azure
- Vercel

## 🏗️ Architecture

                         User
                           │
                           ▼
                    React Frontend
                           │
                           ▼
                      FastAPI API
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Authentication             Document Management
             │                           │
             ▼                           ▼
        PostgreSQL                File Storage
                                         │
                                         ▼
                                  Document Parsing
                                         │
                                         ▼
                                     Chunking
                                         │
                                         ▼
                                    Embeddings
                                         │
                                         ▼
                                   ChromaDB
                                         │
                                         ▼
                               Semantic Retrieval
                                         │
                                         ▼
                                  RAG Context
                                         │
                                         ▼
                                Prompt Builder
                                         │
                                         ▼
                                  Azure OpenAI
                                         │
                                         ▼
                                  AI Response