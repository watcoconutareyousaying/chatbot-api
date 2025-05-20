from app.services.helpers import download_huggingface_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from app.services.llms.deepseek import DeepSeekChat
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from app.services.prompt import system_prompt
from app.core.config import get_env_var
import os


def rag_chain():
    try:
        embeddings = download_huggingface_embeddings()

        docsearch = PineconeVectorStore.from_existing_index(
            index_name="dental-chatbot",
            embedding=embeddings,
        )

        retriever = docsearch.as_retriever(
            search_type="similarity", search_kwargs={"k": 3})

        # Dynamically select LLM provider
        llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if llm_provider == "deepseek":
            print("Using DeepSeek LLM")
            llm = DeepSeekChat(api_key=get_env_var(
                "DEEPSEEK_API_KEY"))  # type: ignore
        elif llm_provider == "openai":
            print("Using OpenAI LLM")
            llm = OpenAI(temperature=0.4, max_tokens=500)
        elif llm_provider == "ollama":
            print("Using ollama LLM")
            llm = ChatOllama(model="llama3.2", temperature=0.4, model_kwargs={"num_predict": 1024})  # type: ignore
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        return rag_chain

    except Exception as e:
        print(f"[RAG Init Error] {e}")
        raise
