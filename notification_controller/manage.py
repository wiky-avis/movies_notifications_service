import aiomisc
import click


@click.group()
def cli():
    pass


@cli.command(help="run-consumers")
@click.pass_context
def run_consumers(ctx):
    from src.workers.consumers.runner import main

    with aiomisc.entrypoint(
        *main.consumers,
        log_config=False,
        debug=main.config.debug,
    ) as loop:
        loop.run_forever()


@cli.command(help="run-daemons")
@click.pass_context
def run_daemons(ctx):
    from src.workers.cron.runner import main

    with aiomisc.entrypoint(
        *main.daemons,
        log_config=False,
        debug=main.config.debug,
    ) as loop:
        loop.run_forever()


if __name__ == "__main__":
    cli()
