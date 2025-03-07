from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from src.routers.mensagens import router as mensagens_router  # Importando corretamente
from src.scheduler import iniciar_scheduler
from src.routers.agendamento_router import router as agendamento_router

app = FastAPI(title="API de Mensagens e Convênios")

# Iniciar o agendador de tarefas ao iniciar o FastAPI
iniciar_scheduler()

BASE_DIR = Path(__file__).resolve().parent.parent
PAGES_DIR = BASE_DIR / "pages"

app.mount("/pages", StaticFiles(directory="pages"), name="pages")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(mensagens_router)
app.include_router(agendamento_router)

# Servir páginas HTML
@app.get("/")
async def serve_index():
    return FileResponse("pages/grupos.html")

@app.get("/grupos")
async def serve_list():
    return FileResponse("pages/grupos.html")

@app.get("/add")
async def serve_grupos():
    return FileResponse("pages/add.html")

@app.get("/edit/{group_id}")
async def serve_edit(group_id: int):
    return FileResponse(PAGES_DIR / "edit.html")

@app.get("/agendamento/add")
async def serve_create_agenda():
    return FileResponse("pages/agendamentos/add.html")

@app.get("/agendamentos/")
async def serve_create_agenda():
    return FileResponse("pages/agendamentos/index.html")


# uvicorn backend.main:app --reload