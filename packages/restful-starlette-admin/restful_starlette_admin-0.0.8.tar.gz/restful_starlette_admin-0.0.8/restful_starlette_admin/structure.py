from restful_starlette_admin import file_content


PROJECT_STRUCTURE = {
    # root directory
    'aerich.toml': {'is_dir': False, 'content': file_content.project_name_aerich_toml},
    'main.py': {'is_dir': False, 'content': file_content.project_name_main_py},
    'README.md': {'is_dir': False, 'content': file_content.project_name_readme_md},
    '__init__.py': {'is_dir': False, 'content': file_content.common_init_py},
    # project directory
    'project': {'is_dir': True},
    'project/__init__.py': {'is_dir': False, 'content': file_content.common_init_py},
    'project/asgi.py': {'is_dir': False, 'content': file_content.project_name_project_asgi_py},
    'project/routes.py': {'is_dir': False, 'content': file_content.project_name_project_routes_py},
    'project/server.py': {'is_dir': False, 'content': file_content.project_name_project_server_py},
    'project/settings.py': {'is_dir': False, 'content': file_content.project_name_project_settings_py},
    # modules directory
    'modules': {'is_dir': True},
    'modules/__init__.py': {'is_dir': False, 'content': file_content.common_init_py},

}

APPLICATION_STRUCTURE = {
    # app root directory
    './{app_name}': {'is_dir': True},
    './{app_name}/__init__.py': {'is_dir': False, 'content': file_content.common_init_py},
    './{app_name}/app.py': {'is_dir': False, 'content': file_content.app_name_app_py},
    './{app_name}/endpoints.py': {'is_dir': False, 'content': file_content.app_name_endpoints_py},
    './{app_name}/routes.py': {'is_dir': False, 'content': file_content.app_name_routes_py},
    './{app_name}/models.py': {'is_dir': False, 'content': file_content.app_name_models_py},
    './{app_name}/transports.py': {'is_dir': False, 'content': file_content.app_name_transports_py},
}
