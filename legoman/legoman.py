from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import markdown
import click
from distutils.dir_util import copy_tree
import pkg_resources
import os
import sys
import logging

log = logging.getLogger("legoman")
logging.basicConfig()

content_dir = output_dir = j2env = None

@click.group()
@click.option('--debug', default=False, is_flag=True)
@click.option(
    '--content_dir', 'contentdir', envvar='CONTENT_DIR',
    default='.', metavar='PATH'
)
@click.option(
    '--output_dir', 'outputdir', envvar='OUTPUT_DIR',
    default='output', metavar='PATH'
)
@click.option(
    '--template_dir', 'templatedir', envvar='TEMPLATE_DIR',
    default='templates', metavar='PATH'
)
def main(debug, contentdir, outputdir, templatedir):
    global content_dir, output_dir, template_dir, j2env
    if debug:
        log.setLevel(logging.DEBUG)
    content_dir = Path(contentdir)
    output_dir = Path(outputdir)
    template_dir = Path(templatedir)

    j2env = Environment(loader=FileSystemLoader([template_dir]))
    # load macros and filters
    j2env.filters.update({'fm': frontmatter})
    j2env.globals.update({'glob': glob})

# ---------- Config ----------

md = markdown.Markdown(
    extensions=[
        'meta', 'codehilite', 'toc', 'attr_list', 'fenced_code', 'extra',
        'tables', 'toc', 'markdown_captions', 'mdx_include', 'mdx_math',
        'footnotes'
    ],
    extension_configs = {
        'mdx_math': {
            'enable_dollar_delimiter': True
        },
        'toc': {
            'anchorlink': True
        }
    }
)

# ---------- Filters & Functions ----------

def glob(*patterns):
    """Loop through files matching glob patterns.

    Args:
        *patterns (list of str): glob patterns to search with

    Returns:
        *paths (list of Path): paths to files
    """
    items = []
    for pattern in patterns:
        for path in content_dir.glob(pattern):
            if path.exists():
                items.append(path)
    return items


def frontmatter(paths, md=md):
    """Loop through file paths and parse frontmatter

    Args:
        *paths (list of Path): paths to files with frontmatter
    """
    items = []
    for path in paths:
        content = md.convert(path.read_text())
        items.append(
            {
                **{k:v[0] for k, v in md.Meta.items()},
                'path':path.relative_to(content_dir).with_suffix('.html'),
                'parent':path.relative_to(content_dir).parent,
                'content':content
            }
        )
    return items

# ---------- Rendering ----------

def render_md(text, j2env):
    """Render markdown to HTML

    Args:
        text (str): markdown content

    Returns:
        str: rendered HTML
    """
    html = md.reset().convert(text)
    if not 'template' in md.Meta:
        md.Meta['template'] = ['default.j2']
    template = j2env.get_template(md.Meta['template'][0])
    return template.render(**{k:v[0] for k, v in md.Meta.items()}, content=html)

def render_j2(text, j2env):
    """Render Jinja2 to HTML

    Args:
        text (str): Jinja2 content

    Returns:
        str: rendered HTML
    """
    template = j2env.from_string(text)
    return template.render()

# ---------- Building ----------

@main.command(short_help="generate content", help="generate output/ from content/")
@click.argument('content_file', required=False)
def build(content_file):
    """Loop content_dir and write rendered results to output_dir"""

    if content_file is not None:
        single(content_file)
    else:
        for content_file in content_dir.rglob('*'):
            if (content_file.is_relative_to(output_dir) or
                content_file.is_relative_to(template_dir) or
                content_file.is_relative_to('.git')):
                continue
            single(content_file)

def single(content_file):
    """Render single file"""
    content_file = Path(content_file)
    output_file = output_dir.joinpath(
        content_file.relative_to(content_dir)
    )
    output_file.parent.mkdir(exist_ok=True)
    log.debug('parsing ' + content_file.as_posix())

    try:
        if content_file.suffix.lower() == '.md':
            output_file.with_suffix('.html').write_text(
                render_md(content_file.read_text(), j2env)
            )

        elif content_file.suffix == '.j2':
            output_file.with_suffix('.html').write_text(
                render_j2(content_file.read_text(), j2env)
            )
        elif content_file.is_file():
            if output_file.is_file():
                output_file.unlink()
            os.link(str(content_file), str(output_file))
    except Exception as e:
        log.error('error parsing ' + content_file.as_posix())
        log.error(
            click.style(str(type(e)) + ' ' + str(e), fg='red'),
        )

@main.command(short_help="initialize project", help="initialize project")
def init():
    """Copy skeleton project from demo folder"""
    copy_tree(pkg_resources.resource_filename(__name__, 'demo/'), '.')