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
    cmd:
        description:
            - Execute the given commands to get the package version number.
        required: true
        type: str
    regexp:
        description: Regexp to use for extracting only the version number.
        required: false
        type: str
    version:
        description: desired version for current installation.
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - ansi_colle.mods.cmp_pkg

author:
    - Chun Pan Yung
"""

EXAMPLES = r"""
# Pass
- name: Check package verison
  ansi_colle.mods.cmp_pkg:
    cmd: ansible --version
    regexp: '(^ansible\.\w+)(\s+)([0-9]+\.[0-9]+\.[0-9]+)'
    version: '2.14.1'

# fail the module
- name: Test failure of the module
  ansi_collle.mods.cmp_pkg:
    cmd: not_existing_commands
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
    type: int
    returned: always
    sample: 0
"""

from ansible.module_utils.basic import AnsibleModule  # noqa: E402


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type="str", required=True),
        new=dict(type="bool", required=False, default=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_message="", message="")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result["original_message"] = module.params["name"]
    result["message"] = "goodbye"

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params["new"]:
        result["changed"] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params["name"] == "fail me":
        module.fail_json(msg="You requested this to fail", **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
