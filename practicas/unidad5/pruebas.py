"""
Script auxiliar para ejecutar las 5 consultas de prueba y guardar
los resultados (respuestas + documentos recuperados) en un archivo.
"""

import os
import time
from asistente import cargar_base_vectorial, crear_cadena_rag

PREGUNTAS = [
    "Cuantos dias de vacaciones tengo al año?",
    "Cual es el procedimiento para reportar una incidencia tecnica?",
    "Puedo trabajar desde casa todos los dias de la semana?",
    "Cual es el menu del comedor de la empresa?",
    "Cada cuanto tiempo debo cambiar mi contraseña?",
]


def main():
    vectorstore = cargar_base_vectorial()
    cadena, retriever = crear_cadena_rag(vectorstore)

    resultados = []
    for i, pregunta in enumerate(PREGUNTAS, 1):
        print("\n" + "=" * 70)
        print(f"CONSULTA {i}: {pregunta}")
        print("=" * 70)

        t0 = time.time()
        docs = retriever.invoke(pregunta)
        respuesta = cadena.invoke(pregunta)
        dt = time.time() - t0

        print(f"\n[Documentos recuperados: {len(docs)}]")
        for j, d in enumerate(docs, 1):
            fuente = os.path.basename(d.metadata.get("source", "?"))
            print(f"  {j}. {fuente} | {d.page_content[:90]}...")

        print(f"\nRespuesta:\n{respuesta}")
        print(f"\nTiempo: {dt:.2f}s")

        resultados.append({
            "pregunta": pregunta,
            "docs": [
                {
                    "fuente": os.path.basename(d.metadata.get("source", "?")),
                    "contenido": d.page_content,
                }
                for d in docs
            ],
            "respuesta": respuesta,
            "tiempo": dt,
        })

    with open("resultados_pruebas.txt", "w", encoding="utf-8") as f:
        for i, r in enumerate(resultados, 1):
            f.write(f"{'=' * 70}\n")
            f.write(f"CONSULTA {i}: {r['pregunta']}\n")
            f.write(f"{'=' * 70}\n\n")
            f.write(f"Documentos recuperados: {len(r['docs'])}\n")
            for j, d in enumerate(r["docs"], 1):
                f.write(f"\n  [{j}] {d['fuente']}\n")
                f.write(f"      {d['contenido']}\n")
            f.write(f"\nRespuesta:\n{r['respuesta']}\n")
            f.write(f"\nTiempo: {r['tiempo']:.2f}s\n\n")

    print("\n\nResultados guardados en resultados_pruebas.txt")


if __name__ == "__main__":
    main()
