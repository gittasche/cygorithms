#!/bin/bash

set -e
set -x

COMMIT_MSG = $(git log --no-merges -1 --oneline)

if [[ "$COMMIT_MSG" =~ \[build\] ||
      "$COMMIT_MSG" =~ \[ci\] ]]; then
    echo "::set-output name=build::true"
fi