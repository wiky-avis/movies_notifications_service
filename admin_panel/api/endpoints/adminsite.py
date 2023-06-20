import logging
from typing import Any

from common.exceptions import DeliveryException
from common.models.delivery import DeliveryChannel, DeliveryType
from common.services.communication import ServiceCommunicator
from common.services.delivery import DeliveryParser
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.amis.components import Form, InputFile
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from settings import settings
from starlette.requests import Request


logger = logging.getLogger(__name__)


# Create AdminSite instance
site = AdminSite(settings=Settings(database_url=settings.db.url))


@site.register_admin
class CreateTemplateForm(admin.FormAdmin):
    """
    Форма для создания шаблона
    """

    page_schema = "Создать шаблон"
    form = Form(
        title="Форма для создания шаблона", submitText="Создать шаблон"
    )

    class schema(BaseModel):  # Тут обязательно название с маленькой буквы
        """
        Класс для указания полей формы
        """

        template_name: str = Field(
            ..., title="Название шаблона", max_length=50
        )
        template_body: str = Field(
            ..., title="Содержимое шаблона", amis_form_item="textarea"
        )
        description: str = Field(
            ..., title="Описание", amis_form_item="textarea"
        )
        channel: DeliveryChannel = Field(DeliveryChannel.EMAIL, title="Канал")
        type: DeliveryType = Field(
            DeliveryType.NOT_NIGHT, title="Тип отправки"
        )

    # Запускается при отправке формы
    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        service_communicator = ServiceCommunicator()
        try:
            succeeded, msg = await service_communicator.create_template(
                data.dict()
            )
            if succeeded:
                return BaseApiOut(msg=msg)
            else:
                return BaseApiOut(status=-1, msg=msg)
        except Exception as e:
            logger.exception(e, exc_info=True)
            return BaseApiOut(status=-1, msg="Неизвестная ошибка")


@site.register_admin
class SendCommunicationForm(admin.FormAdmin):
    """
    Форма для отправки коммуникации
    """

    page_schema = "Отправить коммуникацию"
    form = Form(
        title="Форма для отправки коммуникации",
        submitText="Отправить коммуникацию",
    )

    class schema(BaseModel):
        """
        Класс для указания полей формы
        """

        template_id: int = Field(..., title="ID шаблона")
        channel: DeliveryChannel = Field(DeliveryChannel.EMAIL, title="Канал")
        type: DeliveryType = Field(
            DeliveryType.NOT_NIGHT, title="Тип отправки"
        )
        encoded_csv: str = Field(
            None,
            title="CSV файл с выборкой",
            amis_form_item=InputFile(
                btnLabel="Выбрать файл",
                asBase64=True,
            ),
        )

    async def handle(
        self, request: Request, data: schema, **kwargs
    ) -> BaseApiOut[Any]:
        """
        Запускается при отправке формы
        """
        service_communicator = ServiceCommunicator()
        delivery_parser = DeliveryParser()
        try:
            success_cnt = 0
            error_cnt = 0
            errors = set()

            decoded = delivery_parser.decode_csv(data.encoded_csv)
            models = delivery_parser.build_model_list(data.dict(), decoded)

            for model in models:
                succeeded, msg = await service_communicator.send_delivery(
                    model.dict()
                )
                if succeeded:
                    success_cnt += 1
                else:
                    error_cnt += 1
                    errors.add(msg)

            return BaseApiOut(
                msg=f"Успешных отправок - {success_cnt}\n Ошибок - {error_cnt}\n Ошибки - {errors}"
            )
        except DeliveryException as e:
            logger.exception(e, exc_info=True)
            return BaseApiOut(status=-1, msg=str(e))
        except Exception as e:
            logger.exception(e, exc_info=True)
            return BaseApiOut(status=-1, msg="Неизвестная ошибка")
