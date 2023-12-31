import re
from typing import Dict

from jinja2 import Environment, Template, meta
from jinja2.exceptions import TemplateError

from templates_service.common.exceptions import TemplateValidationError


class HTMLValidator:
    def __init__(self):
        self.env = Environment()
        self.template_str: str = None
        self.jinja_template: Template = None
        self.mandatory_parameters: list[str] = None
        self.optional_parameters: Dict[str, str] = None

    def parse(self, template_body: str) -> tuple[list | None, dict | None]:
        try:
            self.template_str = template_body
            # Парсит шаблон и выдает и возвращает специальную модель Template
            # https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template
            self.jinja_template = self.env.parse(self.template_str)

            # Парсим параметры в шаблоне, обновит атрибуты класса
            self.parse_parameters()

            return self.mandatory_parameters, self.optional_parameters

        except TemplateValidationError as template_error:
            raise template_error
        except TemplateError as jinja_error:
            if hasattr(jinja_error, "message"):
                error_message = jinja_error.message
            else:
                error_message = "Ошибка валидации шаблона"
            raise TemplateValidationError(error_message)
        except Exception:
            raise TemplateValidationError()

    def parse_parameters(self) -> None:
        # Получаем какие параметры ожидаются в шаблоне
        # Он возвращается все переменные, даже если у них есть дефолтные значения
        missing_parameters: set[str] = meta.find_undeclared_variables(
            self.jinja_template  # type: ignore
        )

        if not missing_parameters:
            return  # Значит нет параметров

        # Далее через регекс получаем какие параметры имеют дефолтные значения
        # Нотация дефолтных параметров всегда следующая:
        # {{ my_variable|default('my_variable is not defined') }}
        # Паттерн ниже получает название переменной и ее стандартное значение
        optional_pattern = re.compile(
            r"{{\s*(\w*)\s*\|\s*default\(['|\"](.*?)['|\"]"
        )
        optional_parameters = {
            match.group(1): str(match.group(2))
            for match in optional_pattern.finditer(self.template_str)
        }

        mandatory_parameters = [
            param
            for param in missing_parameters
            if param not in optional_parameters
        ]

        if not optional_parameters:
            self.optional_parameters = optional_parameters
        if not mandatory_parameters:
            self.mandatory_parameters = mandatory_parameters

    def render(self, template_body: str, template_parameters: dict) -> str:
        try:
            # Парсит шаблон и выдает и возвращает специальную модель Template
            # https://jinja.palletsprojects.com/en/3.1.x/extensions/#jinja2.nodes.Template
            jinja_template = self.env.from_string(template_body)

            return jinja_template.render(template_parameters)

        except TemplateError as jinja_error:
            if hasattr(jinja_error, "message"):
                error_message = jinja_error.message
            else:
                error_message = "Ошибка валидации шаблона"
            raise TemplateValidationError(error_message)
        except Exception:
            raise TemplateValidationError()
