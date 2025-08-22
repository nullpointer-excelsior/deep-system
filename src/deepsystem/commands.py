import click
from deepsystem.question import invoke as invoke_question
from deepsystem.config import update_ai_model, get_configuration
from deepsystem import sessions
from deepsystem.history import select_code_snippet
from deepsystem import ui
import pyperclip 
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
@click.option("-s", "--select-file", "selectfile", count=True, help="Select a file with fzf to ask a question about this file. you can pass a multiple files using the short option repeatedly eg: '-sss' select 3 files") # TODO: Using the count option might enable selecting multiple files
@click.option("-c", "--from-clipboard", "fromclipboard", is_flag=True, help="Add clipboard content to question.")
def question(question, selectfile, fromclipboard):
    
    contextfiles = []

    for _ in range(selectfile):
        if fileselected := ui.select_files():
            contextfiles.append(fileselected)

    if contextfiles:
        console.print("\n[bold]📝 Context files added:[/]")
        console.print("\n".join(f"[grey42]- {f}[/]" for f in contextfiles))

    clipboard_content = pyperclip.paste() if fromclipboard else None

    if not question:
        question = click.prompt(click.style("\n💬 Enter your question", fg="yellow"), type=str)

    model = configuration['ai']['model']['selected']    

    with console.status(f"[bold green] 🦜 Thinking and hallucinating with {model}...[/]", spinner="dots"):
        response = invoke_question(question, contextfiles=contextfiles, clipboard=clipboard_content)
    
    display_markdown(response["answer"])


@click.command(help='Select code snippet from agent chat history')
def code_history():
    if code := select_code_snippet():
        display_code(code)
    else:
        console.print("🚫 Snippets not found")


@click.command(help='Clean chat session of the current working directory')
def clean():
    sessions.clean_current_session()  
    console.print("🧹 [bold green]Session cleaned [/bold green]")


@click.command(help='Update model based on configured choices')
def model():
    if update_ai_model():
        console.print("🚀 [bold green]Model updated [/bold green]")