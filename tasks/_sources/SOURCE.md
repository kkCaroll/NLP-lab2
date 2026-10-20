# Source snapshots

These snapshots are used only to construct tasks. They are not executed during inventory.

| Source | Path | Version or commit | License | Retrieval |
|---|---|---|---|---|
| QuixBugs | `QuixBugs/` | `4257f44b0ff1181dedaedee6a447e133219fcebf` | MIT | `git clone --depth 1 https://github.com/jkoppel/QuixBugs.git` |
| BigCodeBench | `bigcodebench/bigcodebench-v0.1.4.parquet` | v0.1.4, 1140 tasks | Apache-2.0 | HuggingFace mirror `bigcode/bigcodebench` |
| HumanEval | `humaneval/HumanEval.jsonl.gz` | 164 tasks | MIT | `https://github.com/openai/human-eval` |

The nested QuixBugs `.git` directory was removed after cloning to avoid a nested repository. The commit hash above identifies the snapshot.

Inventory command:

```bash
python -I harness/inventory_sources.py
```

Outputs:

- `PLAN/03_candidate_pool.json`
- `PLAN/03_candidate_pool.md`
