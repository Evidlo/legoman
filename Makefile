.ONESHELL:
.SILENT:
SHELL := /bin/bash

html:
	python legoman.py

requirements:
	pip install jinja2 markdown python-markdown-math

devserver:
	# kill backgrounded process on exit
	trap "exit" INT TERM
	trap "kill 0" EXIT
	# serve content
	httpwatcher --root output --port 8000 &
	# wait for change and rebuild
	python legoman.py
	while :; do
		inotifywait -r -e modify --format %w content
		python legoman.py
	done
