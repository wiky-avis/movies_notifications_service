import click

from notifications_api.src.settings import logger, settings


@click.group()
def cli():
    pass


@cli.command("api")
def api():
    import uvicorn

    from notifications_api.src.app import create_app

    uvicorn.run(
        create_app(),
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
        reload=True,
    )
