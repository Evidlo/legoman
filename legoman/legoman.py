from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import markdown
import click
from distutils.dir_util import copy_tree
import pkg_resources
import os
import sys

@click.group()
@click.option('--debug', default=False, is_flag=True)
@click.option('--content_dir', envvar='CONTENT_DIR', default='content', metavar='PATH')
@click.option('--output_dir', envvar='OUTPUT_DIR', default='output', metavar='PATH')
@click.option('--template_dir', envvar='TEMPLATE_DIR', default='templates', metavar='PATH')
@click.pass_context
def main(ctx, debug, content_dir, output_dir, template_dir):
    if debug:
        click.echo("Debugging enabled...")
    ctx.content_dir = Path(content_dir)
    ctx.output_dir = Path(output_dir)
    ctx.j2env = Environment(loader=FileSystemLoader([template_dir]))

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
        }
    }
)

def jinja_path(*patterns, content_dir):
    """Search through content_dir and find markdown files matching glob patterns

    Args:
        *patterns (list of str): glob patterns to search with

    Returns:
        list of dict: where each dict
    """
    items = []
    for pattern in patterns:
        for path in content_dir.glob(pattern):
            md.convert(path.read_text())
            items.append(
                {
                    **{k:v[0] for k, v in md.Meta.items()},
                    'path':path.relative_to(content_dir).with_suffix('.html')
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
    # get template
    if not 'template' in md.Meta:
        md.Meta['template'] = ['default.j2']
    template = j2env.get_template(md.Meta['template'][0])
    return template.render(**{k:v[0] for k, v in md.Meta.items()}, content=html)


def render_j2(text):
    """Render Jinja2 to HTML

    Args:
        text (str): Jinja2 content

    Returns:
        str: rendered HTML
    """
    template = env.from_string(text)
    return template.render(path=jinja_path)

# ---------- Building ----------

@main.command(short_help="generate content", help="generate output/ from content/")
@click.pass_context
def build(ctx):
    """Loop content_dir and write rendered results to output_dir"""

    for content_file in ctx.parent.content_dir.rglob('*'):
        output_file = ctx.parent.output_dir.joinpath(
            content_file.relative_to(ctx.parent.content_dir)
        )
        output_file.parent.mkdir(exist_ok=True)
        click.echo('parsing ' + content_file.as_posix())

        if content_file.suffix.lower() == '.md':
            output_file.with_suffix('.html').write_text(
                render_md(content_file.read_text(), ctx.j2env)
            )

        elif content_file.suffix == '.j2':
            output_file.with_suffix('.html').write_text(
                render_j2(content_file.read_text(), j2env)
            )

        # symlink regular files to output_dir, replacing existing symlinks
        elif content_file.is_file():
            if output_file.is_file():
                output_file.unlink()
            os.link(str(content_file), str(output_file))


@main.command(short_help="render single file", help="render single file")
@click.argument('input_file')
@click.pass_context
def single(ctx, input_file):
    """Render single file"""
    input_file = Path(input_file)

    if input_file.suffix.lower() == '.md':
        print(render_md(input_file.read_text(), ctx.parent.j2env))

    if input_file.suffix.lower() == '.j2':
        print(render_j2(input_file.read_text(), ctx.parent.j2env))


@main.command(short_help="initialize project", help="initialize project")
def init():
    """Copy skeleton project from demo folder"""
    copy_tree(pkg_resources.resource_filename(__name__, 'demo/'), '.')
