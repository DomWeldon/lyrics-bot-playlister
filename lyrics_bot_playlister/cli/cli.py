"""CLI tools to download lyrics etc."""
import typer

app = typer.Typer()


@app.command()
def hello():
    typer.echo("Hello!")


@app.command()
def goodbye():
    typer.echo("Goodbye!")
