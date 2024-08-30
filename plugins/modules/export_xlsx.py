# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ans_colle.mods.export_xlsx
version_added: "1.1.4"
short_description: Export list of dictionary from Ansible to Microsoft Excel format.
description:
  - It will compile data from a list of dictionary toi Microsoft .xlsx file format using pandas.
  - It will read file from path, and compare it to data wanting to be exported.
options:
  data:
    description:
      - list of dictionary where key will be the first row of excel sheet, and data will be the value.
    type: list(dict)
    required: yes
  path:
    description:
      - Path to the file it will be exported to.
    type: path
  sheet_name:
    description:
      - Name of worksheet.
    aliases: [ name ]
    default: 'Sheet1'
    type: str
author:
  - Chun Pan Yung
requirements:
  - pandas(python module)
  - openpyxl(python module)
'''

EXAMPLES = r'''
- name: Give file and path for it to export.
  ansi_colle.mods.export_xlsx:
    path: /tmp/file.xlsx
    data:
      - name: debian
        version: 12
        location: USA
      - name: windows_server
        version: 2010
        location: Canada
      - name: redhat
        version: 9.7
        location: UK
'''

RETURN = r'''
changed:
  description: Whether it has either sucessfully export as .xlsx file format.
  returned: always
  type: bool
  sample: true
rc:
  description: Return code indicating whether it export data sucessfully or not.
  returned: always
  type: int
  sample: 0
path:
  description: file path of exported data.
  returned: always
  type: str
  sample: /tmp/file.xlsx
'''

import pandas as pd
from os.path import splitext
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        data=dict(type='list', required=True, elements='dict'),
        path=dict(type='str', required=True),
        sheet_name=dict(type='str', default='Sheet1', aliases=['name'])
    )

    result = dict(
        changed=False,
        path='',
        rc=0
    )

    module = AnsibleModule(argument_spec=module_args)

    # Early return if file does not ends with .xlsx
    path: str = module.params['path']
    _, file_extension = splitext(path)
    if file_extension != '.xlsx':
        module.fail_json(msg="This module only supports .xlsx file type.")

    # Get sheet_name from parameters
    sheet_name: str = module.params['sheet_name']

    # Read data from file
    from_excel: pd.DataFrame = pd.DataFrame()
    try:
        from_excel = pd.read_excel(path, sheet_name=sheet_name)
    except FileNotFoundError as e:
        module.fail_json(msg=f"File not found: {e}")
    except IsADirectoryError as e:
        module.fail_json(msg=f"Path given is a directory: {e}")
    except ValueError as e:
        module.fail_json(msg=f"Path file type cannot be imported: {e}")

    # Convert Ansible Data to DataFrame
    ansible_data: pd.DataFrame = pd.DataFrame()
    try:
        ansible_data = pd.DataFrame(module.params['data'])
        ansible_data.to_excel(path, sheet_name='Default')
    except:
        result['rc'] = 1
        module.fail_json(msg='Unable to convert data into DataFrame type', **result)

    # if excel data compare to ansible_data return non-empty (meaning there
    # is difference in data), overwrite file.
    if not from_excel.compare(ansible_data).empty:
        ansible_data.to_excel(path, sheet_name=sheet_name)
        result['changed'] = True


    result['path'] = path
    module.exit_json(**result)  # Success return

def main():
    run_module()

if __name__ == '__main__':
    main()




