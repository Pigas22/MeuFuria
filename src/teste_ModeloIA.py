import ollama as ol

def pergunta(pergunta: str):
    stream = ol.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": pergunta},],
        stream=True
    )

    for chunk in stream:
        print(chunk["message"]["content"], end='', flush=True)

pergunta('Você conhece o time de e-sports FURIA?')