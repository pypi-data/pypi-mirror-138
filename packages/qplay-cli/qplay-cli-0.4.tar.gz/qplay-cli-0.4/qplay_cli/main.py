import click
from qplay_cli.dataset.commands import dataset

@click.group()
def quantplay():
    pass

quantplay.add_command(dataset)

if __name__ == '__main__':
    quantplay()