#!/usr/bin/env bash
# Copy a fixture somewhere the answer keys aren't reachable, and print the path.
#
# Fixtures live next to README.md, which names the defects seeded in each one. A reviewer
# following this skill explores the neighbourhood of its target, so pointed at a fixture in
# place it will read the answer key and score well for the wrong reason. That has already
# happened once, and the reviewer was honest enough to say so — don't rely on that.
#
#   usage:  eval $(./isolate.sh doc-code-drift-repo)   # sets FIXTURE
#           ./isolate.sh argued-philosophy-doc.md
set -euo pipefail

name="${1:?usage: isolate.sh <fixture-name>}"
src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/fixtures/$name"
[[ -e "$src" ]] || { echo "no such fixture: $name" >&2; exit 1; }

dest="$(mktemp -d "${TMPDIR:-/tmp}/editor-fixture-XXXXXX")"
cp -r "$src" "$dest/"
echo "$dest/$name"
