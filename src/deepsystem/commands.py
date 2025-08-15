import click
from question import invoke as invoke_question



@click.command(help='Make a question with session based on the current working directory')
@click.argument('question')
def question(question):
    invoke_question(question)
