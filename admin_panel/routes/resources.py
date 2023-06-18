import os
from typing import List

from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import (
    Action,
    Dropdown,
    Field,
    Link,
    Model,
    ToolbarAction,
)
from fastapi_admin.widgets import displays, filters, inputs
from starlette.requests import Request

from admin_panel.common.models import enums
from admin_panel.common.models.admin import Admin, Config, EmailTemplate
from admin_panel.settings.constants import BASE_DIR


upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "../static", "uploads"))


@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "admin model"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]

    async def get_toolbar_actions(
        self, request: Request
    ) -> List[ToolbarAction]:
        return []

    async def cell_attributes(
        self, request: Request, obj: dict, field: Field
    ) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)

    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []


# @app.register
# class Content(Dropdown):
#     class CategoryResource(Model):
#         label = "Category"
#         model = Category
#         fields = ["id", "name", "slug", "created_at"]
#
#     class ProductResource(Model):
#         label = "Product"
#         model = Product
#         filters = [
#             filters.Enum(
#                 enum=enums.ProductType, name="type", label="ProductType"
#             ),
#             filters.Datetime(name="created_at", label="CreatedAt"),
#         ]
#         fields = [
#             "id",
#             "name",
#             "view_num",
#             "sort",
#             "is_reviewed",
#             "type",
#             Field(
#                 name="image", label="Image", display=displays.Image(width="40")
#             ),
#             Field(name="body", label="Body", input_=inputs.Editor()),
#             "created_at",
#         ]
#
#     label = "Content"
#     icon = "fas fa-bars"
#     resources = [ProductResource, CategoryResource]


@app.register
class NotificationTemplate(Dropdown):
    class EmailTemplate(Model):
        label = "Email"
        model = EmailTemplate
        filters = [
            filters.Search(
                name="campaign_name",
                label="Название кампании",
                search_mode="contains",
                placeholder="campaign name",
            ),
            filters.Enum(
                enum=enums.NotificationStatus, name="status", label="Status"
            ),
            filters.Datetime(name="created_at", label="CreatedAt"),
        ]
        fields = [
            "id",
            "campaign_name",
            Field(
                name="html_code", label="Код шаблона", input_=inputs.Editor()
            ),
            "description",
            "status",
            "created_at",
        ]

    label = "Шаблоны"
    icon = "fas fa-bars"
    resources = [EmailTemplate]


@app.register
class ConfigResource(Model):
    label = "Config"
    model = Config
    icon = "fas fa-cogs"
    filters = [
        filters.Enum(enum=enums.Status, name="status", label="Status"),
        filters.Search(name="key", label="Key", search_mode="equal"),
    ]
    fields = [
        "id",
        "label",
        "key",
        "value",
        Field(
            name="status",
            label="Status",
            input_=inputs.RadioEnum(enums.Status, default=enums.Status.on),
        ),
    ]

    async def row_attributes(self, request: Request, obj: dict) -> dict:
        if obj.get("status") == enums.Status.on:
            return {"class": "bg-green text-white"}
        return await super().row_attributes(request, obj)

    async def get_actions(self, request: Request) -> List[Action]:
        actions = await super().get_actions(request)
        switch_status = Action(
            label="Switch Status",
            icon="ti ti-toggle-left",
            name="switch_status",
            method=Method.PUT,
        )
        actions.append(switch_status)
        return actions
