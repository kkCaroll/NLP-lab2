# Attribution

This task adapts the correct binary search from QuixBugs `find_first_in_sorted` and adds original duplicate detection utilities.

- Source: https://github.com/jkoppel/QuixBugs
- Source file: `correct_python_programs/find_first_in_sorted.py`
- Commit: `4257f44b0ff1181dedaedee6a447e133219fcebf`
- License: MIT, see `LICENSE`

Modifications: adapted the binary search into `seqkit.search.find_first_in_sorted`, added duplicate detection, statistics, run analysis and reporting modules, rewrote the target and regression tests, and injected a scan-order bug in duplicate selection.
