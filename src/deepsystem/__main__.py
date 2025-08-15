import click
from commands import question, clean, model


@click.group(help='OS Agent system')
def cli():
    pass


cli.add_command(question)
cli.add_command(clean)
cli.add_command(model)

cli()