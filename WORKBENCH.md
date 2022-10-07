# Introduction

This document desribes my chosen tools, processes and workflow for a generic python based project as per my preferred workflow/framework/process.

It might get added to a separate project (skeleton, template, cookiecutter, yeoman generator, etc) so that it can be used as documentation and evolve as practices do, being clearly distinct from product specific details.

## Rationale

Python projects can be started without any development workbench or framework (just a script and a bunch of assets), but with some simple structure the handling of project dependencies, packaging and distribution becomes easier and allows for powerful integrations.

There are different approaches to follow. Mine is based on Poetry for the most part (something I started doing many times for many projects, but never committed 100% to). It will enforce project environment isolation and dependency management. It does so by using a TOML descriptor file (`pyproject.toml`) for the project.

Obviously this requires [Poetry](https://python-poetry.org/), which can be installed from the source or via Homebrew (on macOS). A Homebrew or a recommended installation runs in isolation as a program. It can also be installed via PIP (not recommended). If it was already installed, then `poetry self update` or `brew update && brew install poetry` will take care of upgrading the version.

When a project is already existing, the easiest approach is to add a `pyproject.toml` file manually or using `poetry init` from within the project folder, which starts an interactive process. See other projects for reference.


# Notes on tools

## Criteria

Although most systems include a default Python installation, the most extended usage of Python relies on virtual environments or _venv_ (as per Python's module from 3.3) to provide isolation across projects, particularly during development phases. There are different ways of achieving this based on preferences, framework styles and requirements.

This document describes my process.

## Pyenv

It is very convenient to install several versions of Python on the same system. This helps with testing of version support while also isolating development environments from the main system installation.

[`pyenv`](https://github.com/pyenv/pyenv) is a great tool for this and it is dettached from virtual environments and additional packages (a difference with Conda, for instance).

Suggested installation is via `brew install pyenv`, which should be followed by the next series of commands (in the case of **Zsh**) for shell integration and to solve a warning from `brew doctor` executions (regarding "config" scripts outside of the system).

```
echo '# Pyenv ' >> ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo '' >> ~/.zshrc
echo '# solve brew doctor warning' >> ~/.zshrc
echo "alias brew='env PATH=\"\${PATH//\$(pyenv root)\/shims:/}\" brew'" >> ~/.zshrc
```
Of course, this might change with newer versions of `pyenv` or the installation method used.

---
**note**: Installation requires compilation on the machine. If the Homebrew `binutils` are installed (`brew list binutils`), then it requires uninstallation as they are poorly supported on macOS and some headers/symbols are missing.

To check if there are any Homebrew packages installed that depend on it, run `brew uses binutils --installed`.

**In my case it was a dependency of `crosstool-ng`, but I don't recall ever using this sucessfully, so no harm done. I'll go back to this when/if needed.**

---

### Useful commands

* `python -V` : indicates the current active version of Python
* `pyenv versions` : list versions installed and the one selected for the project (see `pyenv local`)
* `pyenv install --list` : list available versions
* `pyenv install <version>` : installs version `<version>` (under `$(pyenv root)/versions`)
* `pyenv update` (or `brew upgrade pyenv`) upgrades `pyenv` so that newer versions can be installed
* `pyenv local <version>` : selects the Python version to use for that folder/project, persisted in a `.python-version` file.
* `pyenv which <executable>` : prints the full path of an executable (`pyenv which python` will provide the path where `python` is installed, not the shim)

### Usage

1. Install whichever versions of Python are desired using the `pyenv install` command described previously (check `pyproject.toml` if already existing to comply with the constraint),

   Do NOT set a python version as global (NO `python global <version>`).
2. Choose the correct version of Python matching the project requirements, or the desired working version (and set in `pyproject.toml`).
3. Automate version selection via `direnv` (see below my preferred approach of additionally creating a _venv_).

Currently `poetry` doesn't use `pyenv` automatically, so all python installation will be done outside of `poetry`. Activation is also external to provide more flexibility. It is automated via `direnv` (although it can be done manually).

## Direnv

There are many ways of ensuring the correct version of python or a virtual environment is used overall for a project. Some are manual, some automated. My preferred tool for this (and other automations) is [direnv](https://direnv.net/). **direnv** augments shells by loading and unloading environment variables depending on the current directory.

From **direnv** version 2.21.0, a `layout pyenv` is supported. It provides more control than the previous `layout python` or `layout python3`, which can be adopted if upgrading **direnv** is not an option.

A `.envrc` file is created and added to the project to ensure:

* a Python version matching the constraint in `pyproject.toml` is specified and enforced.
* a local _venv_ is created, with a symlink at `.venv` for compatibility with other tools (and Poetry managed local _venv_). This happens when first changing into the project directory once `direnv allow <project directory>` has been run.

**direnv** is by no means required, as version and _venv_ activation can be handled manually, or delegated fully to `poetry`, but it helps ensuring the automated creation of _venv_ EXTERNALLY to Poetry, so that Poetry will run in it, while at the same time reducing errors as the version and _venv_ will be used regardless of wrapping commands with `poetry run`.

This is currently the best way I could find to manage the Python version with the current constraints of the tools.

### Useful commands

* `direnv allow <project>` : allow direnv integration for the `<project>` folder
* `direnv allow` : allow direnv integration the current project
* `direnv deny` : block direnv integration for the current project or `<project>` if passed
* `direnv edit` : open and edit `.envrc` for the current project or `<project>` if passed

### Usage

Create a `.envrc` with the following content within the `<project>` folder:

```
layout pyenv <python version> # 3.9.13, for instance

ln -s .direnv/$(basename $VIRTUAL_ENV) .venv 2>/dev/null || return 0
```

Run `direnv allow <project>`.

## Poetry

### Installation

[Poetry](https://python-poetry.org/) needs to be installed externally to the project as well. This can be done via the custom installer or via Homebrew (on macOS). A Homebrew or a recommended custom installation runs in isolation as a program. It can also be installed via `pip`, although this is not recommended.

If it was already installed, then `poetry self update` or `brew update && brew install poetry` will take care of upgrading the Poetry version.

Recommended version is >=1.2.0, although 1.1.14 (and most of the 1.1.x line) was used successfully.

### Configuration

When in doubt, Poetry's configuration can be checked with `poetry config --list`. More information is available [here](https://python-poetry.org/docs/master/configuration/).
Configuration changes to Poetry itself would typically take place via the modification of `config.toml` (a configuration file located in a common folder such as `~/Library/Preferences/pypoetry/config.toml` on macOS) or a `poetry config <setting name> <setting value>` command. 

If the flag ` --local` is used, then a `poetry.toml` file will be created at the root level of the project folder, containing that local configuration.

There is a set of recommended configuration flags:

* `poetry config virtualenvs.in-project true` : so that any Poetry managed _venv_ will be created within the project.
* `poetry config virtualenvs.create true` : this is the default, but guarantees a _venv_ will always be created to avoid polluting the Python version used by Poetry itself (if not, when running `poetry install` the dev package could get installed on top of Poetry's Python, as an example).
* `poetry config virtualenvs.prefer-active-python true` : experimental from version `1.2.0`. It allows the creation on a managed _venv_ based on the active Python version.

### Useful commands

* `poetry -V` : indicates the current version of Poetry
* `poetry list` : list Poetry commands
* `poetry version [major, minor, patch]`: used to bump the version in Poetry
* `poetry build` : to build
* `poetry publish` : to publish
* `poetry config --list` : check poetry configuration
* `poetry config <setting> <setting value> [--local]` : configure `<setting>` with value `<setting value>`
* `poetry new <folder>` : creates a new Poetry managed project in `<folder>`
* `poetry init` : initialiles a Poetry managed project in the current folder, interactively
* `poetry env info -p` : provides the path to the _venv_ used by `poetry`
* `poetry add $(cat requirements.txt)` : adds requirements from a `requirements.txt` file
* `poetry export -o requirements.txt` : produce a `requirements.txt` file


### Usage

Poetry project initialisation can be done via:

* `poetry new <folder> [--src]` : when there is no preexisting code in the folder to be created. see [documentation](https://python-poetry.org/docs/cli/#new). `--src` is used to create a `src` folder layout (with modules in `src/<package>`). The `src` layout is my preferred option above the direct one (modules in `<package>`).
* `poetry init` : when there is preexisting code. The command should be run within the folder.

To allow building, a Python project structure should be used (this is important if modifying it or creating it manually at first). When initialising an already existing set of Python files, it is quite common to have them layed out directly under the project folder. Some reestructuring might be required first (moving files under `<folder>/<package>` or `<folder>/src/<package>`)

## Pre-commit

[pre-commit](https://pre-commit.com/) is a tool that simplifies the management of `git` pre-commit hooks. It is particularly suited for linters and code stylers.

The linters used by `pre-commit` are installed a specific cache, and not in the project _venv_.
If all linting or styling is meant to happen automatically then the corresponding tools can be removed from the development dependencies. Be mindful as this would imply losing the capability of using the tools manually and some IDE integration.

### Installation

The recommended installation is as a global tool, similarly to Poetry. This is because `pre-commit` can be used with non-Python projects and to ensure dependency isolation.

Use `brew install pre-commit`.

### Useful commands

* `pre-commit install` : installs the pre-commit script.
* `pre-commit uninstall` : uninstalls the pre-commit script, effectively disabling the integration.
* `pre-commit install-hooks` : nstalls the hooks environments without running them (if they were not available, they will get installed the first time they are run anyway).
* `pre-commit run` : runs the hooks on all staged files explicitely. If `-a` is used, they will run on all repo files.
* `pre-commit sample-config` : creates a sample file. This shouldn't be needed as the skeleton file provided with this workflow can used instead.
* `pre-commit autoupdate` : autoupdates the repos in the config to the latest versions.

### Usage

After installation of the tool, the pre-commit script and the installation of the hook repos, standard use of git will ensure hooks run before accepting a commit. Any error will prevent the commit from taking place.

`pre-commit` can be used manually (via `run`) and it will only affect the staged files unless `-a` (or `--all-files`) is passed.
Manual running is only recommended when configuring new hooks.


# Notes on Python versions

## Python version (constraint)

When initialised, a project will be configured to use the same python version used for the installation of `poetry` (the required one in case of using `brew` (see `brew info poetry --json` but keep in mind that the `brew` formulae might have been updated without upgrading the installed packages). This is reflected in the `[tool.poetry.dependencies]` section of the project `pyproject.toml` file.

Changing the constraint is done via edition of `pyproject.toml`. Alignment between the constraint and the actual Python version is achieved either via `pyenv` and the `.envrc` file. An alternative (not used in my process) is to ensure the desired Python version is installed somehow (via `pyenv` or otherwise) and making use of a Poetry managed _venv_.

This cosntraint is checked but it is dettached from the interpreter version used, in that enforcement of the constraint is attempted (a valid and avaialble Python version is looked for within the PATH).

## Python version (interpreter)

If there is no version of Python installed via `pyenv` (or otherwise), then the only one available would be the **system** one. This version will be whatever was already available or installed (either by default or due to the installation of `poetry` or similar via Homebrew). The preferred way of decoupling this version dependency is to ensure Python versions are installed via `pyenv`, and then activated and used from `poetry`.

`poetry` doesn't integrate with `pyenv` nor with `.python-version` files (created when running `pyenv local <version>`) automatically, but it is able to detect when it is running within an active _venv_. Therefore, my preferred option is to ensure `poetry` uses a _venv_ created externally explicitly, that is located within the project folder. This way, the environment and Python version can be used with or without `poetry` and _venv_ visibility is more immediate. This _venv_ creation and activation is handled via `direnv` as a way of automating the process.

## _venv_

Virtual environments (or _venv_) are recommended to avoid dependency pollution across projects, by isolating those dependencies for a given project. The feature has evolved along different versions of python, with slightly different implementations, but it is part of Python since version 3.3.

There are different ways of handling virtual environments:

* automatically generated and managed via Poetry: this depends on the configuration setting `virtualenvs.create` being `true` (or not set) and NOT running within an active _venv_ when executing certain commands on the folder.
* implicitly via `layout pyenv` usage in a `direnv` configuration file or manually.
* integrated with conda/mamba.

Poetry doesn't create virtual environments on your behalf during initialisation. They are created when required during the execution of a command `poetry show`, `poetry run`. Because we are using `direnv` to manage the local _venv_, a `.envrc` must be created and enabled for the project first.

This way `poetry` detects the current _venv_ (if activated) and it will not use the "system" Python version nor attempt to locate a version and create a managed _venv_. It also provides more control than just relying on the order of Python installations in the PATH (as Poetry can search for valid Python versions if available).

An alternative that results in Poetry managed _venv_ is available from 1.2.0. It requires enabling `virtualenvs.prefer-active-python` and running:

```
pyenv install <version> # if not installed yet
pyenv shell <version> # poetry shell 3.9.13, for instance
poetry new <project>
cd <project>
vi pyproject.toml # to edit the python constraint
poetry env use python
```

---
**note**: Running in a virtual environment can be checked via:

* global variable `VIRTUAL_ENV` being populated
* `python -c "import sys; print(sys.prefix != sys.base_prefix)"` printing `True`.

  `sys.base_prefix` is the prefix of the system Python a _venv_ was created from (if using `venv` or recent versions of `virtualenv`). For older versions of the `virtualenv` module, `sys.real_prefix` should be used.

---

### Poetry managed _venv_

For completeness, this section provides some information regarding Poetry managed virtual environments.

Poetry could be configured to support the creation of managed local _venv_ (`virtualenvs.in-project` set to `true`), but that would require additional integration for out-of-Poetry usage. Without this setting, Poetry would use the path configured by `poetry config virtualenvs.path`, which might result in orphan _venv_ when deleting projects but not dealing with the Poetry setup first.

The folder for a managed local _venv_ is `.venv`.

If a specific version of Python is desired for a managed _venv_, then it needs to be done explicitly via `poetry env use 3.9` (for instance). This attempts to locate the desired Python version and creates the virtual environments explicitly.

If managed virtual environments are not local to the project, the association of project to virtual environment is kept by poetry itself in `<virtualenvs.path>/envs.toml`.

The following are useful commands for Poetry managed _venv_:

* `poetry env info -p` : provides the path to the _venv__ used by `poetry`
* `poetry config virtualenvs.path` : provides the path to all Poetry managed _venv_ outside of projects
* `poetry env list` : gives list of environments available for the current project
* `poetry env remove <python environment>` : with `<python environment>` being an item from `poetry env list`
* `poetry env use <version>` : to create a managed _venv_ with Python `<version>`
* `poetry env use system`: disables an explicitely activated managed _venv_


If `direnv` were not used, `pyenv local <version>` is recommended when used this way:

```
pyenv local <version>
poetry env use python
```

## Tox

When using [tox](https://tox.wiki/en/latest/), python versions are indicated via `envlist`.

The desired python versions need to be available to `tox`, when not used as full paths (as used with `--discover`). This means the versions need to be available in the path.

Major and minor versions are supported by default, discovering whichever version is available in the system. This means the binaries need to be available in the path, be it directly or via `pyenv` integration.
When using within a _venv_ (as done via `pyenv` and `direnv`), a `PYENV_VERSION` variable is created, which deactivates the loading of `.python-version` (if it was present).
If `PYENV_VERSION` were unuset, then the Python versions listed in `.python-version` would be used (these were installed by `pyenv`). The exception is that, as `tox` is run from within a _venv_, it will use the _venv_ python version for the matching major and minor. In other words, if _venv_ were set to `3.9.13`, this would take precedence over any `3.9` indicated in `.python-version` (`3.9.10`, for instance).

If testing against different patch versions (but the same major and minor, as in `M.m.*`) is desired, then the `tox.ini` configuration needs to be enhanced to support this. To do so:

* specific environments need to created (and used in `envlist`). In the parlour of `tox` these are also called "virtual environment factors"
* a `basepython` property needs to be configured accordingly

An example of this kind of configuration is the following (where `py382` is the name of the synthetic environment/_venv_ factor):

```
[testenv:py382]
basepython = python3.8.2
```

Currently this doesn't work this way (it requires a full path or the binary to be named that way).
Also, for tox 3.x as, `basepython` needs to be added to all factors as otherwise the default rules cannot find an interpreter ([see this issue](https://github.com/tox-dev/tox/issues/1737)).

A `--discover` flag can also be used to give precedence to a given installed version, as in `tox --discover /path/to/python3.8.2`. Several paths can be provided for a multi-environment tox run with discovery enforcement.

**note**: In general, there is not reason to test on different patch versions, and due to the issues described above it is discouraged, particularly in a local workspace due to the `unset PYENV_VERSION` required and the incomplete behaviour observed. It might change with `tox 4.x`. Additionally, testing via tox is better suited for CI/CD related testing, or as a final check only.

### Changes expected for >4.0.0

Better support of `basepython` and patch versions (amongst other things).

# Notes on project structure

Use GIT even if the project would remain local  (via `git init .`) to keep track of changes. It is a good idea to commit the very first initial setup before any code is introduced if possible, so that it can be used as a starting point.

## Files

There are a couple of files quite useful in a Python project (or other development projects) which are linked to additional tools.

* `.editorconfig` : configuration file for [https://editorconfig.org/](https://editorconfig.org/), which integrates with several IDEs and editors (sometimes requiring plugins to do so) to automate the configuration of editing settings (whitespace vs tabs, number of tabs, etc.). It helps improving code style consistency. I try to standardise this file for a given language.
* `.envrc` : enables shell integrations if the system supports [direnv](https://direnv.net/) to load and unload environment variables automatically when working on a project folder (loading a given _venv_, for instance). It is enabled by the execution of `direnv allow` on the project folder.
* `.gitignore` : prevents code repository pollution. I tend to build it ad-hoc instead of relying on common files or generators such as [gitignore.io](https://gitignore.io/).

## Dev dependencies

There are a bunch of development tools recommended for any project to run linting, checking and testing tasks:

* `poetry add -D flake8` : adds PEP8 linting support. Requires a `.flake8` configuration file
* `poetry add -D flake8-commas` : adds check for trailing commas. It can be taken care of automatically by `add-trailing-comma`, for instance, but I prefer also checking
* `poetry add -D pylint` : adds linting support (including cyclomatic complexity checks). Requires a `.pylintrc` configuration file
* `poetry add -D pylint-quotes` : adds single/double quotes checking to `pylint`
* `poetry add -D isort` : adds import stance sorting
* `poetry add -D mypy` : adds static type checking
* `poetry add -D pytest tox pytest-cov` : adds unit testing, automation for test pipelines and test coverage
* `poetry add -D black` : adds autoformatting

**some kind of docstring linter would be nice to have (PEP257, PEP287, Google or Numpy formats), similarly to how PEP8 is checked by flake8 (or pylint with the correct settings)** Can this be done?


# Notes on CI/CD

The skeleton project includes support for CI/CD pipelines, based on the same toolbox that gets installed for purely local development (with `tox` as an entrypoint).
Using `tox`, testing is configured to act on an installed version of the package (at the _venv_ level) and dev/testing dependencies managed by `tox` itself (it would install `poetry` in each _venv_ for builing, `pytest` for testing, etc), potentially with different versions.

CI/CD activities are meant to run on third party cloud services via integration with the remote GIT repository.

Even though support is provided and enabled by default, it can be disabled in different ways without removing the support files:

* disable (or not enable) CI/CD activation for a given project, potentially based on rules or conditions.
* add `[ci skip]` or `[skip ci]` to the commit message. This affects the commit.
* add `-o ci.skip` (short for `--push-option=ci.skip`)to the push command. This affects all commits in the specific push.
* configure `ci.skip` for the project. This acts as a client side switch. This is achieved through the command line via `git config --add push.pushOption ci.skip` or via editing of `.git/config`

Reasons for disabling the CI/CD pipeline could be cost, being in the development phases of the integration (or additional rules) or any other workflow variation.
In my particular case, CI/CD execution makes more sense after spikes

The current GitLab integration supports:

* multi-version testing
* coverage reporting (directly and integrated with Codecov)
* test reporting



## [GitLab](https://docs.gitlab.com/)

This is currently the only CI/CD integration provided as the main repo platform from now on will be [GitLab](https://docs.gitlab.com/).

Integration relies on a `.gitlab-ci.yml` configuration file and ensuring the CI/CD settings are enabled both at the level of the GitLab project (this is the default) and locally (this is the default as well).

The current configuration is meant to run tests in a set of supported Python versions, execute tests and collect code coverage information across the different environments.

Test reports and coverage artifacts are uploaded to GitLab, to be consumed via `Analytics` > `Repository` or via pipeline and job details.

## [CircleCI](https://circleci.com/)

Local development of pipelines:


- Install circleci (`brew install circleci` or following instructions from [the documentation](https://circleci.com/docs/local-cli)) and configure with a CircleCI API token (generated via `User Settings` > `Personal API Tokens` as described [here](https://circleci.com/docs/api-developers-guide))

`circleci setup`
`circleci config validate`
`circleci local execute --job <job name>`

There is a bug on macOS affecting Docker Desktop 4.4.2 and circleci 0.1.21812 (at least) which and surfaces as an error message with `cannot enter cgroupv2`. The issue is [tracked here](https://github.com/CircleCI-Public/circleci-cli/issues/672). One workaround is to set `deprecatedCgroupv1` to `true` in Docker settings (`settings.json`, located in  `~/Library/Group\ Containers/group.com.docker/`) and restart Docker. Another workaround is to downgrade Docker (`4.2.0` seems to work) or circleci-cli.

## [Codecov](https://codecov.io/)

Codecov provides CI indepedent code coverage reporting. It is based on a code coverage report uploader that relies on a Project specific token (`CODECOV_TOKEN`) for authorisation.
It is not a CI service, but it supplements the CI/CD pipeline but allowing the configuration of success/failure criteria based on code coverage. It also provides a dedicated UX for coverage management.

Integration with:

* GitLab: requires Project configuration of `CODECOV_TOKEN` via `Settings` > `CI/CD` > `Variables`.
* CircleCI: requires Project configuration of `CODECOV_TOKEN` via `Project Settings` > `Environment Variables`.


# Notes on workflow

## Working on an existing project

When working on an existing project (either for the first time, or after cleansing via `git clean -xdf`), the _venv_ needs to be recreated. Easiest way to do so is to:

* `direnv allow` : if the project folder is fresh and was not already enabled
* `cd` into the project : this triggers _venv_ recreation via `direnv` and symlink creation
* `poetry install` : installs all dependencies in the workspace _venv_
* `hash -r` : clears the remembered locations for binaries, effectively ensuring newly installed commands are found first (**note**: there was an issue with `tox`)

## `poetry.lock`

Regarding `poetry.lock`, it is a good idea to commit it for tools or working environments (I was previously using Conda for these), because it guarantees version parity and it is not pinning dependencies' versions when building the package (`poetry build`).

## `README.rst`

I personally use Markdown instead of **reStructuredText**, so I used to the poetry default `README.rst` by a `README.md`, but versions greater than 1.2.0 started using Markdown for this file.

## Run console scripts

When working on the project extracted from source code, dependencies should be installed (the project is installed in editable mode):

	`poetry install [--no-root]`

The `--no-root` flag is used to avoid installing the project package itself.

If needed, execution of specific scripts without installation can be done via `poetry run <path to Python file with shellbang>` or `poetry run python <path to Python file>`. Here we reference the file directly and any project structure constraints are bypassed. This can be helpful when testing unstructured files with a set of Python requirements.

It is much better to run `poetry install` so that the correct console script entrypoint wrapper is created and installed into the _venv_, as this allows for proper testing of both the code and the package dependencies.

## Using a Poetry project from a different Python project

In order to use editable mode (to depend on a poetry managed package via pip as editable), pip 21.3 (which supports PEP-660) needs to be used. Otherwise the pyproject.toml `build-backend = "poetry.core.masonry.api"` configuration wouldn't have any impact.

PEP-660 hooks are implemented in Poetry since version 1.0.8.

## Linting

I found a good combination for linting is `pylint`, `flake8` and `mypy`. Installation and configuration of these dependencies allows for runing outside of IDEs if needed.

Linter configuration files are required and should be kept in sync as some checks overlap (line length, for instance).

When using IDEs:

* VS Code: can run both if enabled at the configuration level. I prefer including a `.vscode/settings.json` file with this configuration so that it is specific to a project.

  ```
  {
      "python.linting.enabled": true,
      "python.linting.mypyEnabled": true,
      "python.linting.pylintEnabled": true,
      "python.linting.flake8Enabled": true
  }
  ```

  Linting tasks are run when a file is opened and when it gets saved. Additionally, there is `Pylance` and `Python` extension support (if installed, which is required to enable linting).

* PyCharm: integrates PEP8 checks (with its own configuration) and `pylint` with the configuration from the workspace. Better run on demmand.

While IDE driven linting is useful when working on files one by one, the suggestion is to split work in a coding and a refactoring/linting phase. A complete separate task can be run on a terminal to execute linting on the whole code base.

## Testing

Normalising testing configuration increases consistency and simplifies usage so that all projects use the same structure for testing.

While testing can be done via CI/CD or terminal execution, it is convenient to use an IDE/editor particularly during the test development process.

When using IDEs:

* VS Code: including a `.vscode/settings.json` file provides out of the box integration for testing if the `Python` extension is installed.

  ```
  {
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
  }
  ```


## Code styling

There is support for [editorconfig](https://editorconfig.org/), which configuration (`.editorconfig`) can be used for checking or runtime fixing while saving within a supporting IDE or editor.

In addition to this, `isort` and `black` provide some autoformatting capabilities. As with linter configuration, some settings need to be kept in sync. This is particularly relevant for some settings that are not available in `black`, such as the indentation length or type.

While `editorconfig` is meant to help within the IDE, `isort` and `black` are triggered explicitely. This can be done with:

* command line invocation:
  * `isort <folder or file>` : sorts imports. Use `-c` to just check
  * `black <folder or file>` : autoformat. Use `--check` to just check
* use of pre-commit hooks (as we are using `git`)
* server-side

Overall, the coding style I chose is mostly compatible with that of `black` (more completely since making my mind about maintaining `E701`/`single-line-if-stmt` defaults)

## Pre-commit hooks

Including some degree of automation to run linting and auto-styling (or code style checks) before a commit is beneficial if the goal is to ensure consistency of committed code.

Using [pre-commit](https://pre-commit.com/), managing hooks for linters and stylers becomes simple. It requires the installation of `pre-commit` and the inclusion of a  `.pre-commit-config.yaml` file. This is supported as well by this workflow.

The use of pre-commit hooks is not enforced by the project structure, just supported by it and it depends on developer prefences. If used, it is convenient verifying the version of the repos for `isort`, `black` or other tools also installed in the _venv_ is the same as in `.pre-commit-config.yaml` so that results align regardless of the way the tools are triggered.

If pre-commit hooks are enabled and not allowing a commit, but a commit is desired anyway, then the `-n` (or `--no-verify`) flag can be passed to `git commit`.

Due to the opinionated nature of `black`, the configuration is supported but currently commented out.
The fact that better code writing practices can be promoted via linting (making code style violations visible) and `editorconfig` (for end of line/file there is autoformatting) makes this approach for `black` preferable.
Therefore `black` autoformatting won't run in pre-commit hooks.

## IDEs

IDEs are useful due to autocompletion, syntax highlighting, etc. They usually require the configuration of the Python interpreter to use.

### PyCharm

The following plugins must be installed to simplify usage:

*  `Pylint` : provides integration with `pylint`
*  `Poetry` : allows detection and simple creation of `poetry` _venv_ (including those autocreated by `direnv` with the setup described here)

When opening a Python file, if no interpreter is selected, PyCharm will try to find one and suggest using it. It is able to detect the Poetry Interpreter and configure it this way. If this is not desired (or if the plugin is not installed), any available interpreter could be used and configured.

The project `.idea` folder created can be ignored from a GIT point of view as it just links the project with the interpreter and settings that are not modified in this setup.

### VS Code

The following extensions must be installed to simplify usage:

* `Python` : brings Python support to VS Code and installs `Pylance` (the language server) as well as `Jupyter` (for Jupyter notebook support)

When opening a Python file, VS Code will try to detect the best interpreter. Amongst other scenarios, it can detect and activate `.venv` (Poetry local) and `.direnv` _venv_ setups.

It is recommended to start VS Code within a _venv_ for the purpose of better shell integration, but the `direnv` setup takes care of the _venv_ activation.


# TO-DO

* understand better the usage of virtual environments on poetry/direnv/tox AND handling of conda as well.

* add additional testing support as per some of the previous packages/best practices (tnarik_pymaven or kyss)

* learn well/better the difference between implicit packaging and otherwise, to make up my mind. And explain it here.

* Adding dependencies from GIT (with specific branches or tags) is possible via `poetry add git+ssh://git@github.com/username/packate.git#main` and similar URLs.
