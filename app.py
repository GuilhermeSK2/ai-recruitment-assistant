import sqlite3
from sentence_transformers import SentenceTransformer, util
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def carregar_faq_do_banco():
    conn = sqlite3.connect("recrutamento.db")
    cursor = conn.cursor()

    cursor.execute("SELECT pergunta, resposta FROM faq")
    faq_data = cursor.fetchall()

    conn.close()
    return faq_data


def gerar_embeddings(faq_data):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    perguntas = [item[0] for item in faq_data]
    respostas = [item[1] for item in faq_data]
    embeddings = model.encode(perguntas, convert_to_tensor=True)
    return model, perguntas, respostas, embeddings


def buscar_perguntas_similares(model, embeddings, pergunta_usuario, perguntas, respostas, top_k=3):
    emb_usuario = model.encode(pergunta_usuario, convert_to_tensor=True)
    similaridades = util.cos_sim(emb_usuario, embeddings)[0]

    indices_top_k = similaridades.argsort(descending=True)[:top_k]
    contexto = ""

    for idx in indices_top_k:
        contexto += f"Pergunta: {perguntas[idx]}\nResposta: {respostas[idx]}\n\n"

    return contexto.strip()


def criar_prompt_template():
    return PromptTemplate(
        input_variables=["contexto", "pergunta_usuario"],
        template="""
Você é um assistente especializado em recrutamento de talentos.
Use as perguntas e respostas abaixo como base de conhecimento para responder a pergunta do usuário de forma clara e útil.
Responda sempre em português brasileiro.
Se não encontrar a resposta na base de conhecimento, diga que não sabe a resposta.
Não cumprimente o usuário, apenas responda diretamente à pergunta.
Responda diretamente ao usuário, ele interage com você como se fosse uma conversa.

Base de conhecimento:
{contexto}

Pergunta do usuário:
{pergunta_usuario}

Resposta:"""
    )


def conversar_com_chatbot():
    faq_data = carregar_faq_do_banco()
    model_emb, perguntas, respostas, embeddings = gerar_embeddings(faq_data)

    prompt_template = criar_prompt_template()
    llm = Ollama(model="llama3:8b")  # Precisa estar rodando localmente

    chain = LLMChain(llm=llm, prompt=prompt_template)

    print("Olá! Sou o Chatbot de Recrutamento com IA. Como posso ajudar?\n")

    while True:
        pergunta_usuario = input("Você: ")
        if pergunta_usuario.lower() in ["sair", "exit", "quit"]:
            print("Chatbot: Obrigado por conversar. Até mais!")
            break

        contexto = buscar_perguntas_similares(
            model_emb, embeddings, pergunta_usuario, perguntas, respostas
        )

        resposta = chain.run(contexto=contexto, pergunta_usuario=pergunta_usuario)

        print(f"\nChatbot: {resposta}\n")


if __name__ == "__main__":
    conversar_com_chatbot()