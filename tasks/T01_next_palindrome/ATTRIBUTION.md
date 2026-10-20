# Attribution

This task adapts `next_palindrome` from QuixBugs.

- Source: https://github.com/jkoppel/QuixBugs
- Source file: `python_programs/next_palindrome.py`
- Commit: `4257f44b0ff1181dedaedee6a447e133219fcebf`
- License: MIT, see `LICENSE`

Modifications: wrapped the function in the `digitkit` package, added `is_palindrome` and `next_palindrome_int`, added digit validation, conversion, mirroring and reporting helpers, rewrote the target and regression tests, removed the original docstring example, and injected no additional bug beyond the QuixBugs buggy version.
