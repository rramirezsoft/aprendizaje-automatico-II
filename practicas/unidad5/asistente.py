"""
Asistente RAG para documentacion de empresa TechCorp.
Recupera informacion relevante de ChromaDB y genera respuestas
contextualizadas con Google Gemini.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


def cargar_base_vectorial(ruta_db: str = "./chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory=ruta_db,
        embedding_function=embeddings,
        collection_name="empresa_docs",
    )
    print(f"Base vectorial cargada: {vectorstore._collection.count()} vectores")
    return vectorstore


def crear_cadena_rag(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3,
    )

    template = ChatPromptTemplate.from_messages([
        ("system", """Eres el asistente virtual de TechCorp, especializado en responder
preguntas sobre la documentacion interna de la empresa.

INSTRUCCIONES:
- Responde SOLO con informacion que este en el contexto proporcionado.
- Si la informacion no esta en el contexto, responde exactamente: "No dispongo de informacion sobre ese tema en la documentacion de la empresa. Te recomiendo contactar con el departamento correspondiente."
- NO inventes politicas, procedimientos ni datos.
- Se claro, conciso y profesional.
- Cuando sea posible, indica de que documento proviene la informacion.

CONTEXTO DE DOCUMENTOS INTERNOS:
{context}"""),
        ("human", "{question}"),
    ])

    def formatear_docs(docs):
        return "\n\n---\n\n".join(
            f"[Fuente: {os.path.basename(doc.metadata.get('source', 'desconocida'))}]\n{doc.page_content}"
            for doc in docs
        )

    cadena = (
        {
            "context": retriever | formatear_docs,
            "question": RunnablePassthrough(),
        }
        | template
        | llm
        | StrOutputParser()
    )

    return cadena, retriever


def main():
    print("=" * 50)
    print("ASISTENTE RAG - TechCorp")
    print("=" * 50)
    print("Escribe tu pregunta sobre la documentacion de la empresa.")
    print("Escribe 'salir' para terminar.\n")

    vectorstore = cargar_base_vectorial()
    cadena, retriever = crear_cadena_rag(vectorstore)

    while True:
        pregunta = input("\nTu: ").strip()

        if pregunta.lower() in ["salir", "exit", "quit", "q"]:
            print("\nHasta luego.")
            break

        if not pregunta:
            print("Por favor, escribe una pregunta.")
            continue

        try:
            docs_recuperados = retriever.invoke(pregunta)
            print(f"\n[Documentos recuperados: {len(docs_recuperados)}]")
            for i, doc in enumerate(docs_recuperados, 1):
                fuente = os.path.basename(doc.metadata.get("source", "desconocida"))
                print(f"  {i}. {fuente} - {doc.page_content[:80]}...")

            respuesta = cadena.invoke(pregunta)
            print(f"\nAsistente: {respuesta}")

        except Exception as e:
            print(f"\nError al procesar la pregunta: {e}")


if __name__ == "__main__":
    main()
