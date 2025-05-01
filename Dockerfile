FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema (git, etc)
RUN apt-get update && apt-get install -y git && apt-get clean

# Copia os arquivos para dentro do container
COPY ./src /app

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

# Define o comando padrão para rodar o app
# CMD ["python", "main.py"]
CMD ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]