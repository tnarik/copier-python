# copier-python

A [Copier](https://github.com/copier-org/copier) template for Python projects.


## Features

[Poetry](https://github.com/python-poetry/poetry) used for package dependency management.


## Pre-usage instructions

Currently, this [Copier](https://github.com/copier-org/copier) template relies on and requires the [copier-templates-extensions](https://github.com/copier-org/copier-templates-extensions) plugin so that an embedded Jinja2 extension (`extensions/shell.py`) can be properly loaded and used in templates.

The plugin needs to be installed in the Python environment that is used with `copier`. If `copier` is installed via Homebrew (as it is the case in my setup), the easiest way would be to run the following from the command line:

`$(brew --prefix copier)/libexec/bin/pip3 install copier-templates-extensions`

The embedded `extensions/shell.py` extension is used because even  when a Jinja2 3.x version of [jinja2-shell-extension](https://github.com/metwork-framework/jinja2_shell_extension) is now published, the embedded version includes additional parameters.

##  Usage

Generation of a project is as simple as running:

`copier "gh:tnarik/copier-python" /path/to/your/new/project`

## Alternatives

Perhaps something like [pawamoy/copier-poetry](https://github.com/pawamoy/copier-poetry) is preferable for some people, but it includes too much magic and post-generation scripts which is something I prefer not using. In any case, you can give it a try.