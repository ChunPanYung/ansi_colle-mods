# Ansible Collection - ansi_colle.mods

This collection only contains plugins.
Playbooks directory only contains testing for plugins created.

## Quick Start

```bash
export ANSIBLE_CALLBACK_RESULT_FORMAT=yaml


ansible-galaxy collection install \
  git+https://github.com/ChunPanYung/ansi_colle-mods.git

# Run this to update every time
ansible-playbook ansi_colle.mods.install

# Run this after update, it will ask you sudo password
ansible-playbook ansi_colle.mods.site --connection=local \
  --inventory 127.0.0.1, --ask-become-pass --verbose
```

## Initialize virtual environment

This project use `uv` for Virtual Environment setup.

`uv sync`: Init and sync project's environment according to `pyproject.toml` file.
`source .venv/bin/activate`: Activate bash venv.

## Links

[Documentation Site](https://chunpanyung.github.io/ansi_colle-mods/)
