.ONESHELL:
.SILENT:
SHELL := /bin/bash
.SHELLFLAGS := -ec

html: output
	legoman build

devserver: output
	# kill backgrounded process on exit
	trap "exit" INT TERM
	trap "kill 0" EXIT
	# serve content
	httpwatcher --root output --watch content,templates --port 8000 &
	# wait for change and rebuild
	legoman build
	while :; do
		inotifywait -r -e modify --format %w content templates
		legoman build
	done

publish: html
	ghp-import -f -p -b master output

clean:
	rm output -rf

output:
	mkdir output
