import typer

import alteia_cli.custom_analytics
import alteia_cli.plugins
from alteia_cli import config
from alteia_cli.loader import Loader

app = typer.Typer()
loader = Loader(app)
loader.extend_app(alteia_cli.custom_analytics.__path__)  # type: ignore
loader.extend_app(alteia_cli.plugins.__path__)


@app.command()
def configure():
    """ Configure platform credentials. """
    config.setup()


if __name__ == "__main__":
    app()
