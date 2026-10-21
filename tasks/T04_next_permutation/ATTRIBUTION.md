# Attribution

This task adapts `next_permutation` from QuixBugs.

- Source: https://github.com/jkoppel/QuixBugs
- Source file: `python_programs/next_permutation.py`
- Commit: `4257f44b0ff1181dedaedee6a447e133219fcebf`
- License: MIT, see `LICENSE`

Modifications: wrapped the function in the `seqkit` package, added sequence comparison, inversion counting, suffix rotation and formatting helpers, rewrote the target and regression tests, removed the original docstring example, and replaced the original defect with a one-line suffix reversal start error.
