from string import Template


class StructureFileTemplate(Template):
    delimiter = '<%$%>'


common_init_py = StructureFileTemplate('''
''')

project_name_aerich_toml = StructureFileTemplate('''
[tool.aerich]
tortoise_orm = "project.settings.TORTOISE_ORM"
location = "./migrations"
src_folder = "./."

''')

project_name_main_py = StructureFileTemplate('''
import uvicorn

from project.settings import settings

app = 'project.asgi:app'

if __name__ == '__main__':
    uvicorn.run(app=app,
                host=settings.SYSTEM_SETTINGS.HOST,
                port=settings.SYSTEM_SETTINGS.PORT,
                reload=settings.SYSTEM_SETTINGS.DEBUG,
                use_colors=settings.SYSTEM_SETTINGS.DEBUG,
                ws='websockets'
                )
''')

project_name_readme_md = StructureFileTemplate('''
### <%$%>project_name powered by micro_kit

----

#### 1、数据库迁移
```shell

# 创建配置文件（default：aerich.toml）, 基本配置如下：

[tool.aerich]
tortoise_orm = "project.settings.TORTOISE_ORM"
location = "./migrations"
src_folder = "./."

# 指定配置文件进行初始化
aerich -c aerich.toml init -t project.settings.TORTOISE_ORM

# 初始化DB（只需要执行一次，已生成init.sql之后则无需再执行）
aerich init-db

# 生成新的迁移脚本
aerich migrate

# 执行最新的数据库迁移
aerich upgrade
```
''')

# ------------ project directory ------------

project_name_project_asgi_py = StructureFileTemplate('''
from project.server import create_application


app = create_application()

''')

project_name_project_routes_py = StructureFileTemplate('''
''')

project_name_project_server_py = StructureFileTemplate('''
from jinja2 import TemplateNotFound
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from starlette.types import ASGIApp
from tortoise.contrib.starlette import register_tortoise

from project.settings import TORTOISE_ORM
from restful_starlette.blueprint import Blueprint, register_blueprints
from restful_starlette.exception.handlers import GLOBAL_EXCEPTION_HANDLERS

from restful_starlette.log.structlog import setup_logging


async def template_not_found_handler(request: Request, exc: TemplateNotFound) -> Response:
    response = HTMLResponse(
        f'<html><body><h1>Not Found</h1><h3>there is not the template "{exc.name}"</h3></body></html>')
    return response


# 默认装载全局错误处理函数
GLOBAL_EXCEPTION_HANDLERS.update({
    TemplateNotFound: template_not_found_handler,
})


def create_application() -> ASGIApp:
    """
        create ASGI application instance
    :return:
    """

    app = Blueprint(middleware=[],
                    exception_handlers=GLOBAL_EXCEPTION_HANDLERS)

    from restful_starlette.apps.swagger.app import swagger

    # 单独注册接口文档
    register_blueprints(path='/', app=app, blueprints=[swagger, ])

    @app.on_event("startup")
    async def startup_event() -> None:
        setup_logging()

    register_tortoise(app, config=TORTOISE_ORM)

    return app

''')

project_name_project_settings_py = StructureFileTemplate('''
from pathlib import Path

from restful_starlette.conf.base import GlobalSettings

from restful_starlette.conf.db import MySQLSettings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'lpiZRQwWoj&*wh29Jovk$uA3YGP$TSQYpM4ooy1z3zGuNT=vmLp'


class Setting(GlobalSettings):
    """
        settings
    """
    # mysql settings
    MYSQL_SETTINGS: MySQLSettings


# get global settings
settings = Setting.get_global_settings(env_path=BASE_DIR / 'env')

# Tortoise orm settings
TORTOISE_ORM = {
    "connections": {"default": settings.MYSQL_SETTINGS.dsn},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                # "modules.test.models",
            ],
            "default_connection": "default",
        },
    },
}

''')

# ------------ App templates ------------

app_name_app_py = StructureFileTemplate('''# app
from .routes import routes
from restful_starlette.blueprint import Blueprint

blueprint = Blueprint(routes=routes)
''')

app_name_models_py = StructureFileTemplate('''# models
import typing

from tortoise import fields

''')

app_name_endpoints_py = StructureFileTemplate('''# endpoints

''')

app_name_routes_py = StructureFileTemplate('''# routes
from starlette.routing import Route, Mount

routes = [
    Mount(path='/<%$%>app_name', routes=[
        # <%$%>app_name
        # Route(path='/get/{id:int}', endpoint=endpoints.XXXXX),

    ]),
]
''')
app_name_transports_py = StructureFileTemplate('''# transports
from pydantic.main import BaseModel

''')
