#!/bin/sh

set -eu

SCRIPT="scripts/verify-platform-adapters.sh"

if [ ! -x "$SCRIPT" ]; then
  echo "missing executable $SCRIPT" >&2
  exit 1
fi

"$SCRIPT"
