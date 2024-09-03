# Ansible Collection - ansi_colle.mods

This collection only contains plugins.
Playbooks directory only contains testing for plugins created.

## Requirements

There are 2 sets of dependencies: python and ansible

### Python

Check [pyproject.toml](./pyproject.toml) for dependencies.

if you use [PDM](https://pdm-project.org):

```bash
#!/bin/bash
pdm venv create
$(pdm venv activate)
pdm use  # Pick the location of venv
pdm install --production
```

### Ansible

Execute one of following:

Install from file: `$ ansible-galaxy install -r requirements.yml`
Install from CLI: `$ ansible-galaxy collection install git+https://github.com/ChunPanYung/ansi_colle-mods.git`

## Links

[Documentation Site](https://chunpanyung.github.io/ansi_colle-mods/)
