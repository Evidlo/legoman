# legoman

<img src="demo/content/man.svg" width=200>

Simple static website generator.

Supports TOC, image captions, LaTeX, code highlighting and tables.

[Demo](http://evanw.org)

# Usage

``` bash
pip install legoman

# in an empty directory
legoman init
make html

# run devserver (requires inotify-tools)
make devserver
```

# How it works

Files in `content/` are rendered and copied to `output/`, so the directory structure of your rendered website matches the structure of your source files.

For example, the demo `content/`:
```
content
├── codehilite.css
├── index.j2
├── projects
│   ├── bar_proj
│   │   └── index.md
│   └── foo_proj
│       ├── cheetos_small.png
│       └── index.md
└── styles.css
```

yields this `output/`
```
output
├── codehilite.css
├── index.html
├── projects
│   ├── bar_proj
│   │   └── index.html
│   └── foo_proj
│       ├── cheetos_small.png
│       └── index.html
└── styles.css
```

# CGI

Legoman can also render files on the fly, which is useful for dynamically rendering files on a webserver.

    echo '# hello world' | legoman cgi md
    
Or for serving markdown with lighttpd:

    $HTTP["url"] =~ "\.md$" {
        cgi.assign = ( ".md"  => "/path/to/legoman cgi md")
    }

# See also
- [Hugo](https://github.com/gohugoio/hugo) - similar idea, but written in Go and uses Go's templating engine
- [Dozens of other static website generators](https://www.staticgen.com/)
