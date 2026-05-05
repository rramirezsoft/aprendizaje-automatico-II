"""
Cliente MCP minimo para validar que el servidor funciona correctamente.
Lanza el servidor por stdio, lista las tools y ejecuta cada una con
una entrada de ejemplo.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent


async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "src" / "server.py")],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=" * 60)
            print("TEST DEL SERVIDOR MCP - DesignPatterns-MCP")
            print("=" * 60)

            tools = await session.list_tools()
            print(f"\nTools disponibles: {len(tools.tools)}")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description.splitlines()[0]}")

            print("\n--- list_patterns() ---")
            r = await session.call_tool("list_patterns", {})
            print(r.content[0].text)

            print("\n--- search_patterns('clase con una unica instancia', k=2) ---")
            r = await session.call_tool(
                "search_patterns",
                {"query": "clase con una unica instancia", "k": 2},
            )
            print(r.content[0].text[:600] + "...")

            print("\n--- get_pattern('observer') ---")
            r = await session.call_tool("get_pattern", {"name": "observer"})
            print(r.content[0].text[:400] + "...")

            print("\nTodas las tools responden correctamente.")


if __name__ == "__main__":
    asyncio.run(main())
