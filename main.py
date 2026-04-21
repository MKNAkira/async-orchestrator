from fastapi import FastAPI
from tasks import process_heavy_data
from celery.result import AsyncResult

app = FastAPI(title="Async Orchestrator API")

@app.get("/")
def read_root():
    return {"message": "Orquestrador Online", "status": "ready"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- NOVA ROTA ASSÍNCRONA ---
@app.post("/processar/{dados}")
def iniciar_processamento(dados: str):
    """
    Recebe o dado do usuário e envia para a fila do Celery.
    Responde instantaneamente sem deixar o usuário esperando.
    """
    # O .delay() é a mágica do Celery. Ele não roda a função aqui, ele manda pro Redis!
    tarefa = process_heavy_data.delay(dados)
    
    return {
        "message": "Processamento enviado para a fila com sucesso!",
        "task_id": tarefa.id
    }

@app.get("/status/{task_id}")
def verificar_status(task_id: str):
    """
    O usuário envia o ID que recebeu e nós perguntamos ao Celery (via Redis)
    qual é o status atual da tarefa.
    """
    # Cria uma referência à tarefa baseada no ID
    tarefa = AsyncResult(task_id, app=process_heavy_data.app)
    
    # Monta a resposta
    resposta = {
        "task_id": task_id,
        "status": tarefa.state, # Pode ser PENDING, STARTED, SUCCESS, FAILURE...
        "resultado": tarefa.result if tarefa.ready() else "Ainda processando..."
    }
    
    return resposta    