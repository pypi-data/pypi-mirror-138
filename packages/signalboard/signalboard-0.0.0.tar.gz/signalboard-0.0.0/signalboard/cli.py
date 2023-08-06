import sys

import click

from signalboard.main import run


@click.command()
@click.option('--port', default=5000, help='Server port number')
@click.option('--workers', default=None, help='Server workers')
def main(port, workers):
    run(port=port, workers=workers)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
