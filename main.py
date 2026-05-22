import os
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

app = FastAPI(title="Frontend - DocIA")

# Resolve o problema de HTTP/HTTPS no Azure (Mixed Content)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Monta a pasta estática para o CSS e Imagens funcionarem
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura a pasta onde estão os HTMLs
templates = Jinja2Templates(directory="templates")

@app.get("/api-config.js")
async def api_config_js():
    """Gera um arquivo JS dinâmico com as URLs dos microserviços vindas do ambiente."""
    auth_url = os.getenv("AUTH_API_URL", "http://localhost:8001")
    empresas_url = os.getenv("EMPRESAS_API_URL", "http://localhost:8002")
    projetos_url = os.getenv("PROJETOS_API_URL", "http://localhost:8003")
    upload_url = os.getenv("UPLOAD_FRONTEND_URL", "http://localhost:5000")
    diagramas_url = (
        os.getenv("Diagramas_FRONTEND_URL")
        or os.getenv("DIAGRAMAS_FRONTEND_URL")
        or "http://localhost:5000"
    )


    js_content = f"""
    window.API_CONFIG = {{
        auth: "{auth_url}",
        empresas: "{empresas_url}",
        projetos: "{projetos_url}",
        upload: "{upload_url}",
        diagramas: "{diagramas_url}"
    }};
    """
    return Response(content=js_content, media_type="application/javascript")

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/")
@app.post("/login")
async def login_post(request: Request):
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro_get(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/cadastro")
async def cadastro_post(request: Request):
    return RedirectResponse(url="/login", status_code=303)

@app.get("/esqueceu-senha", response_class=HTMLResponse)
async def esqueceu_senha_get(request: Request):
    return templates.TemplateResponse("esqueceu_senha.html", {"request": request})

@app.post("/esqueceu-senha")
async def esqueceu_senha_post(request: Request):
    return RedirectResponse(url="/confirmacao-senha", status_code=303)

@app.get("/confirmacao-senha", response_class=HTMLResponse)
async def confirmacao_senha(request: Request):
    return templates.TemplateResponse("confirmacao_senha.html", {"request": request})

@app.get("/criar-senha", response_class=HTMLResponse)
async def criar_senha_get(request: Request):
    return templates.TemplateResponse("criar_senha.html", {"request": request})

@app.post("/criar-senha")
async def criar_senha_post(request: Request):
    return RedirectResponse(url="/login", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/perfil", response_class=HTMLResponse)
async def perfil(request: Request):
    return templates.TemplateResponse("perfil.html", {"request": request})

@app.get("/projeto", response_class=HTMLResponse)
async def projeto(request: Request):
    return templates.TemplateResponse("projeto.html", {"request": request})

@app.get("/empresa", response_class=HTMLResponse)
async def empresa(request: Request):
    return templates.TemplateResponse("empresa.html", {"request": request})

@app.get("/empresa/membros", response_class=HTMLResponse)
async def empresa_membros(request: Request):
    return templates.TemplateResponse("empresa_membros.html", {"request": request})

@app.get("/empresa/solicitacoes", response_class=HTMLResponse)
async def empresa_solicitacoes(request: Request):
    return templates.TemplateResponse("empresa_solicitacoes.html", {"request": request})

@app.get("/empresa/configuracoes", response_class=HTMLResponse)
async def empresa_configuracoes(request: Request):
    return templates.TemplateResponse("empresa_configuracoes.html", {"request": request})

@app.get("/projeto/membros", response_class=HTMLResponse)
async def projeto_membros(request: Request):
    return templates.TemplateResponse("projeto_membros.html", {"request": request})

@app.get("/projeto/solicitacoes", response_class=HTMLResponse)
async def projeto_solicitacoes(request: Request):
    return templates.TemplateResponse("projeto_solicitacoes.html", {"request": request})

@app.get("/projeto/configuracoes", response_class=HTMLResponse)
async def projeto_configuracoes(request: Request):
    return templates.TemplateResponse("projeto_configuracoes.html", {"request": request})

@app.get("/empresas", response_class=HTMLResponse)
async def empresas(request: Request):
    return templates.TemplateResponse("lista_empresas.html", {"request": request})

@app.get("/projetos", response_class=HTMLResponse)
async def projetos(request: Request):
    return templates.TemplateResponse("lista_projetos.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
