import click
from question import invoke as invoke_question
from sessions import clean_current_session



@click.command(help='Make a question with session based on the current working directory')
@click.argument('question')
def question(question):
    invoke_question(question)


@click.command(help='Clean chat session of the current working directory')
def clean():
    clean_current_session()