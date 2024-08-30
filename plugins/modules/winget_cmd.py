#!/usr/bin/env python
# -*- coding: utf-8 -*-
DOCUMENTATION = r'''
---
module: winget_cmd
short_description: Execute winget command to either install or remova package.
description:
  - Assume ansible_user has administrator privilege.
  - Windows only.
options:
  state:
    description:
      - Whether to install (V(present)), or remove (V(absent)) a package.
      - Default is V(present).
    choices: ['absent', 'present']
    type: str
  id:
    description:
      - Install package by its ID.
      - Must be exact matched.
    type: str
'''

EXAMPLES = r'''
- name: Install firefox, ID must be exact matched
  ansi_colle.mods.winget_cmd:
    id: Mozilla.Firefox

- name: Remove 7-Zip
  ansi_colle.mods.winget_cmd:
    id: 7zip.7zip
    state: absent
'''

RETURN = r'''
changed:
  description: Whether it has either sucessfully installed or uninstalled a package.
  returned: always
  type: bool
  sample: true
rc:
  description: Return code after winget command execution.
  returned: always
  type: int
  sample: 0
output:
  description: Output after execute winget command.
  returned: return code is not understood.
  type: str
  sample: 'Unrecognized command.'
'''
