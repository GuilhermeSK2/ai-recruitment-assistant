# Chatbot de Recrutamento com IA (RAG)

Este projeto implementa um chatbot de recrutamento de talentos utilizando a arquitetura RAG (Retrieval-Augmented Generation). O chatbot é capaz de responder a perguntas sobre recrutamento de forma clara e útil, buscando informações em uma base de conhecimento (FAQ) armazenada em um banco de dados SQLite e utilizando um Large Language Model (LLM) local (Llama3, via Ollama) para gerar as respostas.

## Visão Geral

A arquitetura RAG é ideal para criar chatbots que precisam de conhecimento específico e atualizado, indo além do que foi aprendido durante o treinamento do LLM. Neste projeto, o fluxo de trabalho é o seguinte:

1.  **Base de Conhecimento (FAQ):** Perguntas e respostas frequentes sobre recrutamento são armazenadas em um banco de dados SQLite.
2.  **Geração de Embeddings:** As perguntas da FAQ são convertidas em vetores numéricos (embeddings) usando um modelo de Sentence Transformer (`all-MiniLM-L6-v2`).
3.  **Busca de Similaridade:** Quando o usuário faz uma pergunta, o chatbot busca as perguntas mais semanticamente similares na FAQ usando os embeddings.
4.  **Criação de Contexto:** As perguntas e respostas similares encontradas são reunidas para formar um "contexto" relevante.
5.  **Geração de Resposta (LLM):** O contexto relevante e a pergunta do usuário são enviados a um LLM (Llama3:8b, executando localmente via Ollama). O LLM é instruído a usar esse contexto para formular uma resposta clara e direta.
6.  **Resposta ao Usuário:** O chatbot exibe a resposta gerada. Se a informação não estiver na base de conhecimento, o chatbot informará que não sabe a resposta.

Este projeto é uma solução eficaz para automatizar o suporte a candidatos ou gerentes de contratação com perguntas comuns.

## Estrutura do Projeto

* `app.py`: O script Python principal que contém toda a lógica do chatbot.
* `recrutamento.db`: O banco de dados SQLite que armazena a base de conhecimento FAQ.

## Tecnologias Utilizadas

* **Python 3**
* **`sqlite3`**: Módulo embutido para interação com o banco de dados SQLite.
* **`sentence-transformers`**: Para gerar embeddings de sentenças.
* **`langchain`**: Framework para orquestrar LLMs e criar cadeias de processamento.
    * `langchain.llms.Ollama`: Conector para LLMs executados via Ollama.
    * `langchain.prompts.PromptTemplate`: Para definir a estrutura do prompt.
    * `langchain.chains.LLMChain`: Para encadear o LLM com o prompt.
* **Ollama**: Plataforma para executar LLMs localmente.
* **Llama3:8b**: Modelo de linguagem grande da Meta (você pode usar outro modelo Llama3 se preferir).


## Interagindo com o Chatbot

Ao executar `app.py`, você verá uma mensagem de boas-vindas. Você pode digitar suas perguntas sobre recrutamento.

**Exemplos de perguntas para testar:**

* `Como me candidato?`
* `Quais os requisitos para Desenvolvedor Python?`
* `Como funciona o processo de seleção?`
* `Vocês aceitam trabalho remoto?`
* `Quanto tempo para o feedback?`
* `Quais os benefícios?`
* `Posso me candidatar a várias vagas?`
* `Existem chances de crescer na carreira?`
* `Qual a capital do Brasil?` (para testar quando a resposta não está na base de conhecimento)

Para encerrar a conversa, digite `sair`, `exit` ou `quit`.

## Exemplo de interação:

<img width="882" height="125" alt="Image" src="https://github.com/user-attachments/assets/71ad3d85-389c-47f0-97d9-c850070bc8f1" />

