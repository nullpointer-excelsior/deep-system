import click
from question import invoke as invoke_question
from sessions import clean_current_session
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def display_markdown(content):
    print('')
    console.print(Markdown(content))
    print('')

@click.command(help='Make a question with session based on the current working directory')
@click.argument('question')
@click.pass_context
def question(ctx, question):
    
    with console.status("[bold green] 🦜 Thinking and hallucinating...[/]", spinner="dots"):
        response = invoke_question(question, model=ctx.obj["model"])
    
    display_markdown(response["answer"])


@click.command(help='Clean chat session of the current working directory')
def clean():
    clean_current_session()    