#!/usr/bin/env python

import ast

import astpretty
import os
from collections import namedtuple
import configparser
import sys
from typing import Dict
from inspect import getsourcefile
from .kernel_cli import lab_start_kernel
from .docker import lab_build_image
from .overrides import start_kernel_override, build_image_override

if sys.version_info < (3, 8):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

import click


workspace = os.environ['WORKSPACE']
workspace_data = os.path.join(workspace, 'data')


@click.group()
def lab():
    pass


@lab.command()
def hello():
    click.echo('Hello!')


WorkspaceEntryPointMetadata = namedtuple(
    'WorkspaceEntryPointMetadata',
    ['name', 'value', 'project_name', 'project_version', 'project_path', 'script_name', 'absolute_script_path'])


cli_fn_override_mapping = {
    lab_start_kernel.__name__: start_kernel_override.lab_start_kernel,
    lab_build_image.__name__: build_image_override.lab_build_image
}


class WorkspaceCommands(click.MultiCommand):

    def list_commands(self, ctx):
        found_cli_plugins = self._cli_plugin_search()
        plugin_names = []
        if found_cli_plugins:
            plugin_names = list(found_cli_plugins.keys())
            plugin_names.sort()
        return plugin_names

    def get_command(self, ctx, folder):
        found_cli_plugins = self._cli_plugin_search()
        if folder not in found_cli_plugins:
            return None

        plugin = found_cli_plugins[folder]
        cli_plugin_script_path = plugin.absolute_script_path
        tree = self._patch_ast_with_impl(cli_plugin_script_path, plugin)
        code = compile(tree, cli_plugin_script_path, mode='exec')
        try:
            ns = {}
            eval(code, ns, ns)
            return ns[found_cli_plugins[folder].script_name]
        except Exception as e:
            click.echo(f'Exception raised: {type(e)}, {e}')
            return None

    @classmethod
    def _cli_plugin_search(cls) -> Dict[str, WorkspaceEntryPointMetadata]:
        cli_plugins = {}
        for folder in os.listdir(workspace):
            project_path = os.path.join(workspace, folder)
            setup_cfg_path = os.path.join(project_path, 'setup.cfg')
            if not os.path.exists(setup_cfg_path):
                continue

            setup_cfg = configparser.ConfigParser()
            setup_cfg.read(setup_cfg_path)
            if 'options.entry_points' not in setup_cfg or 'lab_assistant.cli_plugins' not in setup_cfg[
                'options.entry_points']:
                continue

            entry_point = setup_cfg['options.entry_points']['lab_assistant.cli_plugins']
            entry_point_name, entry_point_value = map(lambda x: x.strip('\n '), entry_point.split('='))
            script_name = cls.find_script_name_from_entrypoint(entry_point_value)
            absolute_script_path = cls._find_absolute_script_path(project_path, script_name)
            if not absolute_script_path:
                click.echo(
                    f'Error: project "{folder}" supplies a lab assistant CLI plugin but script "{script_name}" could not be loaded')
                continue

            if 'metadata' not in setup_cfg:
                click.echo(f'Error: Lab project "{folder}" detected without project metadata')
                continue

            if 'version' not in setup_cfg['metadata']:
                click.echo(f'Error: Lab project "{folder}" detected without project version metadata')
                continue

            cli_plugins[entry_point_name] = WorkspaceEntryPointMetadata(
                name=entry_point_name,
                value=entry_point_value,
                project_path=project_path,
                project_name=setup_cfg['metadata']['name'],
                project_version=setup_cfg['metadata']['version'],
                script_name=script_name,
                absolute_script_path=absolute_script_path)
        return cli_plugins

    @staticmethod
    def find_script_name_from_entrypoint(entry_point_value):
        if ':' in entry_point_value:
            script_path, function_name = entry_point_value.split(':')
            script_path_parts = script_path.split('.')
            script_name = script_path_parts[-1]
        else:
            script_path_parts = entry_point_value.split('.')
            script_name = script_path_parts[-1]
        return script_name

    @classmethod
    def _patch_ast_with_impl(cls, cli_plugin_script_path, plugin: WorkspaceEntryPointMetadata):
        with open(cli_plugin_script_path) as dependant_cli_file:
            tree = ast.parse(dependant_cli_file.read(), mode='exec')
            last_import_index = 0

            prepared_overrides = []
            for i, node in enumerate(tree.body):
                if isinstance(node, ast.ImportFrom) and \
                        (node.module == 'lab_assistant_utils.kernel_cli' or
                         node.module == 'lab_assistant_utils.docker'):
                    last_import_index = i + 1
                    for fn_name in node.names:
                        if isinstance(fn_name, ast.alias) and fn_name.name in cli_fn_override_mapping:
                            fn_override = cli_fn_override_mapping[fn_name.name]
                            fn_override_source_path = getsourcefile(fn_override)
                            prepared_override = cls._assign_project_variables(fn_override_source_path, plugin)
                            prepared_overrides.extend(prepared_override)
            tree.body[last_import_index:last_import_index] = prepared_overrides
            tree = ast.fix_missing_locations(tree)
            # astpretty.pprint(tree)
            return tree

    @staticmethod
    def _assign_project_variables(fn_override_source_path: str, plugin: WorkspaceEntryPointMetadata):
        with open(fn_override_source_path) as fn_override_file:
            override_tree = ast.parse(fn_override_file.read())
            # astpretty.pprint(override_tree)
            for node in override_tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'project_name':
                            node.value = ast.Constant(value=plugin.project_name, kind=None)
                        elif isinstance(target, ast.Name) and target.id == 'project_version':
                            node.value = ast.Constant(value=plugin.project_version, kind=None)
                        elif isinstance(target, ast.Name) and target.id == 'project_path':
                            node.value = ast.Constant(value=plugin.project_path, kind=None)
            return override_tree.body

    @staticmethod
    def _find_absolute_script_path(project_path: str, script_name: str) -> str:
        script_filename = f'{script_name}.py'
        exclude = {'.git', '.idea', '.ipynb_checkpoints', '__pycache__', '.pytest_cache', 'data'}
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in exclude]
            absolute_script_path = os.path.join(root, script_filename)
            if script_filename in files and os.path.exists(absolute_script_path):
                return absolute_script_path


class LabCliPlugins(click.MultiCommand):
    ENTRY_POINT_GROUP = 'lab_assistant.cli_plugins'

    def list_commands(self, ctx):
        eps = entry_points()[self.ENTRY_POINT_GROUP]
        plugin_names = []
        for e in eps:
            plugin_names.append(e.name)
        return plugin_names

    def get_command(self, ctx, plugin_name):
        eps = entry_points()[self.ENTRY_POINT_GROUP]
        for e in eps:
            if e.name == plugin_name:
                return e.load()


lab_cli_plugins = LabCliPlugins(help='Lab CLI plugin commands')
workspace_commands = WorkspaceCommands(help='Workspace commands')
cli = click.CommandCollection(sources=[lab, workspace_commands, lab_cli_plugins])

if __name__ == '__main__':
    cli()
