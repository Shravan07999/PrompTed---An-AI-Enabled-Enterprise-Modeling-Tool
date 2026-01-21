from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from api import prompts, chains, execute, auth, analytics

app = FastAPI(title="Prompt Management Tool API")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router)
app.include_router(prompts.router)
app.include_router(chains.router)
app.include_router(execute.router)
app.include_router(analytics.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Prompt Management Tool API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
