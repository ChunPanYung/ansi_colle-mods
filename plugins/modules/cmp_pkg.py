#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cmp_pkg

short_description: Given a package version, it will compare to installed
version.

version_added: "1.0.1"

description: This is my longer description explaining my test module.

options:
    name:
        description:
            - command name to check version with.
            - It will append '--version' at the end before running given command.
        aliases: [ command_name ]
        required: true
        type: list
    regexp:
        description: Regexp to use for extracting only the version number.
        default: '[0-9]+.[0-9]+.[0-9]+'
        type: str
    version:
        description: desired version for current installation.
        aliases: [ desired_version ]
        required: true
        type: str
    index:
        description:
            - Which version number selected from after running command.
            - if more than 1 matched version are returned.
            - Default is 0.
            - First occurence is 0, second is 1, and third is 2 etc.
        default: 0
        type: int

extends_documentation_fragment:
    - ansi_colle.mods.cmp_pkg

author:
    - Chun Pan Yung
"""

EXAMPLES = r"""
# Pass
- name: Check package verison
  ansi_colle.mods.cmp_pkg:
    name: ansible --version
    regexp: '[0-9]+.[0-9]+.[0-9]+'
    version: '2.14.1'

- name: Get the second version number after executing command with regexp.
  ansi_colle.mods.cmp_pkg:
    name: ansible --version
    index: 1
    desired_version: 3.12.1

# fail the module
- name: Test failure of the module
  ansi_colle.mods.cmp_pkg:
    name: not_existing_commands
"""

RETURN = r"""
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'The installed version matched the desired version.'
rc:
    description:
        - return 1 if desired 'version' is greater than installed version.
        - return 0 if desired 'version' is equal to installed version.
        - return -1 if desired 'version' is less than installed version.
        - return -2 if it cannot be compared.
    type: int
    returned: always
    sample: 0
version_list:
    description: List of version numbers returned after running cmd with regexp.
    type: list(str)
    returned: always
    sample: ['2.14.1', '3.11.9', '3.1.12']
version_selected:
    description:
        - version selected from version_list for comparison with given version.
    returned: always
    type: str
    sample: '2.14.1'

"""

import shlex  # noqa: E402

from ansible.module_utils.basic import AnsibleModule  # noqa: E402
from ansible.module_utils.common.text.converters import (  # noqa: E402
    to_native,  # noqa: E402
    to_bytes,  # noqa: E402
    to_text,  # noqa: E402
)  # noqa: E402
from ansible.module_utils.common.collections import is_iterable  # noqa: E402


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type="str, required=True, aliases=['command_name']),
        version=dict(type="str", required=True, aliases=["desired_version"]),
        regexp=dict(type="str", default="[0-9]+.[0-9]+.[0-9]+"),
        index=dict(type="int", default=0),
    )

    result = dict(
        changed=False,
        message="",
        rc=None,
        version_list=None,
        version_selected=None,
        start=None,
        end=None,
        stdout="",
        stderr="",
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    name = module.params["name"]
    # Make sure 'name' is not empty.
    if name.strip() == "":
        result["message"] = "no command name is given."
        module.fail_json(**result)

    args: list = shlex.split(name)
    # It will only take 1 command_name.
    if len(args) != 1:
        result["message"] = "More than 1 command name is given."
        module.fail_json(**result)

    # Append '--version' to args
    args.append("--version")

    # Execute command regardless whether is it check mode or not.
    # This module should be change system.
    result['start'] = datetime.datetime.now()
    result["rc"], result["stdout"], result["stderr"] = module.run_command(args)

    # TODO: need to filter the result

    result['end'] = datetime.datetime.now()

    # Convert to text for jsonization and usability
    if result['start'] is not None and result['end'] is not None:
        # Convert to string
        result['delta'] = to_text(result['end'] - result['start'])
        result['end'] = to_text(result['end'])
        result['start'] = to_text(result['start'])

    if result['rc'] == -2:
        result['message'] == 'Version cannot be compared.'
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
