from system import system_summary
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from typing import Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from typing_extensions import Annotated, TypedDict

system_prompt = """
Eres un asistente especializado en sistemas operativos Linux, Bash scripting, programación en general, DevOps, y seguridad informática ofensiva y defensiva, así como en mejores prácticas en administración de sistemas y DevOps.

# INSTRUCCIONES CLAVE:
- Responderás todas las dudas que te presente en español, con respuesta directa.
- Toda explicación debe ser breve y directa, con un enfoque técnico.
- Si debes generar código este debe estar completamente en inglés, incluidos los nombres de variables, funciones, comandos y cualquier comentario necesario.
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
# for chunk in question_model.stream({ "messages": messages, "system_summary": system_summary.summary() }):
#     print(chunk.content, end="", flush=True)


class Options(TypedDict):
    copy: bool
    copy_code: bool


class InputState(TypedDict):
    question: str
    options: Options


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    system_summary: str


class OutputState(TypedDict):
    answer: str


def system_summary_node(state: InputState) -> State:
    return {
        "messages": [HumanMessage(content=state["question"])],
        "system_summary": system_summary.summary()
    }


def model_call_node(state: State) -> OutputState:
    answer = ''
    for chunk in question_model.stream(state):
        print(chunk.content, end="", flush=True)
        answer += chunk.content
    return {
        "answer": answer
    }

def build_agent():
    builder = StateGraph(state_schema=State, input_schema=InputState, output_schema=OutputState)
    builder.add_node("system_summary", system_summary_node)
    builder.add_node("model_call", model_call_node)
    builder.add_edge(START, "system_summary")
    builder.add_edge("system_summary", "model_call")
    builder.add_edge("model_call", END)
    return builder.compile()

graph = build_agent()
res = graph.invoke({ "question": "que sistema operativo es este?"})

print(res)