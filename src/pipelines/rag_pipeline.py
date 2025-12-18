from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.vectorstore.hybrid_vector_store import HybridVectorStore

# Prompt para a parte geracional do retrieval
prompt_rag = ChatPromptTemplate.from_template(
    """
    Você é um ACP - um Agente Conversacional Pedagógico especializado em ajudar estudantes com dúvidas relacionadas a conteúdos acadêmicos.
    Sua função é fornecer respostas claras e informativas com base no material de estudo fornecido pelo contexto.
    Inclua todas as informações relevantes do contexto em suas respostas, evitando suposições ou informações externas.
    Suas respostas devem ser sempre em português brasileiro e devem usar um tom leve.

    Se não encontrar a resposta no contexto, diga:
    "Nenhuma informação disponível no contexto."
                
    Contexto:
    {context}

    Pergunta:
    {question}
    """
)


def rag_pipeline(store: HybridVectorStore, question: str,  model:str, prompt: str = prompt_rag):

    docs = store.hybrid_search(question, top_k=5)
    context = "\n\n".join([d[1] for d in docs])

    llm = OllamaLLM(model=model, temperature=0)

    chain = (
            prompt
            | llm
            | StrOutputParser()
        )
    
    return chain.invoke({"context": context, "question": question})