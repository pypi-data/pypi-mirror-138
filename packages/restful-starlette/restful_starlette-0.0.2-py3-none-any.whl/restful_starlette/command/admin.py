import os

import click
import file_content

project_structure = {
    # root directory
    './{project_name}': {'is_dir': True},
    './{project_name}/aerich.toml': {'is_dir': False, 'content': file_content.project_name_aerich_toml},
    './{project_name}/main.py': {'is_dir': False, 'content': file_content.project_name_main_py},
    './{project_name}/README.md': {'is_dir': False, 'content': file_content.project_name_readme_md},
    # project directory
    './{project_name}/project': {'is_dir': True},
    './{project_name}/project/__init__.py': {'is_dir': False, 'content': file_content.common_init_py},
    './{project_name}/project/asgi.py': {'is_dir': False, 'content': file_content.project_name_project_asgi_py},
    './{project_name}/project/routes.py': {'is_dir': False, 'content': file_content.project_name_project_routes_py},
    './{project_name}/project/server.py': {'is_dir': False, 'content': file_content.project_name_project_server_py},
    './{project_name}/project/settings.py': {'is_dir': False, 'content': file_content.project_name_project_settings_py},
    # modules directory
    './{project_name}/modules': {'is_dir': True},
    './{project_name}/modules/__init__.py': {'is_dir': False, 'content': file_content.common_init_py},

}


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
def init_project(name):
    for file in project_structure:
        completed_path = file.format(project_name=name)
        config = project_structure.get(file)
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


if __name__ == '__main__':
    admin_cli()
