from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from celery.result import AsyncResult
from tasks import process_heavy_data, celery_app

app = FastAPI(
    title="GlobalLog Async Orchestrator",
    description="API robusta para processamento assíncrono de manifestos logísticos.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOVO: Sub-modelo simulando as linhas de uma planilha densa
class ItemEstoque(BaseModel):
    prato: str
    lote: str
    quantidade: int

class ManifestoPayload(BaseModel):
    codigo_rastreio: str = Field(..., description="Código único da carga", min_length=5)
    motorista: str = Field(...)
    filial_origem: str = Field(default="SPO-01")
    # NOVO: Lista que pode receber milhares de itens
    itens: list[ItemEstoque] = []

@app.get("/")
def read_root():
    return {"message": "Orquestrador Online", "status": "ready"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/processar/", status_code=202)
def iniciar_processamento(payload: ManifestoPayload):
    # O payload agora pode ter dezenas de megabytes
    tarefa = process_heavy_data.delay(payload.model_dump())
    
    return {
        "message": "Manifesto recebido e enviado para a fila de processamento.",
        "task_id": tarefa.id
    }

@app.get("/status/{task_id}")
def verificar_status(task_id: str):
    tarefa = AsyncResult(task_id, app=celery_app)
    
    return {
        "task_id": task_id,
        "status": tarefa.state,
        "resultado": tarefa.result if tarefa.ready() else "Aguardando operário (Worker)..."
    }