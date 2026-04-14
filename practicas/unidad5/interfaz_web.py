"""
Interfaz web con Gradio para el asistente RAG TechCorp (bonificacion).
Ejecuta: python interfaz_web.py
"""

import gradio as gr
from asistente import cargar_base_vectorial, crear_cadena_rag

vectorstore = cargar_base_vectorial()
cadena, retriever = crear_cadena_rag(vectorstore)


def responder(mensaje, historial):
    return cadena.invoke(mensaje)


demo = gr.ChatInterface(
    fn=responder,
    title="Asistente RAG - TechCorp",
    description=(
        "Consulta la documentacion interna de la empresa "
        "(politicas de RRHH, procedimientos de soporte tecnico, etc.)"
    ),
    examples=[
        "¿Cuantos dias de vacaciones tengo al año?",
        "¿Cual es el procedimiento para reportar una incidencia tecnica?",
        "¿Cada cuanto tiempo debo cambiar mi contraseña?",
    ],
)


if __name__ == "__main__":
    demo.launch()
