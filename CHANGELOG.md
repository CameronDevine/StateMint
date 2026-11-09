# Changelog

## 3.0.0 (unreleased)

### Python package
- **Output expressions.** Outputs may be any expression in the system's
  variables, e.g. `FK + FB`, `m*vm` or `vm'`. Before, every output was parsed
  as `name(t)`, so `FK + FB` became `FK + FB(t)` and the `FK` term was silently
  dropped from C and D.
- **Empty lists and blank entries** are ignored, so a system with no "other
  elemental equations" works. `StateMint.split_entries` splits a text field at
  new lines and at commas outside parentheses.
- **Safer, clearer parsing.** Input text may contain only names, numbers,
  `+ - * / ^ ( ) , = '` and spaces (no attribute access, dunders or keywords),
  so equations can't run arbitrary Python. Every malformed input raises
  `StateMintError` with a message naming the equation and the problem.
- `^` means a power; `abs`, `Min`, `Max`, `Heaviside` and `pi` are available.
- **`I` is an ordinary name** (an inertance or a current), no longer the
  imaginary unit.
- **Elimination.** The variables that are neither states nor inputs are
  eliminated by solving the equations simultaneously, as a linear system in
  those variables (Rowell and Wormley 5.5), with the original substitution
  method as the fallback for equations nonlinear in them. `Solve(...,
  method=...)` selects one. Coupled state derivatives, derivatives of primary
  variables and algebraic loops of any length are handled; singular or
  underdetermined systems raise an error instead of hanging or returning a
  wrong model; leftover variables are named.
- **Transfer functions** are computed entry by entry as ratios of determinants
  and cancelled, so each entry is one fraction (and the 6-state hydroelectric dam takes
  seconds, not minutes). `TF` is `None` for nonlinear models.
- New result attributes: `Parameters`, `Linear`, `Nonstandard`.
- New module `StateMint.web`: formats a model as LaTeX, MATLAB, Mathematica
  and Python for the web interface (formerly the AWS Lambda handler).
- Rowell and Wormley Example 5.13 (nonlinear fluid system) now solves.
- Raw docstrings: no `SyntaxWarning` on Python 3.12+.
- **Breaking:** Python 3.10+ and SymPy 1.10+; `to_numpy.matrix` is removed
  (use `to_numpy.array`); `I` is no longer the imaginary unit.
- Packaging with `pyproject.toml`; tests with pytest on GitHub Actions
  (Python 3.10-3.14, SymPy 1.10-latest); docs build on Read the Docs again.
- Regression tests for 38 worked models in the System Dynamics notes.

### Web interface
- **Runs in the browser.** Pyodide and SymPy run StateMint in a Web Worker,
  replacing the AWS API Gateway + Lambda (on the retired `python3.8` runtime).
  The site is static and can be hosted anywhere.
- Empty fields (HTTP 400 "Failed" before), trailing commas (#11) and the
  share button (#12) work; errors explain what is wrong.
- Results list the model's parameters; the x' form shows the F term.
- Saved systems use localStorage instead of cookies (migrated automatically).
- Google Analytics removed; Bootstrap 3.4.1; no IE polyfills.

### Tutorial
- Through- and across-variables were swapped; fixed.
- Notation aligned with the System Dynamics notes (T for torque, K_r, B_r,
  edge/branch/link, tension positive).
- The example's pipe had the wrong sign; corrected.
- Documents the input syntax, the results and the Python package.
- GitHub renders its math natively (no more codecogs images).

## 2.1.1 (2021-04-16)
- Lambda moved to Python 3.8.
