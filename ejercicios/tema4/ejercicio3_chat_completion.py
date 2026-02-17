from openai import OpenAI

client = OpenAI() 

def chat(user_message: str, system_prompt: str = "Eres un asistente util.") -> str:
    """
    Envia un mensaje al modelo y retorna la respuesta.

    Args:
        user_message: Mensaje del usuario.
        system_prompt: Instrucciones del sistema.

    Returns:
        Respuesta del modelo como texto.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

class Conversation:
    """Gestiona una conversacion multi-turno con historial de mensajes."""

    def __init__(self, system_prompt: str = "Eres un asistente util."):
        self.messages = [{"role": "system", "content": system_prompt}]

    def chat(self, user_message: str) -> str:
        """
        Envia mensaje y mantiene historial.

        Args:
            user_message: Mensaje del usuario.

        Returns:
            Respuesta del modelo.
        """
        self.messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.7,
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        """Reinicia la conversacion manteniendo el system prompt."""
        self.messages = [self.messages[0]]

    def get_history_length(self) -> int:
        """Retorna el numero de mensajes en el historial."""
        return len(self.messages)

def compare_temperatures(
    prompt: str,
    temperatures: list[float] | None = None,
) -> dict[float, str]:
    """
    Compara respuestas con diferentes temperaturas.

    Args:
        prompt: Prompt a enviar al modelo.
        temperatures: Lista de temperaturas a probar.

    Returns:
        Diccionario con temperatura como clave y respuesta como valor.
    """
    if temperatures is None:
        temperatures = [0, 0.5, 1.0, 1.5]

    results = {}
    for temp in temperatures:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=150,
        )
        results[temp] = response.choices[0].message.content

    return results

def main():
    print("=" * 60)
    print("PARTE A: Chat Basico")
    print("=" * 60)

    response = chat("¿Cual es la capital de Francia?")
    print(f"Pregunta: ¿Cual es la capital de Francia?")
    print(f"Respuesta: {response}")

    print()

    response_custom = chat(
        "Explica que es una API REST en una frase",
        system_prompt="Eres un profesor de informatica. Responde de forma breve.",
    )
    print(f"Pregunta: Explica que es una API REST en una frase")
    print(f"Respuesta: {response_custom}")

    print()
    print("=" * 60)
    print("PARTE B: Conversacion Multi-turno")
    print("=" * 60)

    conv = Conversation("Eres un tutor de matematicas. Responde de forma concisa.")

    preguntas = [
        "¿Que es una derivada?",
        "Dame un ejemplo simple",
        "¿Y una integral?",
    ]

    for pregunta in preguntas:
        print(f"\nUsuario: {pregunta}")
        respuesta = conv.chat(pregunta)
        print(f"Asistente: {respuesta}")
        print(f"[Mensajes en historial: {conv.get_history_length()}]")

    print()
    print("=" * 60)
    print("PARTE C: Comparacion de Temperaturas")
    print("=" * 60)

    prompt_creativo = "Escribe un slogan creativo para una app de meditacion"
    results = compare_temperatures(prompt_creativo)

    for temp, response in results.items():
        print(f"\n--- Temperature: {temp} ---")
        print(response)

    print()
    print("=" * 60)
    print("OBSERVACIONES SOBRE LA TEMPERATURA")
    print("=" * 60)
    print("""
- Temperature 0:   Determinista, siempre la misma respuesta. Ideal para
                   tareas que requieren consistencia y precision.
- Temperature 0.5: Ligeramente creativa pero aun predecible. Buen balance
                   para la mayoria de tareas.
- Temperature 1.0: Creativa y variada. Buena para generacion de contenido,
                   brainstorming y tareas creativas.
- Temperature 1.5: Muy aleatoria, puede generar resultados incoherentes
                   o inesperados. Usar con precaucion.

Conclusion: Para tareas de produccion (chatbots, soporte), usar 0.3-0.7.
Para tareas creativas (slogans, historias), usar 0.7-1.2.
Temperaturas >1.3 rara vez son utiles en produccion.
""")


if __name__ == "__main__":
    main()
