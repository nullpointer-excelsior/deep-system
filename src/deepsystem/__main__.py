import click
from commands import question


@click.group(help='OS Agent system')
@click.option('--model', '-m', default="gpt-4.1-nano", help='OpenAI model to use')
def cli(model):
    print(f"using: {model}")


cli.add_command(question)

cli()