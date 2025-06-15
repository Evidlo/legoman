from setuptools import setup
from pathlib import Path

setup(
    name='legoman',
    version='3.1.0',
    packages=['legoman'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="a tiny static website generator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    license="GPLv3",
    keywords="static web generator jinja2 markdown",
    url="https://github.com/evidlo/legoman",
    entry_points={
        'console_scripts': [
            'legoman = legoman.legoman:main',
        ],
    },
    scripts=['legoman/legoman_cgi'],
    install_requires=[
        "jinja2",
        "colorama",
        "markdown",
        "python-markdown-math",
        "livereload",
        "mdx_include",
        "markdown_captions",
        "ghp-import",
        "click"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
