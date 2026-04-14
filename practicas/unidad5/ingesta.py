"""
Ingesta de documentos para el sistema RAG.
Carga documentos, los divide en chunks y los almacena en ChromaDB
usando embeddings de Google Gemini.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("No se encontro GOOGLE_API_KEY en el archivo .env")


def cargar_documentos(ruta_documentos: str):
    loader = DirectoryLoader(
        ruta_documentos,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documentos = loader.load()
    print(f"Documentos cargados: {len(documentos)}")
    for doc in documentos:
        print(f"  - {doc.metadata['source']} ({len(doc.page_content)} caracteres)")
    return documentos


def dividir_documentos(documentos):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"Chunks generados: {len(chunks)}")
    tam_medio = sum(len(c.page_content) for c in chunks) // len(chunks)
    print(f"Tamaño medio de chunk: {tam_medio} caracteres")
    return chunks


def crear_base_vectorial(chunks, ruta_db: str = "./chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=ruta_db,
        collection_name="empresa_docs",
    )

    print(f"Base vectorial creada en: {ruta_db}")
    print(f"Vectores almacenados: {vectorstore._collection.count()}")
    return vectorstore


if __name__ == "__main__":
    print("=" * 50)
    print("INGESTA DE DOCUMENTOS - Sistema RAG TechCorp")
    print("=" * 50)

    documentos = cargar_documentos("./documentos")
    chunks = dividir_documentos(documentos)

    print("\nEjemplo de chunk:")
    print(f"  Contenido: {chunks[0].page_content[:150]}...")
    print(f"  Metadata: {chunks[0].metadata}")

    vectorstore = crear_base_vectorial(chunks)

    print("\nIngesta completada con exito.")
