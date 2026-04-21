# Async Task Orchestrator

Uma API RESTful focada em resolver um problema clássico da engenharia de software: gargalos de processamento síncrono.

Construí este projeto para demonstrar como receber requisições pesadas (como extração de dados, geração de relatórios ou processamento de arquivos), devolver uma resposta instantânea ao usuário e realizar todo o trabalho pesado em background.

# O Problema vs. A Solução

O Problema: Se uma API tenta processar um arquivo de 500 páginas no exato momento em que o usuário faz a requisição, a conexão HTTP fica "presa". Se 100 usuários fizerem isso ao mesmo tempo, o servidor esgota suas conexões, a memória vai a 100% e a aplicação cai (Timeout/Erro 504).

A Solução (Este Projeto):
Adotei uma arquitetura baseada em mensageria (Message-Driven).

O usuário envia o dado.

A API não processa nada na hora. Ela anota o pedido, joga numa fila ultrarrápida e devolve um "recibo" (task_id) para o usuário instantaneamente.

Trabalhadores isolados (workers) puxam essas tarefas da fila no ritmo que a CPU aguenta, sem nunca derrubar o servidor web.

O usuário usa o task_id para consultar se a tarefa já terminou.

# Por que escolhi essa Stack? (Decisões de Engenharia)

Cada ferramenta aqui foi escolhida com um propósito específico para garantir escalabilidade:

FastAPI (O Balcão de Atendimento): Por que não Flask ou Django? O FastAPI é moderno, assíncrono por natureza e extremamente rápido. O maior trunfo dele é usar o Pydantic por baixo dos panos, o que valida qualquer payload de entrada de forma estrita antes mesmo de bater na minha regra de negócio. Além disso, ele gera o Swagger sozinho.

Celery (O Operário de Força Bruta): Por que não usar apenas asyncio nativo do Python? Porque o asyncio roda na mesma máquina da API. Se a máquina reiniciar, perco as tarefas. O Celery é padrão de mercado para background tasks distribuídas. Se der erro, ele faz retry automático. Se a demanda subir, posso simplesmente subir mais 10 containers de Celery (escalabilidade horizontal) e a API nem percebe.

Redis (O Correio / Broker): O Celery precisa de um lugar muito rápido para buscar as tarefas. O Redis roda em memória RAM, o que faz dele o message broker perfeito (e super leve) para gerenciar essa fila e também para guardar o status temporário ("Pendente", "Sucesso") dos resultados.

Docker & Docker Compose (A Infraestrutura): O clássico "na minha máquina funciona" não serve para produção. Com o Docker Compose, eu garanto que o servidor web, o banco de dados em memória e o worker subam perfeitamente integrados em qualquer sistema operacional com apenas um comando.

# Como rodar o projeto na sua máquina

Esqueça a configuração manual de ambientes virtuais do Python. Você só precisa ter o Docker e o Docker Compose instalados.

Clone este repositório:

git clone [https://github.com/SEU_USUARIO/async-orchestrator.git](https://github.com/MKNAkira/async-orchestrator.git)
cd async-orchestrator


Suba a infraestrutura completa (API, Redis e Celery Worker):

docker compose up --build -d


(A flag -d deixa rodando em background para seu terminal não ficar preso).

Acesse a documentação interativa (Swagger) e faça seus testes:
👉 https://www.google.com/search?q=http://127.0.0.1:8000/docs

📡 Endpoints (Como usar)

POST /processar/{dados}: Envie um dado. A API vai simular um processamento de 15 segundos e retornar imediatamente um HTTP 200 com o seu task_id.

GET /status/{task_id}: Cole o task_id aqui. A API vai te dizer se está "PENDING" (Ainda processando) ou "SUCCESS" (com o resultado final gerado pelo worker).