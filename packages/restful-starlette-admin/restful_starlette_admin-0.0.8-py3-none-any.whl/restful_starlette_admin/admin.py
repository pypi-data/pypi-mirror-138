import importlib
import os

import click
from restful_starlette_admin import file_content
from restful_starlette_admin.structure import PROJECT_STRUCTURE, APPLICATION_STRUCTURE


@click.group()
def admin_cli():
    """Admin CLI: provide actions to initial restful starlette project"""
    pass


@admin_cli.command()
@click.option(
    "--name",
    default="new_project",
    type=click.STRING,
    help="The new project name",
)
def start_project(name):
    for file in PROJECT_STRUCTURE:
        completed_path = file.format(project_name=name)
        config = PROJECT_STRUCTURE.get(file)
        if config.get('is_dir', False):
            # 文件夹先验证是否存在，不存在则递归创建
            if not os.path.exists(completed_path):
                os.makedirs(completed_path)
                print(f'创建文件夹 --> {completed_path}')
        else:
            # 文件直接创建，并写入预设内容

            context = {
                'label': file,
                'project_name': name,
                'file': file,
                'completed_path': completed_path,
            }

            with open(file=completed_path, mode='w') as f:
                f.write(config.get('content', file_content.StructureFileTemplate("")).substitute(context))
            print(f'创建文件 --> {completed_path}')


@admin_cli.command()
@click.option(
    "--name",
    default="new_app",
    type=click.STRING,
    help="The new app name",
)
def start_app(name):
    for file in APPLICATION_STRUCTURE:
        completed_path = file.format(app_name=name)
        config = APPLICATION_STRUCTURE.get(file)
        if config.get('is_dir', False):
            # 文件夹先验证是否存在，不存在则递归创建
            if not os.path.exists(completed_path):
                os.makedirs(completed_path)
                print(f'创建文件夹 --> {completed_path}')
        else:
            # 文件直接创建，并写入预设内容

            context = {
                'label': file,
                'app_name': name,
                'file': file,
                'completed_path': completed_path,
            }

            with open(file=completed_path, mode='w') as f:
                f.write(config.get('content', file_content.StructureFileTemplate("")).substitute(context))
            print(f'创建文件 --> {completed_path}')


@admin_cli.command()
@click.option(
    "--setting_class",
    default="restful_starlette.conf.base.GlobalSettings",
    type=click.STRING,
    help="Create env file, example: restful_starlette.conf.base:GlobalSettings",
)
@click.option(
    "--work_directory",
    default="./",
    type=click.STRING,
    help="Work directory",
)
def init_env(setting_class, work_directory):
    import sys
    sys.path.append(work_directory)
    module_path, class_name = setting_class.rsplit(':', 1)
    # print(module_path, class_name)
    setting_module = importlib.import_module(module_path)

    local_setting_class = getattr(setting_module, class_name)
    if hasattr(local_setting_class, "generate_env_file"):
        local_setting_class.generate_env_file()
        print("Create file .env successfully ...")


if __name__ == '__main__':
    admin_cli()
