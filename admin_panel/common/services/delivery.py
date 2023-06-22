import csv
from base64 import b64decode

from common.exceptions import DeliveryException
from common.models.delivery import DeliveryModel, ObjectParameter, Recipient


class DeliveryParser:
    def __init__(
        self,
        delimiter: str = ";",
        replace_prefix: str = "data:text/csv;base64,",
        row_split: str = "\r\n",
        text_encoding: str = "utf-8",
    ):
        self.replace_prefix = replace_prefix
        self.delimiter = delimiter
        self.row_split = row_split
        self.text_encoding = text_encoding

    def decode_csv(self, encoded: str) -> list[dict]:
        encoded = encoded.replace(self.replace_prefix, "")
        decoded_csv = b64decode(encoded).decode(self.text_encoding)
        csv_reader = csv.DictReader(
            decoded_csv.split(self.row_split), delimiter=self.delimiter
        )
        return list(csv_reader)

    def build_model_list(
        self, input_data: dict, csv_list: list[dict]
    ) -> list[DeliveryModel]:
        models = []

        for row in csv_list:
            # Файл может содержать не только параметры, но и получателя с его имейлом
            # В таком случае их нужно убрать из параметров
            if "user_id" in row:
                user_id = row.pop("user_id")
            else:
                raise DeliveryException("Не у всех пользователей есть user_id")

            email = row.pop("email", None)

            recipient = Recipient(user_id=user_id, email=email)

            parameters = []

            if row:
                for key, value in row.items():
                    parameters.append(ObjectParameter(name=key, value=value))

            delivery = DeliveryModel(
                template_id=input_data["template_id"],
                recipient=recipient,
                parameters=parameters,
                channel=input_data["channel"],
                type=input_data["type"],
                sender="notifications_admin_panel",
            )

            models.append(delivery)

        return models
