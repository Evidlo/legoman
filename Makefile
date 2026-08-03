# Evan Widloski - 2019-03-04
# makefile for building/testing legoman

# run all lines in target in single shell, quit on error
.ONESHELL:
.SHELLFLAGS = -ec

version := $(shell python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")


.PHONY: dist
dist:
	python -m build --sdist

.PHONY: pypi
pypi: dist man
	twine upload dist/legoman-$(version).tar.gz
