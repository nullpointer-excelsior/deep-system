import click
from deepsystem.question import invoke as invoke_question
from deepsystem.config import update_ai_model, get_configuration
from deepsystem.sessions import clean_current_session
from deepsystem.history import select_code_snippet
from deepsystem import ui
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()
configuration = get_configuration()

def display_markdown(content):
    print('')
    console.print(Markdown(content))
    print('')

def display_code(code):
    syntax = Syntax(code, "python", theme="monokai", line_numbers=False)
    print('')
    console.print(syntax)
    print('')


@click.command(help='Make a question with session based on the current working directory')
@click.argument('question', required=False)
@click.option("-f", "--file", "files", type=click.Path(dir_okay=False), multiple=True, help="File to add to the context agent")
@click.option("-s", "--select-file", "selectfile", is_flag=True, help="Select a file with fzf to ask a question about this file")
def question(question, files, selectfile):
    
    contextfiles = [f for f in files]
    
    if selectfile and (fileselected := ui.select_files()):
        contextfiles.append(fileselected)

    if not question:
        question = click.prompt(click.style("💬 Enter your question", fg="yellow"), type=str)

    model = configuration['ai']['model']['selected']    

    with console.status(f"[bold green] 🦜 Thinking and hallucinating with {model}...[/]", spinner="dots"):
        response = invoke_question(question, contextfiles=contextfiles)
    
    display_markdown(response["answer"])


@click.command(help='Select code snippet from agent chat history')
def code_history():
    code = select_code_snippet()
    if code is not None:
        display_code(code)


@click.command(help='Clean chat session of the current working directory')
def clean():
    clean_current_session()  
    console.print("🧹 [bold green]Session cleaned [/bold green]")


@click.command(help='Update model based on configured choices')
def model():
    if update_ai_model():
        console.print("🚀 [bold green]Model updated [/bold green]")