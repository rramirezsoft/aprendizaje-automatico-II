"""
Ingesta de los documentos de patrones de diseno.
Lee los .md de la carpeta data/, los trocea en chunks, calcula embeddings
con Gemini y los almacena en ChromaDB para que el servidor MCP los pueda
consultar por similitud semantica.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "chroma_db"
COLLECTION = "design_patterns"

load_dotenv(ROOT / ".env")

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("No se encontro GOOGLE_API_KEY en el archivo .env")


def cargar_documentos():
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documentos = loader.load()
    print(f"Documentos cargados: {len(documentos)}")
    for doc in documentos:
        nombre = Path(doc.metadata["source"]).stem
        doc.metadata["pattern"] = nombre
        print(f"  - {nombre} ({len(doc.page_content)} caracteres)")
    return documentos


def dividir(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)
    print(f"Chunks generados: {len(chunks)}")
    print(f"Tamaño medio: {sum(len(c.page_content) for c in chunks) // len(chunks)} caracteres")
    return chunks


def indexar(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
        collection_name=COLLECTION,
    )
    print(f"Base vectorial creada en: {DB_DIR}")
    print(f"Vectores almacenados: {vs._collection.count()}")
    return vs


if __name__ == "__main__":
    print("=" * 60)
    print("INGESTA - Patrones de Diseno")
    print("=" * 60)

    documentos = cargar_documentos()
    chunks = dividir(documentos)
    indexar(chunks)

    print("\nIngesta completada con exito.")
