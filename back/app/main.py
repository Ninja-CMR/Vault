from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import auth, vault, secret, tools, security, activity
from app.services.activity_service import ActivityLoggerService
from app.database.database import SessionLocal
import asyncio

# Création des tables de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vault API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    # Tâche répétitive pour flusher les logs
    async def flush_logs_periodically():
        while True:
            await asyncio.sleep(10)  # Flush toutes les 10 secondes
            db = SessionLocal()
            try:
                ActivityLoggerService.flush_logs(db)
            finally:
                db.close()
    
    asyncio.create_task(flush_logs_periodically())

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
app.include_router(security.router)
app.include_router(activity.router)

@app.get("/")
def root():
    return {"message": "Bonjour Vault - API opérationnelle"}