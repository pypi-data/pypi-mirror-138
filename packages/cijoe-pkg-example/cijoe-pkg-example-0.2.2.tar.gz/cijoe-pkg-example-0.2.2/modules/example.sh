#!/usr/bin/env bash
#
# CIJOE module the cijoe-pkg-example
#
# Functions:
#
# example::env    - Verify the environment definition
#
# REQUIRED variables:
#
# EXAMPLE_DUT     - Path to Device-Under-Test
# EXAMPLE_FOO     - Arbitrary variable containing a number
#
example.env() {
  if [[ ! -v EXAMPLE_DUT ]]; then
    cij.err "example.env: invalid EXAMPLE_DUT: '$EXAMPLE_DUT'"
    return 1
  fi

  if [[ ! -v EXAMPLE_FOO ]]; then
    cij.err "example.env: invalid EXAMPLE_FOO: '$EXAMPLE_FOO'"
    return 1
  fi

  return 0
}

