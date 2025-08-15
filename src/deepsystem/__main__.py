import click
from commands import question, clean


@click.group(help='OS Agent system')
@click.option('--model', '-m', default=None, help='OpenAI model to use')
@click.pass_context
def cli(ctx, model):
    ctx.ensure_object(dict)
    ctx.obj["model"] = model
    print(f"using: {model}")


cli.add_command(question)
cli.add_command(clean)

cli()