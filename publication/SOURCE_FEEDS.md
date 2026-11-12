# Public provider source feeds

This candidate is prepared from Hygiene main
`1bf05c0763b1ffe5434c30eb80f2a51a7b106cf5`, after the existing Journey/Search
adoption. The selected shared Relay revision is
`981ddf4367c67fcd625e54321d95bab027f6c0f2`, merged through
[Relay #176](https://github.com/egohygiene/relay/pull/176).
The current Relay producer, native builder, validation/provenance
helpers and `site.json` exact-generator seal must select the same reviewed
immutable revision before handoff. No consumer implementation is copied.

## Existing admission remains first

The `checks`, `validation`, `admission`, `build` and `deploy` jobs, event set,
dependencies, build admission condition and deployment condition are preserved.
The new steps are inside `build`, which already requires
`needs.admission.outputs.ready == 'true'`. Only canonical
`egohygiene/hygiene` push/manual contexts select provider capture. A PR may
retain the existing admitted ADR/Journey/Search review path but cannot capture
provider feeds or deploy through this patch.

Original ADR-0001 metadata, its historical Accepted claim, actual human
architecture approval, canonical policy-owner mode and the explicit Identity
ADR-0017 reference are unchanged. The metadata/approval hold remains real:
when source admission blocks the job, capture, generation and deployment remain
unreached. This packet supplies no ratification, exemption or gate bypass.

## Producer, ordinary artifact, native admission

The shared `repository-intelligence-github-sources` producer captures bounded
public issue/PR metadata, check runs matched to the represented source commit,
and published release metadata. Public titles/check names are explicitly opted
in through its supported bounded field contract. Bodies, comments, actors,
emails, logs, drafts/private releases and unauthorized data are excluded by the
shared producer. Missing access, partial pages, findings and execution remain
distinct; no capture establishes a clean repository or completed installation.

The producer writes its closed capture bundle outside the checkout and emits
the existing repository/head/run/attempt-bound artifact name. An ordinary
`actions/upload-artifact` step retains those bytes for seven days. Its actual
artifact ID and ZIP digest, together with the producer's actual UTC `as-of`
boundary, are passed unchanged to the existing native builder. No latest-artifact
search, SHA substitution or commit-time clock refresh is introduced.

The existing `collect-adrs`, `collect-journey` and `search-attribution` options
remain enabled. `collect-dependencies` is true only when this invocation has an
actual capture artifact ID. The shared builder performs its existing same-run
artifact admission and native validation; it owns normalized Work/Health/Releases
and the reviewed public dependency source. Missing/failed capture or upload does
not silently promote an uncaptured provider build: normal step failure prevents
the existing generator from running. An intentionally skipped capture supplies
empty artifact/clock inputs and leaves dependencies unselected.

The build job adds only read permissions for Actions artifact admission, issues,
pull requests and checks, alongside its existing contents read permission.
Pages write and OIDC remain solely in the unchanged deploy job. Public admission
and release/asset reads follow the producer's unauthenticated public interface;
the optional GitHub token is read-only. No new provider, event, job or environment
is installed by this consumer patch.

## Retention, site and recovery

A separate ordinary artifact retains the bounded sanitized producer receipt for
seven days, including when available after an unsuccessful producer/packing
stage. Raw captures and producer receipt are never copied into `dist/` or the
Pages artifact. The existing site handoff, composition inventory, aliases,
canonical origin, immutable selected source, transport seal and complete
manifest verification remain unchanged.

The original 90-day site/recovery/evidence retention and capture-before-deploy
ordering remain intact. Historical source revisions, recovery bytes/digests and
approval evidence are not rewritten. Compare still needs separately reviewed
real retained pairs and an explicit baseline lease; none is selected or created.
This does not add an owner conformance or ratification snapshot automatically.

## Review boundary

Only YAML/JSON parsing, scoped workflow/source preservation and source peer
inspection are included. No API calls, provider/native execution, tests, builds,
CI investigation, dispatch, artifact upload, browser check, deployment or live
verification was performed. The existing 30-minute build limit is unchanged;
actual producer/acquisition/native timing and hosted authority need the deferred
qualification pass. Artifact creation, native admission, ordinary upload, Pages
upload, deployment and live proof must be reported separately when run.

ADR disposition: reference accepted ADR-0002's delivery-history and source/lifecycle
authority and the existing proposed publication records. This bounded consumer
selection changes no owner policy, human disposition or publication authority;
no duplicate ADR is required. Hygiene #47 and all qualification gates remain open.
