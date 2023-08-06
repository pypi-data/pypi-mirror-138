"""Main CLI application"""
import json

import click

from kiraak.main import main
from kiraak.config import Config, API


@click.command()
@click.argument("json_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--clear", is_flag=True)
def cli(json_file: str, clear) -> None:
    """Initiates cli"""
    if clear:  # Clear cached login data
        Config.CONF_FILE.unlink()
        API.TOKEN_FILE.unlink()

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
