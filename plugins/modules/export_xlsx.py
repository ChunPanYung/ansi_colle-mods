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
  - Linux only.
  - Requires pandas to be installed (pip install pandas).
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
author:
  - Chun Pan Yung
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
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        data=dict(type='list', required=True, elements='dict'),
        path=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        rc=0
    )

    module = AnsibleModule(argument_spec=module_args)

    print(module.params['data'])
    path: str = module.params['path']
    try:
        df = pd.DataFrame(module.params['data'])
        df.to_excel(path, sheet_name='Default')
    except:
        result['rc'] = 1
        module.fail_json(msg='Unable to convert data into DataFrame type from pandas library', **result)





    result['path'] = path
    module.exit_json(**result)  # Success return

def main():
    run_module()

if __name__ == '__main__':
    main()




