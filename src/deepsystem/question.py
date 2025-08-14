from system import SystemSummary, system_summary
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model


system_prompt = """
Eres un asistente especializado en sistemas operativos Linux, Bash scripting, programación en general, DevOps, y seguridad informática ofensiva y defensiva, así como en mejores prácticas en administración de sistemas y DevOps.

# INSTRUCCIONES CLAVE:
- Responderás todas las dudas que te presente en español, con respuesta directa.
- Toda explicación debe ser breve y directa, con un enfoque técnico.
- El código debe estar completamente en inglés, incluidos los nombres de variables, funciones y cualquier comentario necesario.
- Incluye comentarios solo cuando sea estrictamente necesario para mejorar la claridad, siempre en inglés.

# CONTEXTO
Tienes disponible la siguiente información del sistema para incluir en tus respuestas solo cuando sea necesario:
{system_summary}

"""

prompt_template = ChatPromptTemplate([
    ("system", system_prompt),
    MessagesPlaceholder("messages")
])


llm = init_chat_model("gpt-4.1-nano-2025-04-14", model_provider="openai")
question_model = prompt_template | llm

messages = [
    HumanMessage(content="como instalo bat")
]
for chunk in question_model.stream({ "messages": messages, "system_summary": system_summary.summary() }):
    print(chunk.content, end="", flush=True)
