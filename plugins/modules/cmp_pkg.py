# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cmp_pkg

short_description: Given a package version, it will compare to installed
version.

version_added: "1.0.2"

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
        default: '\d+\.\d+\.\d+'
        type: str
    version:
        description: desired version for current installation.
        aliases: [ desired_version ]
        required: true
        type: str
    arg:
        description:
            - argument for getting commnad version number, default is '--version'.
            - example: if the command is 'bash', it will be 'bash --version'.
        aliases: [ version_arg ]
        default: '--version'
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
    command_name: ansible
    desired_version: '2.14.1'

- name: Get the second version number after executing command with regexp.
  ansi_colle.mods.cmp_pkg:
    name: ansible
    index: 1
    arg: '--version'
    desired_version: 3.12.1

# fail the module
- name: Test failure of the module
  ansi_colle.mods.cmp_pkg:
    name: not_existing_commands
"""

RETURN = r"""
msg:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'Desired version matches the installed version.'
rc:
    description:
        - return 2 if no desired version is installed.
        - return 1 if desired version is greater than installed version.
        - return 0 if desired version is equal to installed version.
        - return -1 if desired version is less than installed version.
        - return -2 if it cannot be compared.
    type: int
    returned: always
    sample: 0
version_list:
    description: List of version numbers returned after running cmd with regexp.
    type: list(str)
    returned: always
    sample: ['2.14.1', '3.11.9', '3.1.12']
"""

import shlex  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402

from ansible.module_utils.basic import AnsibleModule  # noqa: E402
from ansible.module_utils.compat.version import LooseVersion  # noqa: E402


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type="str", required=True, aliases=["command_name"]),
        version=dict(type="str", required=True, aliases=["desired_version"]),
        regexp=dict(type="str", default=r"\d+\.\d+\.\d+"),
        arg=dict(type="str", default=r"--version", aliases=["version_arg"]),
        index=dict(type="int", default=0),
    )

    result = dict(msg="", rc=None, failed=False)

    module = AnsibleModule(argument_spec=module_args)

    name = module.params["name"]

    args: list = shlex.split(name)
    # It will only take 1 command_name.
    if len(args) != 1:
        result["rc"] = -2
        result["msg"] = "'name' parameter should only be given 1 command."
        module.fail_json(**result)

    # Early return if command does not exist
    if not shutil.which(args[0]):
        result["rc"] = 2
        result["msg"] = "No desired version is installed."
        module.exit_json(**result)

    # It will only take 1 command line argument.
    version_arg: list = shlex.split(module.params["arg"])
    if len(version_arg) != 1:
        result["rc"] = -2
        result["msg"] = "'arg' parameter should only be given 1 command."
        module.fail_json(**result)

    # Append '--version' to args and get command version
    args.append(version_arg[0])
    rc, stdout, stderr = module.run_command(args)

    # Return list of version after re.findall() function
    regexp: str = module.params["regexp"]

    try:
        result["version_list"] = re.findall(regexp, stdout)
    except TypeError:
        module.fail_json(msg="Error getting version from command.", **result)

    # Get only selected version
    index: int = module.params["index"]
    installed_version = result["version_list"][index]
    # Make sure desired_version followed regexp given
    try:
        desired_version = re.search(regexp, module.params["version"]).group(0)
    except AttributeError:
        # desired_version: str = module.params["version"]
        module.fail_json(msg="Error verifying desired version", **result)

    if desired_version < LooseVersion(installed_version):
        result["msg"] = (
            "Desired version({}) is less than installed version({}).".format(
                desired_version, installed_version
            )
        )
        result["rc"] = -1
    elif desired_version > LooseVersion(installed_version):
        result["msg"] = (
            "Desired version({}) is greater than installed version({}).".format(
                desired_version, installed_version
            )
        )
        result["rc"] = 1
    else:
        result["msg"] = "Desired version({}) matches the installed version({}).".format(
            desired_version, installed_version
        )
        result["rc"] = 0

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
