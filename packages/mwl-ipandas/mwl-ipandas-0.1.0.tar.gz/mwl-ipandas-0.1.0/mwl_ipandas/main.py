import ipdb
import typer

import pandas as pd

from pathlib import Path
from typing import Optional


app = typer.Typer()

@app.callback()
def callback():
    """
    This app opens pandas dataframe in an interactive mode
    """

@app.command()
def load(path: Optional[Path] = typer.Argument(None)):
    """
    Load a dataframe
    """
    if path is None:
        typer.echo("No input path given")
        raise typer.Abort()
    if path.is_dir():
        typer.echo("Path is a directory")
        raise typer.Abort()
    elif not path.exists():
        typer.echo("The path doesn't exist")
    elif path.is_file():

        df = None
        if path.suffix in ([".pickle", ".pkl"]):
            df = pd.read_pickle(path)

        elif path.suffix == ".csv":
            df = pd.read_csv(path)
        
        typer.echo(df.columns)
        typer.echo(df.head())
        
        ipdb.set_trace()

