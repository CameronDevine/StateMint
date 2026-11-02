#!/usr/bin/env bash
# Publish the web interface to statemint.stmartin.edu (GitHub Pages,
# StateMint/StateMint.github.io): build it, replace the Pages repository's
# contents with the build (keeping its CNAME), commit and push to master.
#
#   web/deploy-pages.sh            build, commit, and push
#   web/deploy-pages.sh --dry-run  build and commit in a temporary clone only
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="https://github.com/StateMint/StateMint.github.io.git"
make -C "$here" site
tmp="$(mktemp -d)"
git clone -q "$repo" "$tmp/pages"
cd "$tmp/pages"
git ls-files -z | grep -zv '^CNAME$' | xargs -0 git rm -q
rsync -a --exclude testdata "$here/build/" ./
git add -A
version="$(sed -n "s/^__version__ = '\(.*\)'/\1/p" "$here/../python/StateMint/__init__.py")"
git commit -q -m "Deploy StateMint $version web interface ($(git -C "$here" rev-parse --short HEAD))"
git --no-pager show --stat --oneline HEAD | tail -3
if [ "${1:-}" = "--dry-run" ]; then
	echo "Dry run: not pushed. The commit is in $tmp/pages"
else
	git push origin master
fi
