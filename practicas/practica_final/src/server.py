"""
Servidor MCP "DesignPatterns-MCP".

Expone una base de conocimiento RAG sobre patrones de diseno como
herramientas consultables desde cualquier cliente MCP (por ejemplo,
Claude Desktop). Internamente usa ChromaDB y embeddings de Gemini.

Tools expuestas:
- search_patterns(query, k): busqueda semantica en la base RAG
- list_patterns(): lista los patrones disponibles
- get_pattern(name): devuelve el documento completo de un patron concreto

Transporte: stdio (estandar de MCP).
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "chroma_db"
COLLECTION = "design_patterns"

load_dotenv(ROOT / ".env")

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("Falta GOOGLE_API_KEY en .env")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
    collection_name=COLLECTION,
)

mcp = FastMCP("DesignPatterns-MCP")


@mcp.tool()
def search_patterns(query: str, k: int = 3) -> str:
    """Busca en la base de conocimiento de patrones de diseno los fragmentos
    mas relevantes para la consulta dada. Usa busqueda semantica con embeddings.

    Args:
        query: Pregunta o descripcion del problema en lenguaje natural.
        k: Numero de fragmentos a devolver (por defecto 3).

    Returns:
        Texto con los fragmentos recuperados y su patron de origen.
    """
    docs = vectorstore.similarity_search(query, k=k)
    if not docs:
        return "No se encontraron resultados relevantes."
    bloques = []
    for i, d in enumerate(docs, 1):
        patron = d.metadata.get("pattern", "desconocido")
        bloques.append(f"[Resultado {i} - Patron: {patron}]\n{d.page_content}")
    return "\n\n---\n\n".join(bloques)


@mcp.tool()
def list_patterns() -> str:
    """Lista todos los patrones de diseno disponibles en la base de conocimiento.

    Returns:
        Lista en formato texto con el nombre de cada patron indexado.
    """
    archivos = sorted(p.stem for p in DATA_DIR.glob("*.md"))
    if not archivos:
        return "No hay patrones indexados."
    return "Patrones disponibles:\n" + "\n".join(f"- {a}" for a in archivos)


@mcp.tool()
def get_pattern(name: str) -> str:
    """Devuelve el documento completo de un patron concreto.

    Args:
        name: Nombre del patron en minusculas (singleton, factory, observer,
              strategy, decorator, mvc, adapter).

    Returns:
        Contenido completo del fichero markdown del patron, o un mensaje de
        error si no existe.
    """
    archivo = DATA_DIR / f"{name.lower()}.md"
    if not archivo.exists():
        disponibles = ", ".join(p.stem for p in sorted(DATA_DIR.glob("*.md")))
        return f"Patron '{name}' no encontrado. Disponibles: {disponibles}"
    return archivo.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
