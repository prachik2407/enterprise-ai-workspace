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
- LangChain `RecursiveCharacterTextSplitter`
- Hugging Face embeddings via LangChain

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
LangChain Text Splitting
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
LangChain Prompt Template
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

### 🧩 LangChain Integration

LangChain components have been integrated incrementally into the existing application architecture while preserving application-level abstractions.

#### Recursive Character Text Splitting

The custom text chunking implementation has been replaced internally with LangChain's `RecursiveCharacterTextSplitter` while preserving the existing application-level `TextChunk` interface.

#### Hugging Face Embeddings

Embedding generation now uses LangChain's `HuggingFaceEmbeddings` adapter with the `all-MiniLM-L6-v2` model.

The application exposes a `BaseEmbeddingService` interface, allowing the underlying embedding implementation to remain replaceable without coupling the rest of the RAG pipeline directly to LangChain.

Embedding dimension: `384`.

#### RAG Prompt Templates

RAG prompt construction now uses LangChain's `ChatPromptTemplate` through a dedicated `RAGPrompt` component.

The prompt enforces:

- Context-grounded answering
- No fabricated information
- Explicit fallback when the answer is not present in the supplied context
- Concise answers
- Protection of internal instructions

The existing `PromptBuilder` remains as an application-level wrapper around the LangChain prompt implementation.

#### Validation
The custom chunker and LangChain splitter were compared using the same DOCX document with:
```Chunk Size: 1000```
```Chunk Overlap: 200```

#### Results:
| Metric               | Custom Chunker | LangChain |
| -------------------- | -------------: | --------: |
| Extracted Characters |          8,281 |     8,281 |
| Number of Chunks     |             11 |        11 |
| First Chunk Length   |            607 |       607 |
| Last Chunk Length    |            293 |       293 |
| Average Chunk Length |            789 |       789 |
RAG retrieval was also tested after the integration and continued to return the correct answer.

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
- LangChain Text Splitters
- LangChain Hugging Face Embeddings
- LangChain Core Prompt Templates

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
- LangChain
- Azure OpenAI

### Planned AI Infrastructure

- Additional LangChain components
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
        PostgreSQL                  File Storage
                                         │
                                         ▼
                                  Document Parsing
                                         │
                                         ▼
                                LangChain Text Splitting
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
                                  User-specific Filtering
                                         │
                                         ▼
                                  RAG Context
                                         │
                                         ▼
                                Prompt Builder
                                         │
                                         ▼
                            LangChain ChatPromptTemplate
                                         │
                                         ▼
                                  Azure OpenAI
                                         │
                                         ▼
                              Grounded AI Response
                                         │
                                         ▼
                                      Sources

## 📊 Project Status

### Completed

- FastAPI backend foundation
- PostgreSQL and SQLAlchemy integration
- JWT authentication
- Protected document APIs
- Document upload and storage
- PDF/DOCX/CSV/XLSX parsing
- Text chunking
- LangChain RecursiveCharacterTextSplitter
- Sentence Transformer embeddings
- LangChain Hugging Face embeddings
- ChromaDB vector storage
- Semantic retrieval
- User-specific vector retrieval
- RAG prompt pipeline
- LangChain RAG prompt templates
- Azure OpenAI integration
- Grounded RAG answer generation
- Source metadata

### In Progress

- Additional LangChain integrations

### Planned

- LangGraph
- AI Data Analyst
- React frontend integration
- Azure AI Search
- Deployment