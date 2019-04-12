.ONESHELL:
.SILENT:
SHELL := /bin/bash

html: output
	python legoman.py

clean:
	rm output -rf

output:
	mkdir output

requirements:
	pip install jinja2 markdown python-markdown-math httpwatcher

devserver: output
	# kill backgrounded process on exit
	trap "exit" INT TERM
	trap "kill 0" EXIT
	# serve content
	httpwatcher --root output --watch content,templates --port 8000 &
	# wait for change and rebuild
	python legoman.py
	while :; do
		inotifywait -r -e modify --format %w content templates
		python legoman.py
	done
