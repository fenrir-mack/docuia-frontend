from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.api.auth_router import router as auth_router
from presentation.api.perfil_router import router as perfil_router
from infrastructure.database.conexao import engine
from infrastructure.database.models import Base

# Cria as tabelas no banco se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DocuIA — MS1 Autenticação",
    description="Microserviço responsável por login, cadastro e perfil de usuários",
    version="1.0.0"
)

# CORS — libera chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://docuia-frontend-hdc8hzfqbqebc6cp.brazilsouth-01.azurewebsites.net",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os routers
app.include_router(auth_router)
app.include_router(perfil_router)


@app.get("/")
def health_check():
    return {"status": "ok", "servico": "ms1_auth"}
