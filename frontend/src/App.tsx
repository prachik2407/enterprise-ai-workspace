import { FormEvent, useCallback, useEffect, useMemo, useState } from 'react'
import {
  ArrowRight, Bot, Check, ChevronDown, CircleHelp, FileSpreadsheet, FileText,
  FileUp, LoaderCircle, LogOut, MessageSquareText, Plus, ShieldCheck,
  Sparkles, Trash2, UploadCloud, UserRound, X,
} from 'lucide-react'

type User = { id: string; full_name: string; email: string; is_active: boolean }
type DocumentItem = { id: string; filename: string; content_type: string; size: number; status: string; created_at: string }
type Source = { document: string; document_id: string; chunk: string }
type ChatMessage = { role: 'user' | 'assistant'; content: string; sources?: Source[] }

const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')
const TOKEN_KEY = 'eaw_access_token'
const USER_KEY = 'eaw_user'

async function api<T>(path: string, token?: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (response.status === 204) return undefined as T
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = typeof payload.detail === 'string' ? payload.detail : `Request failed (${response.status})`
    throw new Error(detail)
  }
  return payload as T
}

function prettySize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function fileIcon(filename: string) {
  return /\.xlsx?$|\.csv$/i.test(filename) ? <FileSpreadsheet size={19} /> : <FileText size={19} />
}

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [user, setUser] = useState<User | null>(() => {
    try { return JSON.parse(localStorage.getItem(USER_KEY) || 'null') } catch { return null }
  })
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [authBusy, setAuthBusy] = useState(false)
  const [authError, setAuthError] = useState('')
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [loadingDocuments, setLoadingDocuments] = useState(false)
  const [uploadBusy, setUploadBusy] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [notice, setNotice] = useState('')
  const [question, setQuestion] = useState('')
  const [chatBusy, setChatBusy] = useState(false)
  const [chatError, setChatError] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: 'Hi! Upload a document, then ask me a question. I will answer from your indexed documents and show the sources used.' },
  ])
  const [activeTab, setActiveTab] = useState<'workspace' | 'documents'>('workspace')

  const signOut = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setToken(''); setUser(null); setDocuments([])
    setMessages([{ role: 'assistant', content: 'You are signed out. Sign in again to continue.' }])
  }, [])

  const loadDocuments = useCallback(async () => {
    if (!token) return
    setLoadingDocuments(true)
    try { setDocuments(await api<DocumentItem[]>('/api/v1/documents', token)) }
    catch (error) { setNotice(error instanceof Error ? error.message : 'Could not load documents.') }
    finally { setLoadingDocuments(false) }
  }, [token])

  useEffect(() => { if (token) void loadDocuments() }, [token, loadDocuments])

  async function submitAuth(event: FormEvent) {
    event.preventDefault(); setAuthBusy(true); setAuthError('')
    try {
      if (authMode === 'register') {
        await api<User>('/api/v1/auth/register', undefined, {
          method: 'POST', body: JSON.stringify({ full_name: fullName.trim(), email: email.trim(), password }),
        })
      }
      const login = await api<{ access_token: string; token_type: string }>('/api/v1/auth/login', undefined, {
        method: 'POST', body: JSON.stringify({ email: email.trim(), password }),
      })
      const currentUser = await api<User>('/api/v1/auth/me', login.access_token)
      localStorage.setItem(TOKEN_KEY, login.access_token)
      localStorage.setItem(USER_KEY, JSON.stringify(currentUser))
      setToken(login.access_token); setUser(currentUser); setPassword('')
    } catch (error) { setAuthError(error instanceof Error ? error.message : 'Authentication failed.') }
    finally { setAuthBusy(false) }
  }

  async function uploadFiles(files: FileList | null) {
    if (!files?.length || !token) return
    setUploadBusy(true); setUploadError(''); setNotice('')
    try {
      for (const file of Array.from(files)) {
        const form = new FormData(); form.append('file', file)
        const result = await api<{ message: string; filename: string }>('/api/v1/documents/upload', token, { method: 'POST', body: form })
        setNotice(`${result.filename}: ${result.message}`)
      }
      await loadDocuments()
    } catch (error) { setUploadError(error instanceof Error ? error.message : 'Upload failed.') }
    finally { setUploadBusy(false) }
  }

  async function deleteDocument(doc: DocumentItem) {
    if (!token || !window.confirm(`Delete “${doc.filename}” and its indexed chunks?`)) return
    try {
      await api<void>(`/api/v1/documents/${doc.id}`, token, { method: 'DELETE' })
      setDocuments(items => items.filter(item => item.id !== doc.id))
      setNotice(`${doc.filename} was deleted.`)
    } catch (error) { setNotice(error instanceof Error ? error.message : 'Delete failed.') }
  }

  async function askQuestion(event: FormEvent) {
    event.preventDefault()
    const prompt = question.trim()
    if (!prompt || !token || chatBusy) return
    setQuestion(''); setChatError(''); setChatBusy(true)
    setMessages(current => [...current, { role: 'user', content: prompt }])
    try {
      const result = await api<{ answer: string; sources: Source[] }>('/api/v1/chat/ask', token, {
        method: 'POST', body: JSON.stringify({ question: prompt }),
      })
      setMessages(current => [...current, { role: 'assistant', content: result.answer, sources: result.sources }])
    } catch (error) {
      const message = error instanceof Error ? error.message : 'The assistant could not answer.'
      setChatError(message)
      setMessages(current => [...current, { role: 'assistant', content: 'I could not complete that request. Please check the API configuration and try again.' }])
    } finally { setChatBusy(false) }
  }

  const processedCount = useMemo(() => documents.filter(doc => doc.status.toLowerCase() === 'processed').length, [documents])

  if (!token || !user) {
    return <main className="auth-shell">
      <section className="auth-story">
        <div className="brand brand-light"><div className="brand-mark"><Sparkles size={22} /></div><span>Enterprise<span className="brand-muted">AI</span></span></div>
        <div className="story-copy"><span className="eyebrow"><span className="eyebrow-dot" /> YOUR PRIVATE KNOWLEDGE SPACE</span><h1>Turn your documents into <em>answers.</em></h1><p>Upload the information you trust. Ask better questions. Get grounded answers with source references.</p>
          <div className="story-points"><div><ShieldCheck size={18} /><span>Private, user-scoped document retrieval</span></div><div><Sparkles size={18} /><span>AI answers grounded in your files</span></div><div><FileText size={18} /><span>PDF, DOCX, CSV and XLSX support</span></div></div></div>
        <div className="story-footer">Built for focused work · Powered by retrieval-augmented generation</div>
      </section>
      <section className="auth-panel"><div className="auth-card"><div className="mobile-brand brand"><div className="brand-mark"><Sparkles size={20} /></div><span>Enterprise<span className="brand-muted">AI</span></span></div><span className="eyebrow">WELCOME TO YOUR WORKSPACE</span><h2>{authMode === 'login' ? 'Sign in to continue' : 'Create your account'}</h2><p className="muted">{authMode === 'login' ? 'Pick up where your knowledge work left off.' : 'Create a secure workspace for your documents.'}</p>
          <form className="auth-form" onSubmit={submitAuth}>{authMode === 'register' && <label>Full name<input autoComplete="name" required maxLength={100} value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Your name" /></label>}<label>Email address<input type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} placeholder="you@company.com" /></label><label>Password<input type="password" autoComplete={authMode === 'login' ? 'current-password' : 'new-password'} required minLength={8} maxLength={72} value={password} onChange={e => setPassword(e.target.value)} placeholder="At least 8 characters" /></label>{authError && <div className="alert alert-error">{authError}</div>}<button className="button button-primary button-wide" disabled={authBusy}>{authBusy ? <LoaderCircle className="spin" size={18} /> : null}{authMode === 'login' ? 'Sign in' : 'Create account'}<ArrowRight size={17} /></button></form>
          <div className="auth-switch">{authMode === 'login' ? 'New to the workspace?' : 'Already have an account?'} <button onClick={() => { setAuthMode(authMode === 'login' ? 'register' : 'login'); setAuthError('') }}>{authMode === 'login' ? 'Create account' : 'Sign in'}</button></div><div className="secure-note"><ShieldCheck size={15} /> Your documents are scoped to your account</div></div></section>
    </main>
  }

  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><div className="brand-mark"><Sparkles size={21} /></div><span>Enterprise<span className="brand-muted">AI</span></span></div><div className="workspace-label">WORKSPACE <ChevronDown size={14} /></div><nav className="side-nav"><button className={activeTab === 'workspace' ? 'nav-item active' : 'nav-item'} onClick={() => setActiveTab('workspace')}><MessageSquareText size={18} /> AI Assistant</button><button className={activeTab === 'documents' ? 'nav-item active' : 'nav-item'} onClick={() => setActiveTab('documents')}><FileText size={18} /> My documents <span className="nav-count">{documents.length}</span></button></nav><div className="sidebar-bottom"><div className="side-help"><div className="help-icon"><CircleHelp size={17} /></div><div><strong>Need a hand?</strong><span>Ask your docs a question</span></div></div><div className="profile"><div className="avatar"><UserRound size={18} /></div><div className="profile-copy"><strong>{user.full_name}</strong><span>{user.email}</span></div><button className="icon-button signout" title="Sign out" onClick={signOut}><LogOut size={17} /></button></div></div></aside>
    <main className="main-panel"><header className="topbar"><div className="breadcrumb">Workspace <span>/</span> <strong>{activeTab === 'workspace' ? 'AI Assistant' : 'My documents'}</strong></div><div className="topbar-right"><span className="status-pill"><span /> System ready</span><div className="top-avatar">{user.full_name.slice(0, 1).toUpperCase()}</div></div></header>
      {activeTab === 'workspace' ? <section className="workspace-content"><div className="welcome-row"><div><div className="eyebrow"><Sparkles size={14} /> DOCUMENT INTELLIGENCE</div><h1>Your knowledge, <em>in conversation.</em></h1><p>Ask questions across your uploaded documents and explore the sources behind every answer.</p></div><div className="welcome-art"><div className="art-orbit orbit-one" /><div className="art-orbit orbit-two" /><div className="art-core"><Bot size={35} /></div><div className="art-chip chip-a"><FileText size={16} /></div><div className="art-chip chip-b"><Sparkles size={16} /></div></div></div>
        <div className="stats-row"><div className="stat-card"><div className="stat-icon purple"><FileText size={19} /></div><div><span>Indexed documents</span><strong>{processedCount}</strong></div></div><div className="stat-card"><div className="stat-icon mint"><ShieldCheck size={19} /></div><div><span>Private workspace</span><strong>Protected</strong></div></div><div className="stat-card"><div className="stat-icon blue"><Sparkles size={19} /></div><div><span>Answer engine</span><strong>RAG enabled</strong></div></div></div>
        <div className="work-grid"><section className="chat-card"><div className="card-heading"><div className="assistant-avatar"><Bot size={20} /></div><div><h2>Ask your documents</h2><p>Answers are generated from your indexed files</p></div><span className="live-label"><span /> LIVE</span></div><div className="chat-messages">{messages.map((message, index) => <div className={`message-row ${message.role}`} key={`${index}-${message.role}`}><div className="message-avatar">{message.role === 'assistant' ? <Sparkles size={15} /> : <UserRound size={15} />}</div><div className="message-body"><div className="message-label">{message.role === 'assistant' ? 'AI ASSISTANT' : 'YOU'}</div><div className="message-bubble">{message.content}</div>{message.sources && message.sources.length > 0 && <div className="sources"><div className="sources-title"><Check size={14} /> SOURCES USED</div>{message.sources.map((source, sourceIndex) => <div className="source-item" key={`${source.document_id}-${source.chunk}-${sourceIndex}`}><FileText size={14} /><span>{source.document}</span><small>Chunk {source.chunk}</small></div>)}</div>}</div></div>)}{chatBusy && <div className="message-row assistant"><div className="message-avatar"><Sparkles size={15} /></div><div className="message-body"><div className="message-label">AI ASSISTANT</div><div className="message-bubble thinking"><span /><span /><span /> Thinking through your documents…</div></div></div>}</div>
          {chatError && <div className="inline-error">{chatError}</div>}<form className="chat-composer" onSubmit={askQuestion}><textarea value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void askQuestion(e as unknown as FormEvent) } }} placeholder="Ask a question about your documents…" maxLength={2000} rows={2} /><div className="composer-bottom"><span><ShieldCheck size={13} /> Answers grounded in your documents</span><button className="send-button" type="submit" disabled={chatBusy || !question.trim()} aria-label="Send question">{chatBusy ? <LoaderCircle className="spin" size={17} /> : <ArrowRight size={18} />}</button></div></form></section>
          <aside className="right-column"><section className="upload-card"><div className="section-title"><div><h2>Knowledge base</h2><p>Keep your source files close</p></div><span className="count-badge">{documents.length}</span></div><label className={`drop-zone ${uploadBusy ? 'uploading' : ''}`} onDragOver={e => e.preventDefault()} onDrop={e => { e.preventDefault(); void uploadFiles(e.dataTransfer.files) }}><input type="file" accept=".pdf,.docx,.csv,.xlsx" multiple disabled={uploadBusy} onChange={e => { void uploadFiles(e.target.files); e.currentTarget.value = '' }} /><div className="upload-symbol">{uploadBusy ? <LoaderCircle className="spin" size={22} /> : <UploadCloud size={23} />}</div><strong>{uploadBusy ? 'Processing documents…' : 'Click to upload files'}</strong><span>or drag files here</span><small>PDF, DOCX, CSV, XLSX · Up to 25 MB</small></label>{uploadError && <div className="alert alert-error compact">{uploadError}</div>}{notice && <div className="alert alert-success compact"><Check size={14} />{notice}</div>}<div className="document-list-head"><strong>Recent documents</strong><button onClick={() => setActiveTab('documents')}>View all <ArrowRight size={13} /></button></div>{loadingDocuments ? <div className="empty-docs"><LoaderCircle className="spin" size={18} /> Loading files…</div> : documents.length === 0 ? <div className="empty-docs"><FileUp size={22} /><span>Your knowledge base is empty.</span><small>Upload a file to get started.</small></div> : <div className="mini-doc-list">{documents.slice(0, 4).map(doc => <div className="mini-doc" key={doc.id}><div className="doc-type-icon">{fileIcon(doc.filename)}</div><div className="mini-doc-info"><strong title={doc.filename}>{doc.filename}</strong><span>{prettySize(doc.size)} · {doc.status.toLowerCase()}</span></div><span className={`doc-status ${doc.status.toLowerCase()}`} title={doc.status}><Check size={12} /></span></div>)}</div>}</section><section className="tip-card"><div className="tip-icon"><Sparkles size={17} /></div><div><strong>Get better answers</strong><p>Ask specific questions. The assistant cites source documents so you can verify the information.</p></div></section></aside></div><footer className="page-footer"><span>Enterprise AI Workspace</span><span>Grounded answers · Source transparency · Private retrieval</span></footer></section> : <section className="documents-page"><div className="documents-title"><div><div className="eyebrow"><FileText size={14} /> KNOWLEDGE LIBRARY</div><h1>My documents</h1><p>Manage the files available to your private AI assistant.</p></div><label className="button button-primary upload-cta"><Plus size={17} /> Add documents<input type="file" accept=".pdf,.docx,.csv,.xlsx" multiple disabled={uploadBusy} onChange={e => { void uploadFiles(e.target.files); e.currentTarget.value = '' }} /></label></div>{uploadError && <div className="alert alert-error">{uploadError}</div>}{notice && <div className="alert alert-success"><Check size={14} />{notice}</div>}<div className="documents-table-card"><div className="table-toolbar"><strong>{documents.length} {documents.length === 1 ? 'document' : 'documents'}</strong><button className="button button-quiet" onClick={() => void loadDocuments()}><LoaderCircle size={15} className={loadingDocuments ? 'spin' : ''} /> Refresh</button></div>{loadingDocuments ? <div className="table-empty">Loading your documents…</div> : documents.length === 0 ? <div className="table-empty"><FileUp size={28} /><strong>No documents yet</strong><span>Upload a PDF, DOCX, CSV or XLSX file to begin.</span></div> : <div className="table-scroll"><table><thead><tr><th>NAME</th><th>SIZE</th><th>STATUS</th><th>UPLOADED</th><th /></tr></thead><tbody>{documents.map(doc => <tr key={doc.id}><td><div className="table-file"><div className="doc-type-icon">{fileIcon(doc.filename)}</div><div><strong>{doc.filename}</strong><small>{doc.content_type}</small></div></div></td><td>{prettySize(doc.size)}</td><td><span className={`status-tag ${doc.status.toLowerCase()}`}><span />{doc.status}</span></td><td>{new Date(doc.created_at).toLocaleDateString()}</td><td><button className="icon-button delete-button" title={`Delete ${doc.filename}`} onClick={() => void deleteDocument(doc)}><Trash2 size={16} /></button></td></tr>)}</tbody></table></div>}</div><div className="privacy-banner"><ShieldCheck size={19} /><div><strong>Your documents stay scoped to your account</strong><span>Retrieval filters by your authenticated user ID before the AI model receives context.</span></div></div><footer className="page-footer"><span>Enterprise AI Workspace</span><span>Grounded answers · Source transparency · Private retrieval</span></footer></section>}
    </main>
  </div>
}
