# Attribution

This task adapts the email-address regular expression from BigCodeBench task 761.

- Source: https://github.com/bigcode-project/bigcodebench
- Source task: `BigCodeBench/761`
- Version: v0.1.4
- License: Apache-2.0, see `LICENSE`

Modifications: extracted the email matching behavior into the `mailscan` package, added address normalization and domain reporting helpers, rewrote the target and regression tests, removed the JSON processing context, and injected a missing plus sign in the local-part character class.
