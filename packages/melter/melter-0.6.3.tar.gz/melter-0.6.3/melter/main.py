import logging
import typer

from melter import __version__, __title__
from melter.start_reruns import run_workflow


app = typer.Typer()
LOG = logging.getLogger(__name__)


@app.callback()
def callback(debug: bool = False):
    """
    melter - Identifies which cases that should be analyzed again
    """
    if debug:
        typer.echo("DEBUG logging enabled")
        logging.basicConfig(level=logging.DEBUG)


@app.command()
def version():
    """
    Print the version
    """
    typer.echo("%s, version %s" % (__title__, __version__))


@app.command("start-reruns")
def start_reruns():
    """
    Identify cases that met the criteria for a rerun, and start them
    """
    LOG.info("Running %s, version %s" % (__title__, __version__))
    run_workflow()
