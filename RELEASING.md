# Releasing StateMint

## Python package (PyPI)

1. Set the version in `python/StateMint/__init__.py` (`__version__`) and
   `codemeta.json`, and date the entry in `CHANGELOG.md`.
2. Check: `cd python && pip install -e ".[test]" && pytest`, and
   `make check` (builds and runs `twine check`).
3. Commit, tag `vX.Y.Z`, push, and publish a GitHub release from the tag.
   `.github/workflows/publish.yml` builds and uploads to PyPI by trusted
   publishing. (Once only: a PyPI owner of StateMint adds this repository,
   workflow `publish.yml` and environment `pypi` as a trusted publisher.)
   Without trusted publishing: `cd python && make upload` with a PyPI token.
4. Zenodo archives each GitHub release if the repository's Zenodo
   integration is on (the concept DOI is 10.5281/zenodo.2633330).

## Web interface

1. `make -C web site` builds `web/build/`, cache-busted by the package
   version and commit.
2. ricopic.one: copy it into the homepage repository's `statemint/site/`
   (`rsync -a --delete --exclude testdata web/build/ <homepage>/statemint/site/`),
   commit, and push `main` (pushing `main` deploys).
3. statemint.stmartin.edu (GitHub Pages, StateMint/StateMint.github.io):
   replace that repository's contents with `web/build/`, keeping its
   `CNAME`, and push. The site no longer needs AWS.
