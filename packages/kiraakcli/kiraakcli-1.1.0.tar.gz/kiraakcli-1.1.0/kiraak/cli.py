"""Main CLI application"""
import json

import click

from kiraak.main import main


@click.command()
@click.argument("json_file", type=click.Path(exists=True, dir_okay=False))
def cli(json_file: str) -> None:
    """Initiates cli"""
    if not json_file.endswith(".json"):
        click.echo("File must be a JSON file (.json)!")
        raise click.Abort()
    try:
        with open(json_file, "r") as file:
            json.load(file)
    except json.JSONDecodeError as err:
        click.echo("File must be a valid JSON file!")
        raise click.Abort() from err
    click.echo(f"Adding orders from {json_file}")
    main(json_file)
