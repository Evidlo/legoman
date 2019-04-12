# legoman

![logo](https://i.imgur.com/VJGdOWe.png)

A tiny static generator in 50 lines.

# Usage

Building the example

```
# install requirements
make requirements

# run devserver (requires inotify-tools)
make devserver
```

# How it works

- `.md` files will be rendered using the specified template in `templates/`
- `.j2` files are rendered with Jinja2, they can loop over `.md` files and access their metadata
- all other files are symlinked to `output/`

For example, the example `content/`:
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
├── codehilite.css -> /home/evan/resources/legoman/content/codehilite.css
├── index.html
├── projects
│   ├── bar_proj
│   │   └── index.html
│   └── foo_proj
│       ├── cheetos_small.png -> ~/legoman/content/projects/foo_proj/cheetos_small.png
│       └── index.html
└── styles.css -> ~/legoman/content/styles.css
```

# See also
- [Hugo](https://github.com/gohugoio/hugo) - similar idea, but written in Go and uses Go's templating engine
