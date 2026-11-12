# Public repository inventory and checkpoints

Owner: Hygiene. Implementation: [issue #36](https://github.com/egohygiene/hygiene/issues/36).
The [checkpoint profile](../../catalog/organization-checkpoints.json) is proposed;
it composes Aether's approved auditor 2.0.0 at its exact recorded source/digest.
It installs no scheduler and grants no provider, publication or human-decision authority.

## Canonical source and public admission

[`catalog/repositories.yaml`](../../catalog/repositories.yaml) remains the one
authored role/identity catalog. Its existing non-public role declarations are
outside the public inventory interface. General `tools/catalog.py` and
`tools/context.py` operate on that complete authored source; their reports,
counts and projections are not public inventory artifacts.

[`catalog/public-repositories.json`](../../catalog/public-repositories.json)
is the derived, reviewed public admission interface. Its owner schema is
[`repository-public-catalog.v1`](../../schemas/repository-public-catalog.v1.schema.json).
It contains only explicit public rows with provider ID, canonical identity,
declared aliases, public observation, roles and dated/unknown gates. Downstream
Relay, Pace and Observatory consumers pin this public artifact, schema and
helper source at one immutable Hygiene revision. They do not derive a new
registry, enumerate protected repositories or turn inventory admission into
conformance. A missing repository has no inferred visibility or reason.

The 2026-11-09 public endpoint observation contains 28 public repositories.
That is a dated public result, never a fixed future organization total.
[`public-repository-observation.json`](../../catalog/public-repository-observation.json)
retains only public identity metadata from the unauthenticated GitHub organization
endpoint with `type=public`, page size 100; the response was shorter than a page.
Independent public-only connector discovery agreed. No authorized private
inventory was acquired. A future capture must follow all pages and declare
`partial` when complete discovery cannot be established.

`egohygiene/egohygiene.io` is canonical, with the declared historical alias
`website`. Stable provider ID 1318535423 binds this identity; alias lookup is
explicit rather than a guessed rewrite. Current dependency-register references
use the canonical name. Historical ADRs and immutable receipts retain their
original spellings. Provider IDs detect later renames even when names change.

Antidote's research program/local instrument and Civics' static civic knowledge
base fit the existing knowledge/research plane definition. Their rows cite
immutable owner README/architecture sources and actual roadmap gates. The
provisional/experimental maturity descriptions are source claims, not a score.
Neither owner declares a compatible architectural lifecycle; that field stays
`unknown`. The renamed site's previous rename-pending lifecycle/gate no longer
describes a current next action and also stays unknown pending a source-backed
declaration. These unknowns do not block public identity admission.

Existing role/lifecycle declarations were preserved. The older first gates are
dated source declarations, not freshly verified readiness or remaining-work
claims. Native source coverage, acceptance, publication and human approvals
remain independent. Original ADR-0001 and its approval-null patch are untouched.

## Offline adapter

The standard-library adapter is [`tools/public_inventory.py`](../../tools/public_inventory.py).
It performs no provider discovery, checkout, installation, workflow dispatch or
registry mutation. Explicit public visibility is selected before identities,
duplicates, text, gate validation, counts or hashes. Ambiguous duplicate
visibility rows are excluded; duplicate keys in selected public records fail
closed. Protected rows with irrelevant duplicate keys do not change the public
projection. Bounded JSON transport requirements still apply.

```sh
python3 -I tools/public_inventory.py project
python3 -I tools/public_inventory.py check-generated
python3 -I tools/public_inventory.py check \
  --discovery catalog/public-repository-observation.json \
  --as-of 2026-11-09T14:06:57Z --maximum-age-seconds 604800
```

`project` writes the derived public artifact atomically and refuses to overwrite
its canonical input, including an existing same-file alias. `check-generated`
compares the exact public bytes. `check` accepts the closed public-discovery
shape, binds stable provider IDs and emits a deterministic public drift receipt
under [`repository-public-drift.v1`](../../schemas/repository-public-drift.v1.schema.json).
Exit 0 means only current complete public inventory parity; drift/stale/partial
returns 1 and invalid/inaccessible input returns 2. No result certifies roles,
backlog health, ADR approval or publication.

The receipt separates public missing/extra/renamed identities, archive/default
branch changes and freshness. A transfer outside the organization, visibility
change, deletion or access failure cannot be distinguished from absence without
additional authorized public evidence; the report does not invent a cause.
Partial discovery never establishes absence. Future observations reject. The
explicit evaluation clock and bounded maximum age are inputs; the process wall
clock, raw input checksum, private rows/counts and unused fields never enter
public bytes or digests. Protected input changes within the supported transport
boundary cannot alter the admitted public projection.

## Recurrence, retention and owner handoffs

The proposed default is a weekly public inventory checkpoint, plus explicit
architecture-release, milestone, pre-release, identity-change and on-demand
checkpoints. Each invocation supplies an evaluation boundary. An observation
older than seven days is stale under that profile; a caller may explicitly
select a tighter bounded age. A missing/partial source cannot pass by timing alone.

The checkpoint report follows the pinned Aether request/evidence/finding/status
and immutable dated-report contract. Report catalog drift, backlog shape,
conformance adoption, exceptions and positive evidence separately. A source not
collected remains unavailable; this catalog adapter supplies only inventory
evidence. Retain the dated report and exact public inputs for at least 90 days
under the consumer's artifact lifecycle. Compare only an explicitly selected
compatible prior public artifact/digest; missing, expired, inaccessible or
incompatible baselines remain unavailable. A failed collection never replaces
the last valid baseline. Clocks/transport receipts stay outside deterministic
catalog bytes.

Pace owns discovery/adoption proposals and reviewable reconciliation. Observatory
owns normalization and reporting. Relay owns reusable execution/retention;
Hygiene owns identity/role/applicability policy. Each repository owns its source
facts and final publication. New-repository and rename/transfer/archive/privacy
rules are machine-listed in the profile. Discovery never silently adds an
allowlisted identity or assigns a role; review the bounded catalog change first.

## Review boundary

This implementation pass performs source inspection and static schema/syntax
checks only. The commands above, regression cases, native/runtime compatibility,
scheduled/hosted execution and actual downstream intake remain unexecuted.
The public JSON was authored as a data projection without executing the new
adapter; `check-generated` remains the deferred executable parity gate.
Policy proposal and authoring completeness do not establish ratification,
conformance, provider execution or production freshness.
