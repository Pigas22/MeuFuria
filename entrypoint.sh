#!/bin/bash
# Inicia o servidor Ollama em segundo plano
ollama serve &

# Aguarda o servidor subir
sleep 5

# puxando o modelo
ollama pull gemma3:1b

wait
