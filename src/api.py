from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from src.routers.mensagens import router as mensagens_router  # Importando corretamente
from src.scheduler import iniciar_scheduler
from src.routers.agendamento_router import router as agendamento_router
from src.api_module import auth
from src.middlewares.redirect_unauthorized import RedirectUnauthorizedMiddleware
from src.routers.usuario_route import router as usuario_route

import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="API de Disparador de Mensagens", 
    version="1.0.0"
)

# Iniciar o agendador de tarefas ao iniciar o FastAPI
iniciar_scheduler()

BASE_DIR = Path(__file__).resolve().parent.parent
PAGES_DIR = BASE_DIR / "pages"

app.mount("/pages", StaticFiles(directory="pages"), name="pages")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(RedirectUnauthorizedMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "fallback-key")
)
# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(auth.router)
app.include_router(mensagens_router)
app.include_router(agendamento_router)
app.include_router(usuario_route)

# Servir páginas HTML
@app.get("/login")
async def serve_login():
    return FileResponse("pages/login.html")

@app.get("/")
async def serve_index():
    return FileResponse("pages/grupos.html")

@app.get("/grupos/")
async def serve_list():
    return FileResponse("pages/grupos.html")

@app.get("/add")
async def serve_grupos():
    return FileResponse("pages/add.html")

@app.get("/edit/{group_id}")
async def serve_edit(group_id: int):
    return FileResponse(PAGES_DIR / "edit.html")

@app.get("/view/{group_id}")
async def serve_view(group_id: int):
    return FileResponse("pages/view.html")

@app.get("/agendamento/add")
async def serve_create_agenda():
    return FileResponse("pages/agendamentos/add.html")

@app.get("/agendamentos/")
async def serve_create_agenda():
    return FileResponse("pages/agendamentos/index.html")

@app.get("/mensagens/")
async def serve_list_mensagens():
    return FileResponse("pages/mensagens/index.html")

@app.get("/mensagens/add")
async def serve_add_mensagens():
    return FileResponse("pages/mensagens/add.html")

@app.get("/mensagens/edit/{mensagem_id}")
async def serve_edit_mensagens():
    return FileResponse("pages/mensagens/edit.html")



# uvicorn src.api:app --reload