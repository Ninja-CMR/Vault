from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import auth, vault, secret, tools

# Création des tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vault API", version="1.0.0")

# Configuration CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(auth.router)
app.include_router(vault.router)
app.include_router(secret.router)
app.include_router(tools.router)

@app.get("/")
def root():
    return {"message": "Bonjour Vault - API opérationnelle"}