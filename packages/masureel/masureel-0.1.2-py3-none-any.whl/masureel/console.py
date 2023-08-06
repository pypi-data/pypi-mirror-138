import os 
import click

from . import __version__

@click.command()
@click.option("--update", "-u", is_flag=True)
@click.option("--translate", "-t", is_flag=True)
@click.argument('filename', type=click.Path(exists=True))
@click.version_option(version=__version__)
def main(update, translate, filename):
    if update:
        print('updating airtable cache')
    if translate:
        click.echo(click.format_filename(filename))
        print(f'translating {filename} in {os.getcwd()}')