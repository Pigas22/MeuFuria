import time
import requests
import streamlit as st
import os
from backend.__init__ import LINK_API_BASE, LINK_API_CHAT, MODELO, STREAM, TEMPLATE
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import SystemMessage



from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Criação do modelo (chat-model)
llm = ChatOllama(model=MODELO, temperature=0.1, base_url=LINK_API_BASE)

# Template que aceita histórico de mensagens + nova input
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=TEMPLATE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# Pipeline de execução
chain = prompt | llm

# Histórico (poderia ser armazenado em session_state)
chat_history = []

# Input do usuário
entrada_usuario = "Qual a sua função aqui?"

# Executa com histórico
resposta = chain.invoke({
    "input": entrada_usuario,
    "chat_history": chat_history
})

# Salva a interação no histórico
chat_history.append(HumanMessage(content=entrada_usuario))
chat_history.append(AIMessage(content=resposta.content))

st.write(resposta.content)



CAMINHO_PASTA_LOGO = os.path.abspath(os.path.join("data", "furiagg", "logo"))
FURIA_LOGO = "Furia_Esports_logo.png"
FURIA_BOT_LOGO = "Furia_Bot_logo.png"
SLOGAN_SITE = "MeuFuria - Maior Fansite da FURIA"


@st.cache_data
def espera_modelo_disponivel(mensagens, modelo="gemma3:1b"):
    while True:
        try:
            res = requests.post(LINK_API_CHAT, json={
                "model": modelo,
                "messages": mensagens,
                "stream": STREAM
            })
            if res.status_code == 200 and "error" not in res.json():
                return res
            
            print("Modelo ainda não disponível... tentando de novo.")
        except:
            pass
        time.sleep(15)


# Inicializa o chat com o Bot
if "messages" not in  st.session_state:
    res = requests.post(LINK_API_CHAT, json={
        "model": MODELO,
        "messages": TEMPLATE,
        "stream": STREAM,
        "temperatura": 0.1
    })

    st.session_state.messages = [
        {
            "role": "system",
            "content": TEMPLATE
        }
    ]

    print(res)


# TELA WEB
st.set_page_config(
    page_title= SLOGAN_SITE,
    page_icon= CAMINHO_PASTA_LOGO + os.sep + FURIA_LOGO,
    layout="wide"
)

with st.sidebar:
    st.image(CAMINHO_PASTA_LOGO + os.sep + FURIA_BOT_LOGO, width=100)

    st.header(SLOGAN_SITE, divider=True)
    
    reiniciar = st.button("🔃 Novo Chat")


st.title("Pergunte ao MeuFuria-Bot")

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

mensagem_usuario = st.chat_input("Digite o que estiver pensando... ")

if reiniciar:
    st.session_state.messages = [
        {"role": "system", "content": TEMPLATE}
    ]
    st.rerun()


if mensagem_usuario:
    st.session_state.messages.append({
        "role": "user",
        "content": mensagem_usuario
    })

    with st.chat_message("user"):
        st.markdown(mensagem_usuario)

    with st.spinner("Consultando modelo..."):
        response = espera_modelo_disponivel(st.session_state.messages)

        resposta_json = response.json()
        resposta_modelo = resposta_json.get("message", {}).get("content", "[Erro ao obter a resposta do modelo, tente novamente mais tarde...]")

        st.session_state.messages.append({
            "role": "assistant",
            "content": resposta_modelo
        })

        with st.chat_message("assistant"):
            st.markdown(resposta_modelo)

        st.divider()
        st.title("For DEV's:")
        st.write(response.json())
