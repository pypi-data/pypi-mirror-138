import logging
import os
import pathlib
import re
from sys import path
import click
from pathlib import Path

import yaml
from jinja2 import Environment
from rich.console import Console
from rich.syntax import Syntax

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)5s] %(message)s')
logger = logging.getLogger('TemplateRenderer')

# Config file Environment variables resolver
path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')

PathParam = click.Path(path_type=pathlib.Path)


def path_constructor(loader, node):
    source = node.value
    result = os.path.expandvars(source)
    logger.info('[path_constructor] expand vars for "%s" -> "%s"', source, result)
    if source == result:
        logger.warning('Variable "%s" not found.', source)
    return result


class YamlEnvVarLoader(yaml.SafeLoader):
    pass


YamlEnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
YamlEnvVarLoader.add_constructor('!path', path_constructor)


def load_config(data_file: Path):
    """Load data from YAML file into Python dictionary"""
    with data_file.open('r') as data_io:
        try:
            return yaml.load(data_io, Loader=YamlEnvVarLoader)
        except yaml.YAMLError as exc:
            logger.exception('Unable load config file "%s"', data_file)
            raise


def show_rendered(rendered: str):
    syntax = Syntax(rendered, "yaml", theme="fruity", line_numbers=True)
    console = Console()
    console.print(syntax)


def verify_result(rendered: str):
    """Load rendered"""
    try:
        yaml.unsafe_load(rendered)
    except yaml.YAMLError as exc:
        logger.error('Unable load result file: %s', exc)
        return False

    return True


@click.command()
@click.option(
    '-t',
    '--template-file',
    type=PathParam,
    required=True,
    help='Template file path',
)
@click.option(
    '-r',
    '--result-file',
    type=PathParam,
    required=True,
    help='Result file path',
)
@click.option(
    '-c',
    '--config-file',
    type=PathParam,
    required=True,
    help='Config file path',
    default=None,
)
@click.option(
    '-k',
    '--config-key',
    required=False,
    default=None,
    type=click.STRING,
    help='Config root key'
)
def render(template_file: Path, result_file: Path, config_file: Path, config_key: str):
    """Render template"""
    logger.info('Render template: "%s"', template_file)
    logger.info('Rendered file: "%s"', result_file)
    logger.info('Config file: "%s"', config_file)
    data = load_config(config_file)
    env = Environment(autoescape=True, trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(template_file.read_text())
    if config_key:
        data = data.get(config_key)
        if not data:
            logger.warning('Config key "%s" not found', config_key)
            return
    rendered = template.render(data)

    show_rendered(rendered)

    if verify_result(rendered):
        result_file.write_text(rendered)


if __name__ == '__main__':
    render()
