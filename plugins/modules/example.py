#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""

import shlex  # noqa: E402
from ansible.module_utils.basic import AnsibleModule  # noqa: E402


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type="str", required=True, aliases=["command_name"]),
        version=dict(type="str", required=True, aliases=["desired_version"]),
        regexp=dict(type="str", default="[0-9]+.[0-9]+.[0-9]+"),
        index=dict(type="int", default=0),
    )

    result = dict(message="", rc=None, version_list=None)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    name = module.params["name"]

    args: list = shlex.split(name)
    # It will only take 1 command_name.
    if len(args) != 1:
        module.fail_json(msg="More than 1 command name is given.", **result)

    # Append '--version' to args
    args.append("--version")

    rc, stdout, stderr = module.run_command(args)
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

    name = module.params["name"]

    args: list = shlex.split(name)
    # It will only take 1 command_name.
    if len(args) != 1:
        module.fail_json(msg="More than 1 command name is given.", **result)

    # Append '--version' to args
    args.append("--version")

    # Execute command regardless whether is it check mode or not.
    # This module should be change system.
    rc, stdout, stderr = module.run_command(args)
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result["original_message"] = module.params["name"]
    result["message"] = "goodbye"

    # early return if error
    if rc == -1:
        result["rc"] = -2
        module.fail_json(msg="Version cannot be compared.", **result)

    # Return list of version after re.findall() function
    result["version_list"] = re.findall(module.params["regexp"], stdout)
    # Get only selected version
    index: int = module.params["index"]
    installed_version = result["version_list"][index]
    desired_version = module.params["version"]

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
