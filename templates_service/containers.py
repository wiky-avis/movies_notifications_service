from dependency_injector import containers, providers

from templates_service.common.connectors import db
from templates_service.common.repositories.templates import TemplatesRepository
from templates_service.common.services.templates import TemplatesService
from templates_service.common.validators import validator


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "templates_service.api.v1.endpoints.templates",
        ]
    )

    db_client = providers.Factory(db.DbConnector)
    html_validator = providers.Factory(validator.HTMLValidator)

    templates_repository = providers.Factory(
        TemplatesRepository,
        db=db_client,
        html_validator=html_validator,
    )

    notifications_service = providers.Factory(
        TemplatesService,
        repository=templates_repository,
    )
