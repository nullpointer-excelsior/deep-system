from deepsystem.system import system_summary, markdownfiles
from deepsystem.config import get_configuration
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from typing import Sequence, List
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from typing_extensions import Annotated, TypedDict
from deepsystem.persistence import create_checkpointer


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

filecontext_prompt="""
## CONTEXTO
En base al siguiente contenido:
---
{files}
---
Response la siguiente pregunta: {question}
"""

config = get_configuration()
model = config['ai']['model']['selected']

llm = init_chat_model(f"openai:{model}")

question_model = prompt_template | llm


class Options(TypedDict):
    contextfiles: List[str]
    clipboard: str


class InputState(TypedDict):
    question: str
    options: Options


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    system_summary: str


class OutputState(TypedDict):
    answer: str


def input_node(state: InputState) -> State:
    contextfiles = state["options"]["contextfiles"]
    clipboard = state["options"]["clipboard"]
    if clipboard:
        contextfiles.append(f"\n{clipboard}\n")

    if contextfiles:
        markdown_files = markdownfiles(contextfiles)
        content = filecontext_prompt.format(files=markdown_files, question=state["question"])
    else:
        content = state["question"]

    return {
        "messages": [HumanMessage(content=content)],
        "system_summary": system_summary.summary()
    }


def model_call_node(state: State) -> State:
    answer = question_model.invoke(state).content
    return {
        "messages": AIMessage(content=answer)
    }


def output_node(state: State) -> OutputState:
    return {
        "answer": state["messages"][-1].content   
    }


checkpointer = create_checkpointer()
builder = StateGraph(state_schema=State, input_schema=InputState, output_schema=OutputState)

builder.add_node("input", input_node)
builder.add_node("model_call", model_call_node)
builder.add_node("output", output_node)
builder.add_edge(START, "input")
builder.add_edge("input", "model_call")
builder.add_edge("model_call", "output")
builder.add_edge("output", END)

graph = builder.compile(checkpointer=checkpointer)


def invoke(question, **kwargs):

    config = {
        "configurable": {
            "thread_id": system_summary.cwd 
        }
    }
    input: InputState = { 
        "question": question,
        "options": {
            "contextfiles": kwargs.get("contextfiles", []),
            "clipboard": kwargs.get("clipboard", None)
        }
    }
    return graph.invoke(input, config)
