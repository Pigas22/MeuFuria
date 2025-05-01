import time
import requests
import streamlit as st

def espera_modelo_disponivel(prompt, modelo="gemma3:1b"):
    while True:
        try:
            res = requests.post("http://ollama:11434/api/generate", json={
                "model": modelo,
                "prompt": prompt,
                "stream": False
            })
            if res.status_code == 200 and "error" not in res.json():
                return res
            
            print("Modelo ainda não disponível... tentando de novo.")
        except:
            pass
        time.sleep(15)


# TELA WEB
st.title("Chat com LLM via Ollama")

prompt = st.text_input("Digite sua pergunta: ")
if prompt:
    with st.spinner("Consultando modelo..."):
        response = espera_modelo_disponivel(prompt)

        st.write(response.json()["response"])
        
