import time
from celery import Celery

# Configura o Celery para usar o Redis como "Broker" (Fila) e "Backend" (Guarda Resultados)
# "redis://redis:6379/0" -> O primeiro 'redis' é o nome do container que vamos criar no Docker
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_heavy_data(data: str):
    """
    Simula uma tarefa pesada de 15 segundos (como ler um PDF longo ou fazer uma requisição externa).
    """
    print(f"[{data}] Iniciando processamento pesado...")
    time.sleep(15) 
    print(f"[{data}] Processamento concluído!")
    return {"status": "sucesso", "resultado_gerado": f"Dados processados: {data}"}