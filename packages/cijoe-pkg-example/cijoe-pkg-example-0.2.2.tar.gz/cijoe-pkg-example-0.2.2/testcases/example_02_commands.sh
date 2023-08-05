#!/usr/bin/env bash
#
# testcase-example: executing commands
#
# This is an example of the minimal boiler-plate for creating a testcase, note that this comment
# section is required, a short-description and a long-description *should* always be provided,
# describing what a testcase does. When you generate a report, then these comment sections are
# provided for description of the testcase, along with the actual testscript.
#
# In the first five lines of the script itself, the actual required code it:
#
# 1. Define a test-name by setting CIJ_TEST_NAME to the name of the Bash-script
# 2. Export the test-name
# 3. This provides a path for 'shellcheck'. It is required for the 'selftest' invoking 'shellcheck'
# 4. Source in CIJOE; this is includes cijoe and an installed Bash modules
# 5. 'test.enter': verifies that the environment has what is needed
#
# After the initial boiler-plate, then the actual testcase body begins. Here we invoke a command
# and based on the command return-code signal test.fail / test.pass
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test.enter

if ! cij.cmd "hostname"; then
  test.fail
fi

test.pass
