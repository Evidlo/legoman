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
	# build and serve content
	legoman build
	livereload output -t output -p 8000 -w 1 &
	# wait for change and rebuild
	inotifywait -mre modify --format %w%f . --exclude legoman | while read path
	do
		legoman build $$path
	done

publish: html
	ghp-import -f -p -b master output

clean:
	rm output -rf

output:
	mkdir output