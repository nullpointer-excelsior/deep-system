import click
from deepsystem.commands import question, clean, model


@click.group(help='OS Agent system')
def cli():
    pass


cli.add_command(question)
cli.add_command(clean)
cli.add_command(model)

cli()




# for x in history.get_code_snippets(history.find_message_content()):
#     print(x)