# Changelog

All notable changes to this project will be documented in this file.

## [1.3.3] - 2025-11-28

### 🚀 Features

- Create `taskfile.dist.yml` for quick CLI.
- Update pre-commit repos.
- Use `uv` instead of `pdm`.

### 🐛 Bug Fixes

- `winget` now accept agreement by default.

### 📚 Documentation

- Add quick start section.
- Add `uv` tutorial.

## [1.3.2] - 2024-09-03

### Documentation

- Add attributes to module.
- Create script cmd for pdm.
- Update documentation for ansi_colle.mods.cmp_pkg module.
- Update readme file and remove repeated dependencies.
- [**breaking**] Remove unused dependencies and build.

### Features

- Support check mode.
- Support diff mode.

### Refactor

- Reduce code complexity.

## [1.3.1] - 2024-09-01

### Documentation

- Ansible requirements.yml file.
- Add pyproject.toml lint and doc package.
- Update pre-commit config file.
- Fix module documentation.

### Features

- Validate ansible code before merging.
- Github action to create static page.

### Fix

- Correct cmp_pkg test playbook.
- Ansible-lint error.

### Refactor

- Reduce code complexity.

## [1.3.0] - 2024-08-31

### Documentation

- Fix grammar.

### Features

- [**breaking**] Change rc, use match instead of search.

### Refactor

- Remove version_args parameter.

### Styling

- Configure markdownlint.
- Correct collection name.
- Clean up linting error.

## [1.2.0] - 2024-08-30

### Bug Fixes

- Remove shebang.
- Pandas library
- Remove unused parameter.
- Catch failure to import if sheet_name does not exist.

### Documentation

- Ignore .pdm-python file.
- Ignore pdm.lock file.
- Require openpyxl for xlsx file read and write.

### Features

- Module for exporting ansible data to xlsx file.
- Playbook for testing plugins.

### Styling

- Use pdm instead of poetry.

## [1.1.3] - 2024-07-14

### Bug Fixes

- Use try except to catch error.

## [1.1.2] - 2024-07-14

### Features

- Add alias to module parameter (version_arg to arg).

### Fix

- Encode string in case command output is not utf-8.

### Security

- Ensure module only accepts one command line argument.

## [1.1.1] - 2024-05-15

### Features

- Ping test for both windows and linux.

## [1.1.0] - 2024-04-04

### Features

- Filter `desired_version` with regexp.
- Allow user to specify command arg.

### Refactor

- Save dictionary value to variable.

### Testing

- Test case for new parameter for `cmp_pkg` module.

## [1.0.0] - 2024-03-22

### Features

- Create module for `winget_cmd`.
- Create module for `cmp_pkg`.
