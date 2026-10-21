# Attribution

This task is original work created for this experiment. It does not adapt code from an external benchmark.

The package computes page counts, resolves requested pages, slices fixed size windows, builds page chunks and renders progress text. The injected defect lets the shared interval helper admit one value above the upper bound, so both paging and window slicing handle requests beyond the end incorrectly.
