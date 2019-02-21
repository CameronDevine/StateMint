# Contributing

We welcome contributions in the form of bug reports, bug fixes, improvements to the documentation, ideas for enhancements, or the enhancements themselves!

You can find a [list of current issues](https://github.com/CameronDevine/StateMint/issues) in the project's GitHub repository. Feel free to tackle any existing bugs or enhancement ideas by submitting a [pull request](https://github.com/CameronDevine/StateMint/pulls). Some issues may be marked as `beginner-friendly`. These issues are a great place to start working with StateMint, if you're new here.

## Bug Reports

* Please include a short (but detailed) code snippet or explanation for reproducing the problem. Attach or include a link to any input files that will be needed to reproduce the error.
* Explain the behavior you expected, and how what you got differed.
* Include the full text of any error messages that are printed on the screen or found in the browser console.

## Pull Requests

* If you're unfamiliar with Pull Requests, please take a look at the [GitHub documentation for them](https://help.github.com/articles/proposing-changes-to-a-project-with-pull-requests/).
* **Make sure the test suite passes** on your computer. To do this, run `python TestSuite.py` from the `python` directory, `make test` from the `web` directory, or run the `TestSuite.nb` notebook from the `mathematica` directory, depending on what code has been changed.
* _Always_ add tests and docs for your code.
* Please reference relevant GitHub issues in your commit messages using `#123`.
* Changes should be [PEP8](https://www.python.org/dev/peps/pep-0008/) and [PEP257](https://www.python.org/dev/peps/pep-0257/) compatible, although this project uses tabs instead of spaces.
* Keep style fixes to a separate commit to make your pull request more readable.
* Docstrings should follow the [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
* When you start working on a pull request, start by creating a new branch pointing at the latest commit on [GitHub master](https://github.com/CameronDevine/StateMint/tree/master).
* The copyright policy is detailed in the [`LICENSE`](https://github.com/CameronDevine/StateMint/blob/master/LICENSE).

## Meta

Thanks to the useful [contributing guide of thermostate](https://github.com/bryanwweber/thermostate/blob/master/CONTRIBUTING.md), which served as an inspiration and starting point for this guide.
