#!/usr/bin/env python3

# Copyright: (c) 2021, Yanick Champoux <yanick@babyl.ca>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: command_info

short_description: Retrieves information about a given command.

version_added: "1.0.0"

description: Retrieves the location and version of a command on the remote machine.

options:
    command_name:
        description: Target command.
        required: true
        type: str

    version_args:
        description: Arguments passed to the command to print the version string.
        required: false
        default: --version
        type: str

    version_regex:
        description: Regular expression to capture the version from the command output.
        default: v?(\d+\.\d+\.\d+[^\n ]*)
        required: false
        type: str

    target_version:
        description: Target version to compare against.
        required: false
        type: str

author:
    - Yanick Champoux (@yanick)
"""

EXAMPLES = r"""
- name: perl info
  command_info:
    command_name: perl
    target_version: 5.32.0

# get the info on ls
- name: ls info
  command_info:
    command_name: ls
    version_regex: '(\d+\.d+)'
    target_version: 8.30
"""

RETURN = r"""
needs_upgrade:
    description: Wether the new version of the command needs to be installed.
    type: bool
    sample: True

installed_version:
    description: Version string of the currently installed command.
    type: str
    sample: '1.2.3'

location:
    description: Path where the command was found.
    type: str
    sample: '/usr/local/bin/ls'
"""

from ansible.module_utils.basic import AnsibleModule
import subprocess
import re
from cmp_version import cmp_version


def run_module():
    module_args = dict(
        command_name=dict(type="str", required=True),
        version_args=dict(default="--version"),
        version_regex=dict(default=r"v?(\d+\.\d+\.\d+[^\n ]*)"),
        target_version=dict(default=None, type="str"),
    )

    result = dict(
        changed=False,
        needs_upgrade=False,
        installed_version=None,
        location=None,
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    cmd_location = subprocess.run(
        [
            "which",
            module.params["command_name"],
        ],
        text=True,
        capture_output=True,
    )

    result["location"] = cmd_location.stdout.rstrip()

    if result["location"]:
        cmd_output = subprocess.run(
            [module.params["command_name"], module.params["version_args"]],
            capture_output=True,
            text=True,
        )

        result["command_stdout"] = cmd_output.stdout
        result["command_stderr"] = cmd_output.stderr

        m = re.search(
            module.params["version_regex"],
            result["command_stdout"] + result["command_stderr"],
        )

        if m:
            result["installed_version"] = m.group(1)

    if "target_version" in module.params:
        result["needs_upgrade"] = 1 == cmp_version(
            module.params["target_version"], result["installed_version"]
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
