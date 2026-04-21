# 1. Usamos uma versão leve (slim) do Python 3.11
FROM python:3.11-slim

# 2. Definimos onde o código vai morar dentro do "computador virtual" (container)
WORKDIR /app

# 3. Copiamos a sua lista de dependências para dentro
COPY requirements.txt .

# 4. Mandamos instalar tudo o que está na lista
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo o seu código para dentro do container
COPY . .

# 6. Avisamos que a porta 8000 vai ser usada
EXPOSE 8000

# 7. O comando que liga o servidor assim que o container subir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]