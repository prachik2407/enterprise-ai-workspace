from fastapi import FastAPI

app = FastAPI(
    title = "Enterprise AI Workspace",
    version = "0.1.0"
)


@app.get("/", tags=["General"])
def root() -> dict:
    return {
        "message": "Welcome to Enterprise AI Workspace"
    }


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {
        "status":"healthy"
    }