# Complete reference-gate execution repair

Tracking: [Hygiene #76](https://github.com/egohygiene/hygiene/issues/76),
Roadmap-Step: HYG-Q03. Observed 2026-11-13 UTC.

## Cause and bounded repair

Seven runner integration scenarios copied the complete domain suite into their
disposable repositories and ran it again along with all reference commands.
The outer suite therefore multiplied domain work and exceeded its unchanged
60-second command deadline. Its prior bounded log had already reached a failed
runner control before the timeout, so extending the cap would not establish
success.

Those copies also excluded `.cache`, dropping the exact Aether source now
required by the composed release-declaration CLI. The regular read-only checks
job had not prepared that owner/runtime either. Both were real prerequisites,
not reasons to waive release validation.

The scenarios now use a minimal passing unittest family, with actual injected
pass/skip/failure/empty discovery cases. They still execute every real reference
CLI against disposable canonical inputs. The outer production gate remains
unchanged and discovers every actual test module exactly once. Copies receive
only the three owner files already selected by `tools/release-owner.lock.json`;
arbitrary cache contents are excluded. A new timeout control confirms a killed
command remains failed with retained diagnostics and restores the real 60-second
cap after its short disposable test.

The checks job acquires the existing exact Aether
`8a2a3d08f3aa9da3847bd5277843506ab855192e`, verifies its locked source bytes
before installation, and prepares its pinned runtime in a virtual environment.
This uses the established release-workflow preparation; it does not change
owner, dependency pins, checks permissions, native admission or publication.

## Actual local result

Clean functional source:
`798227ff6b3f4d1334beb5412802bcf4529a57a2`.

The [bounded JSON receipt](2026-11-13-hygiene-76-unit-gate.json) records the actual
configured `tools/check_contracts.py` run: **25/25 checks passed; 302 tests;
zero failures, errors or skips**. Unit execution completed in **22.741 seconds**
under the unchanged 60-second cap. The selected Python was 3.12.14 with
jsonschema 4.10.3, PyYAML 6.0.1, attrs 22.2.0 and pyrsistent 0.20.0. Earlier,
all eight focused runner controls passed in 12.858 seconds. The complete gate
retains actual discovery, explicit skips, failed and empty suites, invalid
catalog/profile input, stale generated output, bounded logs and timeout failure.

This later evidence/continuity change does not relabel its own containing commit
as the tested functional source. Actual PR-event hosted evidence remains a
separate observation. The earlier
[a28fb620 failure](2026-11-13-reference-gate.json) stays unchanged as dated
evidence; it is not silently replaced or retimed.

## Exact native source replay

The exact selected Relay `981ddf4367c67fcd625e54321d95bab027f6c0f2`
prepared a fresh offline native runtime from its selected EgoLint
`d917ea524962639494e5bb4b3196192238ba57d9`, policy and Holon Git objects,
with checksum-locked Python dependencies and Rust 1.85.1. The runtime receipt
binds its actual executable and profile digests; no older cached binary was
substituted for the new build.

Actual adapter runs against immutable candidate `798227f` and unchanged main
`6cc9c63` both completed with **identical 20 retained findings** and
`semantic_status: nonconformant`. ADR coverage is `failed`; contract and diagram
coverage are `unavailable` with unknown adoption. The advisory process exit 0
does not make these passing coverage results. Existing findings include
ADR-0001 metadata, ADR lineage/index, supported contract pins and unknown
adoption. Their exact counts, source provenance and report hashes are retained
in the bounded JSON receipt. The repair introduces none of these findings.

## Remaining independent boundaries

Read-only provider queries returned an empty repository-ruleset list and HTTP403
for main branch-protection details because the integration lacks access. Neither
result establishes required-check enforcement; no provider policy was changed.

Changed-head hosted reference execution remains a separate observation from
the local gate and native replay. A successful advisory process cannot waive original
ADR-0001's actual source and human approval under #47. Agent-Ready Web lifecycle
remains #95, and the broader parent #76 stays open. No deployment, publication,
human ratification or whole-organization conformance is claimed here.

Decision impact: ADR not required for routine runner-fixture isolation and
explicit preparation of the existing ADR-0015 release-owner composition. Accepted
ADR-0002 authority and every proposed decision disposition remain unchanged.
