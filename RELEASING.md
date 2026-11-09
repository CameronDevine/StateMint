# Releasing StateMint

## Python package (PyPI)

1. Install the release tool from the repository root:
   `pip install -e "./python[release]"`. Date the entry in `CHANGELOG.md` and
   commit all pending changes.
2. Check: `cd python && pip install -e ".[test]" && pytest`, and
   `make check` (builds and runs `twine check`).
3. From the repository root, run `bump-my-version bump release` to promote
   the current development version to a final release (`3.0.0.dev0` to
   `3.0.0`). This updates `.bumpversion.toml`,
   `python/StateMint/__init__.py`, and `codemeta.json`, creates a commit,
   and creates an annotated `vX.Y.Z` tag. Preview without changing anything
   with `bump-my-version bump release --dry-run -v`.
   Push the commit and the specific tag: `git push && git push origin vX.Y.Z`.
   Pushing the tag triggers
   `.github/workflows/publish.yml` to build and upload to PyPI by trusted
   publishing. (Once only: a PyPI owner of StateMint adds this repository,
   workflow `publish.yml` and environment `pypi` as a trusted publisher.)
   Without trusted publishing: `cd python && make upload` with a PyPI token.
4. Publish a GitHub release from the tag. Zenodo archives each GitHub release
   if the repository's Zenodo
   integration is on (the concept DOI is 10.5281/zenodo.2633330).

Use `bump-my-version bump major`, `minor`, or `patch` to start the next
development version (for example, `3.0.0` to `3.0.1.dev0` with `patch`).
Use `bump-my-version bump dev` to increment the development suffix.
These commands also commit and tag; add `--no-tag` for development bumps
that should not create a publishable tag. Nothing is pushed automatically,
and bumps require a clean working tree. Changelog entries and dates remain
manual.

## Web interface

1. `make -C web site` builds `web/build/`, cache-busted by the package
   version and commit.
2. ricopic.one: copy it into the homepage repository's `statemint/site/`
   (`rsync -a --delete --exclude testdata web/build/ <homepage>/statemint/site/`),
   commit, and push `main` (pushing `main` deploys).
3. statemint.stmartin.edu (GitHub Pages, StateMint/StateMint.github.io):
   `web/deploy-pages.sh` builds the site, replaces that repository's
   contents with it (keeping its `CNAME`) and pushes; `--dry-run` stops
   before the push. The site no longer needs AWS.
