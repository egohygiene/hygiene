# Complete contract regression gate

Run the same entry point locally and in the Pages workflow's read-only
`checks` job:

```sh
python3 -I tools/check_contracts.py
# Or, with the existing Task runner:
task check
```

Use Python 3.11 or newer and Git. The gate has no third-party Python dependency,
performs no installation or network acquisition, and invokes the existing
reference CLIs. Those scripts use `-E` rather than isolated-script mode because
some import neighboring tools. The gate itself and unittest discovery use `-I`.

The job runs for every pull request and default-branch push, with no path or
matrix selection that excludes catalog, schema, tool, fixture or generated-view
changes. Checkout and diagnostic upload use the existing immutable Action pins;
checkout does not retain credentials and the job has only `contents: read`.

## Coverage and results

Unittest discovery executes every current `tests/test_*.py` module, including
the 194-test predecessor suite and later regression additions. Its actual
run/failure/error/skip/expected-failure counts are printed and recorded. Empty
or missing unittest execution fails even if Python exits zero. Explicit skips
remain visible; a passing process does not mean that skipped cases ran.

The remaining checks call the existing catalog, context, continuity,
Agent-Ready Web, dependency-boundary, Intelligence, presentation, public-site
surface, ADR fixture and release-policy tools. They also check the catalog and
boundary Markdown views, each checked-in generated context, the generated
context TOML contract, and applicability of the preserved ADR-0001 review patch
without applying it. Generated context checks retain the artifact's recorded
source revision; they check regeneration from current canonical inputs, not
authentication of that historical revision.

Every check reports its own result. Later checks continue after an earlier
failure, while any failed check keeps the aggregate nonzero. A planning failure
or interruption leaves `complete: false`. `complete: true` means all planned
checks returned; the separate `status` can still be `failed`.

Reports and logs go to ignored `.cache/contract-regression/`, or the explicitly
selected `--report-directory`. `result.json` records the Git revision and dirty
state when Git is available, Python version, discovered modules, actual commands,
exit/timeout outcomes and log truncation. Up to 256 KiB of diagnostics per
command are retained, including its final output. Output is temporarily spooled
while each command runs; this retention limit is not a live disk quota. Commands
have a 60-second deadline, with owned process-group termination on POSIX; the
workflow additionally has a ten-minute job limit. Incremental reports and bounded
logs are uploaded on success or failure with seven-day retention. A canceled
runner may prevent that upload; an artifact's existence alone supplies no pass.

The regression controls use disposable source copies and the actual gate to
exercise new test discovery, explicit skips, failing/empty suites, invalid
catalog/profile input, stale generated output and bounded retained diagnostics.
They exclude their own test module from each nested copy to prevent recursion.
No negative control changes tracked canonical input.

## Separate acceptance gates

This is a reference-contract regression result. It inherits the current
reference tools' supported grammar and limitations; it does not implement a
second schema or policy engine or repair the remaining audit issues implicitly.
Native ADR/source coverage, source admission, site build and deployment retain
their existing separate jobs and fail-closed decisions. In particular, original
ADR-0001's missing authority/metadata remains owned by #47. Passing fixtures or
the complete regression gate cannot provide that approval.

`HYG-Q03` names this configured gate. The dated August roadmap snapshot remains
historical. Local execution and workflow source are distinct from an actual
changed-head hosted run, and neither proves that a provider ruleset requires
this check before merge. Track remaining hosted/acceptance work in [#76](https://github.com/egohygiene/hygiene/issues/76).
