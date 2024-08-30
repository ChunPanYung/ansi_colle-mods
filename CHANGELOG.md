# Changelog

All notable changes to this project will be documented in this file.

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

## [1.1.2] - 2024-07-14                                                                    ▐│

### Features                                                                               ▐│

- Add alias to module parameter (version_arg to arg).                                      ▐│

### Fix                                                                                    ▐│

- Encode string in case command output is not utf-8.                                       ▐│

### Security                                                                               ▐│

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
