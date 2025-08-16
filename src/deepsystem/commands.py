import click
from deepsystem.question import invoke as invoke_question
from deepsystem.config import update_ai_model, get_configuration
from deepsystem.sessions import clean_current_session
from rich.console import Console
from rich.markdown import Markdown

console = Console()
configuration = get_configuration()

def display_markdown(content):
    print('')
    console.print(Markdown(content))
    print('')

@click.command(help='Make a question with session based on the current working directory')
@click.argument('question', required=False)
def question(question):

    if not question:
        question = click.prompt(click.style("💬 Enter your question", fg="yellow"), type=str)

    model = configuration['ai']['model']['selected']    

    with console.status(f"[bold green] 🦜 Thinking and hallucinating with {model}...[/]", spinner="dots"):
        response = invoke_question(question)
    
    display_markdown(response["answer"])


@click.command(help='Select code snippet from agent chat history')
@click.option('-c', '--copy', help='Copy to clipboard the select code snippet ')
def code_history(copy):
    pass

@click.command(help='Clean chat session of the current working directory')
def clean():
    clean_current_session()  
    console.print("🧹 [bold green]Session cleaned [/bold green]")  


@click.command(help='Update model based on configured choices')
def model():
    update_ai_model()
    console.print("🚀 [bold green]Model updated [/bold green]")