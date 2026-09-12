"""tjp CLI."""
import click
import uvicorn


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--port", default=8123)
def serve(port: int) -> None:
    uvicorn.run("tjp.app:app", port=port)


@main.command()
def inventory() -> None:
    from .desk import inventory as inv

    for k, v in inv().items():
        click.echo(f"{k}: {len(v)} files")
