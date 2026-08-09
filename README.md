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

### 📑 Document Processing
- PDF text extraction
- DOCX text extraction
- CSV parsing
- XLSX parsing
- Text chunking with configurable chunk size and overlap
- Sentence Transformer embeddings

### 🔎 Current AI Pipeline

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

### Frontend
- React
- TypeScript

### Planned AI Infrastructure
- Vector Database
- RAG
- LangChain
- LangGraph
- Azure OpenAI
- Azure AI Search

### Deployment
- Docker
- Azure
- Vercel

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
                React Frontend
                      │
                      ▼
                 FastAPI API
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    Authentication          Document Management
          │                       │
          ▼                       ▼
       PostgreSQL          File Storage + Parsing
                                  │
                                  ▼
                              Chunking
                                  │
                                  ▼
                             Embeddings
                                  │
                                  ▼
                           Vector Database
                                  │
                                  ▼
                                RAG
                                  │
                                  ▼
                             AI Response