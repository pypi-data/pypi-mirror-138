#!/usr/bin/env bash
#
# Logs example_probe to file $CIJ_TEST_RES_ROOT/hook_example_probe.log
#
# on-enter: invoke 'date' on the test-target
# on-exit: invoke 'date' on the test-target
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test.enter

hook.example_probe_enter() {

  cij.cmd "date"

  return 0
}

hook.example_probe_enter
exit $?
