from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import markdown
import click
from distutils.dir_util import copy_tree
import pkg_resources
import os
import sys

# ---------- Config ----------

content_dir = Path('content')
template_dir = Path('templates')
output_dir = Path('output')

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
env = Environment(loader=FileSystemLoader(['templates', '.']))
main = click.group()(lambda: None)

def jinja_path(*patterns):
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

def render_md(text):
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
    template_path = template_dir.joinpath(md.Meta['template'][0])
    assert template_path.is_relative_to, "Template path must be subdir of template_dir"
    # render to template
    template = env.get_template(template_path.as_posix())
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

@click.command(short_help="generate content", help="generate output/ from content/")
def build():
    """Loop content_dir and write rendered results to output_dir"""

    for content_file in content_dir.rglob('*'):
        output_file = output_dir.joinpath(content_file.relative_to(content_dir))
        output_file.parent.mkdir(exist_ok=True)
        print('parsing ' + content_file.as_posix())

        if content_file.suffix.lower() == '.md':
            output_file.with_suffix('.html').write_text(
                render_md(
                    content_file.read_text()
                )
            )

        elif content_file.suffix == '.j2':
            output_file.with_suffix('.html').write_text(
                render_j2(content_file.read_text())
            )

        elif content_file.is_file():
            # symlink regular files to output_dir, replacing existing symlinks
            if output_file.is_file():
                output_file.unlink()
            os.link(str(content_file), str(output_file))


@click.command(short_help="run as CGI", help="process file through stdin")
@click.argument("filetype", type=click.Choice(['md', 'j2']))
def cgi(filetype):
    """Render text from stdin"""
    text = sys.stdin.read()

    if filetype == 'md':
        print(render_md(text))

    if filetype == 'j2':
        print(render_j2(text))


@click.command(short_help="initialize project", help="initialize project")
def init():
    """Copy skeleton project from demo folder"""
    copy_tree(pkg_resources.resource_filename(__name__, 'demo/'), '.')


main.add_command(build)
main.add_command(init)
main.add_command(cgi)
