# Hygiene source-backfill checkpoint — 2026-10-18

This follows the [October 10 inventory](2026-10-10-hygiene-inventory.md) for
[Hygiene #47](https://github.com/egohygiene/hygiene/issues/47). It is stacked on
[PR #68](https://github.com/egohygiene/hygiene/pull/68), exact head
`f234155ff76ffe7164c3d7293318e5e3f9262689`; the historical preservation receipt remains unchanged. The inventory prose is
preserved while its relative links are rebound at the support-document location. Base main is
`b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3`. Full reachable main history contains
81 commits after explicit history acquisition; no unrecorded intent is inferred.

## Source changes

| Surface | Change | Authority retained |
| --- | --- | --- |
| ADR-004 | Insert the missing required Implementation and evidence links section using its existing citations | Every original line and all metadata remain; proposed/in_progress labels unchanged |
| ADR-014 | New repository-local historical proposal for JSON-compatible catalogs and dependency-free Python reference tools | Original implementation/rationale are linked; proposed, null approval, implemented independently of disposition |
| Canonical index | Add ADR-014 and links to this packet and capture guide | One numeric-order row per record; historical identities unchanged |
| Support-document layout | Move migration packets and capture guidance to `docs/adr-workflow/` | Original inventory prose and historical JSON receipt preserved; relative Markdown destinations rebound |
| AGENTS.md | Insert exactly one pinned Aether decision-impact block through its managed merge helper, plus local owner/loading pointers | Existing local instructions and continuity block preserved; no skill installation or automatic enforcement claim |
| ADR-0001 review patch | Prepare required anatomy/metadata while preserving substantive source prose | Unapplied; canonical record unchanged; null approval and proposed identity exception intentionally block conformance |

ADR-002 and ADR-003 through ADR-013 retain their original dispositions; only
ADR-004 gains the bounded section. Twelve current proposals include the new
ADR-014. No architecture/catalog ownership, policy bytes, schemas, production
workflow, release, host or deployed files change. Existing dated implementation
wording elsewhere is left for separate evidence correction rather than inferred
ratification or status promotion.

## Concrete ADR-0001 review

The [unapplied review patch](2026-10-18-adr-0001-review.patch) targets only
`docs/decisions/ADR-0001-holistic-architecture-v0.1.md`, whose original SHA-256 is
`5b7a4f36456e80790d4f7d989600310f8effdb2f800058f0f0bb23826730655b`.
It preserves the Accepted/date bullets, four-digit identity, substantive prose,
five-plane terminology and dependency-boundary amendment. It moves the existing
Rejected bullets under the required alternatives heading, renames the historical
Consequences heading, places Verification under the required evidence heading,
and explicitly records absent historical exit-strategy evidence.

This file is review material, not another canonical ADR or a ready-to-apply
approved migration. **Do not apply it to main as supplied.** The draft preserves
the existing accepted claim with `approval: null`; its legacy-identity exception
is proposed with null approval evidence. A syntax-only preview uses
`git apply --unidiff-zero --check` against the original source hash; it does not
apply or approve the patch. The expected owner validation failure
is evidence that no approval has been fabricated.

The existing [disposition recommendation](2026-10-10-hygiene-inventory.md#adr-0001-disposition-packet)
is ready for the maintainer: reaffirm the unchanged historical record and approve
only its legacy ID/filename exception, or explicitly clarify the intended
historical disposition. If reaffirmed, record the actual date, authority and
durable evidence in both approval and matching approval evidence; separately
record actual exception authority. Preserve the old historical date rather than
backdating the new reaffirmation. No human response is presumed by preparing
this patch, and no future policy exception can waive human lifecycle authority.

After that disposition, apply the reviewed patch, complete real metadata and
rerun native owner validation at the exact new Git revision. Do not copy example
approval objects or silently relabel the original record to get a green result.

## Support-document layout

The native collector conservatively marks unrecognized Markdown inside the
canonical decision directory as incomplete, so it cannot mistake a legacy
record for a harmless note. The inventory packet previously lived there, and
the first draft added two more support documents. This checkpoint moves those
notes to `docs/adr-workflow/` and repairs relative links. It does not weaken the
collector's legacy detection or hide a canonical decision. All fourteen ADRs
remain indexed in `docs/decisions/`; the unapplied review patch is also outside
the ledger directory. The original October 10 packet remains available at its
immutable PR #68 head. Its prose is unchanged here apart from link destinations;
its historical JSON preservation receipt remains byte-identical.

## Native source-validation boundary

Merged EgoLint `72267fd0a371da6d94922cbc6bd3dedddb68df30` supplies owner semantics.
[Relay #154](https://github.com/egohygiene/relay/pull/154) saves candidate
`acfb1222b5f05298ad8c94b2e83bfece84b6cdf8`; hosted action/native validation and
continuity preflight passed for that candidate. It remains a draft; no merged
Relay consumer baseline is claimed. The
[capture guide](CAPTURE.md) records exact authoring and validation selections.

The [bounded source evidence](../evidence/hygiene-adrs-source-backfill-2026-10-18.json)
records reference metadata/anatomy checks, source preservation, managed-module
bytes and the native whole-corpus replay. Source validity remains blocked by
legacy ADR-0001 and its resulting index/lineage gaps. ADR-013's external
`egohygiene/identity#ADR-017` is an existing declared relationship; the recorded
Relay #154 collector has no external-decision selection input, so that finding
does not prove the public target is missing. Preserve the relationship and
select it explicitly through the follow-up below.

## External-reference follow-up and review order

[Relay #155](https://github.com/egohygiene/relay/pull/155), exact candidate
`9fb7b2795d9d0bfa9849a1974ba58bbc7bcf8275`, forwards the existing native external
ADR declaration through every supported input and provenance boundary. Its
local full suite passes 670 tests (19 optional native checks skipped), and fresh
locked acquisition passes all 40 ADR tests with no skips. Hosted checks are
separate candidate evidence. The
[paired immutable Hygiene replay](https://github.com/egohygiene/relay/blob/9fb7b2795d9d0bfa9849a1974ba58bbc7bcf8275/docs/evidence/external-adr-declarations-2026-10-18.json)
removes exactly the one external finding with all 23 source hashes and both
candidate digests unchanged; source remains invalid/publication denied for
ADR-0001's legacy migration. This supplements the earlier dated receipt rather
than rewriting its observation.

Review Relay #154, then retarget/review #155 and use its exact merged revision.
Separately review Hygiene #68, then retarget/review #70. Actual human ADR-0001
disposition and its identity exception can be reviewed from the prepared patch;
apply only with real evidence, then rerun source admission using the exact Relay
baseline and the explicit Identity key in the capture guide. No merge or human
disposition is presumed by these prepared review chains.

## Remaining mini-roadmap

| Step | Prepared state | Next owner/gate |
| --- | --- | --- |
| Shared owner semantics | EgoLint #82 merged; Relay #154 and #155 prepared as a stack | Review/merge owner support then external-input follow-up, using the exact final merge revision |
| Source backfill | ADR-004, proposed ADR-014, capture instructions and legacy review patch drafted | Review this stacked source change and resolve ADR-0001 disposition/exception |
| Full source admission | Native review at immutable candidate; remaining findings retained | Apply actual legacy disposition and select the reviewed external key through Relay #155, then rerun shared validation |
| Read-only production artifact | No invalid corpus promoted | Exact supported Relay baseline and valid source; keep all uncollected domains explicit |
| Host and route | No declaration or deployment invented | Review concrete declaration/composition in the actual publication repository |
| Publication and upkeep | Capture source/pins documented; no automatic hook claimed | Validate/render, approve actual publication, verify live bytes/accessibility/favicons and rollback; close #47 only on its full acceptance |

Rollback is reverting this source checkpoint relative to the inventory head.
The review patch has no applied source state to roll back. Existing deployed
sites, release state, policy authority and historical inventory receipts remain
outside this change.

ADR-Ref: `egohygiene/hygiene#ADR-014` (create; proposed historical reconstruction)
and `egohygiene/hygiene#ADR-004` (update; missing evidence section). ADR-002 governs
metadata and human authority. This checkpoint does not propose a new global
runtime rule or public-host architecture.

## Subsequent merge and host checkpoint

The earlier sections preserve the source-preparation observation. Relay #154
merged at `f2e624cbbd1bb1150e29743061140f601b8486f6`, then #155 at
`6cddad3124bdda1b1e3d54a40931f23322b7be26`. Hygiene #68 merged at
`b774a63187476a1ef83291a3a3fc33a5c6a0e86d`, then #70 at
`6db2a38fb80d9881a7d7d001ffb6d2f8456c3262`. Those merges do not themselves
ratify ADR-0001 or the other proposals.

The maintainer selected `https://hygiene.egohygiene.io` for this repository
and configured GitHub Actions Pages with verified DNS. The
[publication runbook](../../publication/README.md) now prepares that concrete
consumer publisher, canonical repository routes and explicit admission gate.
The remaining source decision is the unchanged ADR-0001's actual approval and
legacy-identity exception. Publication, live UI and provider recovery are
observations to collect after that gate; no invalid corpus is promoted.
