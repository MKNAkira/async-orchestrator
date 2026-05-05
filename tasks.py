import os
import time
import logging
from celery import Celery

# Configuração profissional de Logs (Substitui os "prints" simples)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Puxa a URL do Redis de forma segura do arquivo .env (O Recrutador ama isso)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# bind=True permite acessar o "self" da tarefa
# max_retries=3 faz o Celery tentar de novo se der erro, garantindo resiliência
@celery_app.task(bind=True, max_retries=3)
def process_heavy_data(self, payload: dict):
    # Agora recebemos um dicionário, não mais uma string
    codigo = payload.get('codigo_rastreio', 'Desconhecido')
    
    try:
        logger.info(f"[{codigo}] 📦 Iniciando processamento do manifesto...")
        
        # Simula o trabalho pesado (15 segundos)
        time.sleep(15) 
        
        logger.info(f"[{codigo}] ✅ Processamento concluído com sucesso!")
        return {
            "status": "sucesso", 
            "codigo_processado": codigo,
            "detalhes": "Manifesto validado e inserido no sistema"
        }
        
    except Exception as exc:
        logger.error(f"[{codigo}] ❌ Erro ao processar: {exc}. Tentando novamente em 60s...")
        raise self.retry(exc=exc, countdown=60)