from pyfiglet import Figlet
import click
import sys


#####################
# Helpers: Printing #
#####################
def message_with_checkbox(message):
    return " [ %s ]  %s" % ("\u2713", message)


def message_with_dash(message):
    return " [ - ]  %s" % message


def message_with_error(message):
    return " [ ERROR ]  %s" % message


def ascii_art(message):
    return "\n" + Figlet(font="slant").renderText("  %s  " % message)


########
# Main #
########
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def accio():
    """
    Main Directory
    """
    pass


########
# Help #
########
@click.command("help", short_help="help for accio")
@click.pass_context
def help(context):
    click.echo(ascii_art("ACCIO"))
    click.echo(context.parent.get_help())


accio.add_command(help)


def main():
    args = sys.argv
    if len(args) == 1:
        click.echo(ascii_art("ACCIO"))
    accio()
