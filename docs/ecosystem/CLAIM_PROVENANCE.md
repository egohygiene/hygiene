# Quantitative and compatibility claims

Status: **proposed alpha.1, observe only**. The
[policy](../../catalog/claim-provenance-policy.json),
[provenance schema](../../schemas/claim-provenance.v1.schema.json) and
[ADR-0022](../decisions/ADR-0022-evidence-backed-claim-provenance.md) implement
the bounded source contract in [Hygiene #30](https://github.com/egohygiene/hygiene/issues/30).
Approval remains null. A merged proposal or schema pass does not activate
enforcement or establish that a claim is true.

A statement such as “supports Windows” or “40% faster” must preserve the subject,
represented revision, environment, method and evidence that actually support it.
This contract references existing canonical evidence; it is not a second
benchmark, release or Intelligence database. A schema-conforming record can
still describe fabricated, biased or scientifically invalid evidence.

## Provenance and permitted strength

Every record has stable claim/subject identifiers, repository/component, exact
commit or explicit unknown/null, optional tag and released version, environment,
platform/architecture/runtime and material dependency versions/digests. A procedure
names a versioned command/workflow/adapter/manual method, configuration, dataset,
task, fixture and seed where applicable. Unknown optional inputs remain null;
the limitations explain missing or inapplicable details instead of inventing them.

Quantities define metric, units, aggregation, sample count, value and uncertainty
where appropriate. Null uncertainty is unknown or not supplied, never zero
uncertainty; state why in limitations. Evidence retains raw location or safe
handle, digest, capture time, retention and access boundary. Verification names
the clock, responsible workflow/reviewer and exact evidence IDs. Limitations,
exclusions, confounders, expiration and supersession remain explicit.

| Evidence state | Permitted presentation |
| --- | --- |
| measured | Measured value for the exact procedure, revision and environment; no causal or population-wide implication |
| verified | The named bounded probe was verified for the represented scope; no universal support/certification claim |
| provider-reported | Attribute provider and date; no independent-measurement label |
| reported | Attribute the source and retain verification gap |
| estimated | Show estimate, method, assumptions and uncertainty/limits |
| inferred | Label inference and link supporting evidence |
| unverified | Visibly unqualified; no positive check mark or support assertion |
| stale | Historical, expired or superseded; no current compatibility/support claim |
| blocked | Qualification could not complete; no inference of passed or failed behavior |
| unknown | Missing knowledge; never zero, unsupported or passing by default |
| not-applicable | Scoped reason; no passing test or earned completion |

Badges, benchmark rows and compatibility cells retain this exact state text,
revision, method, clock and evidence reference. Only measured/verified records
with complete current provenance are eligible for a positive **bounded evidence
label**. That label never means a whole repository is compliant, safe, fully
accessible, scientifically validated or ratified. Compatibility uses the exact
platform/runtime/probe cell, not a broader platform family. A bounded probe
cannot substantiate a benchmark; benchmark records use measured semantics.

The reference assessment preserves `declared_state` and calculates an independent
`effective_state`. A strong declaration with missing subject revision, runtime,
verification, expiry or bound raw evidence becomes unverified. Measurements also
need a metric and versioned configuration/fixture. Mutable versions are refused.
Channel matching is case-insensitive against the finite policy list: main,
master, latest, head, trunk, develop, stable, nightly, canary, next, edge,
current, rolling, beta, alpha and dev. Thus `STABLE` is refused, while
`1.2.3-alpha.1+build.7` is a distinct immutable version string. Unknown,
unavailable, unspecified, not-recorded and not-collected are case-insensitive
unknown values: they remain representable but never qualify a strong label in
subject/method/runtime/material-reference inputs. Lexical acceptance alone does
not prove a version exists or is immutable at its owner; actual source admission
must establish that separately.
This is deterministic provenance qualification, not authentication of supplied
facts or independent execution of the command.

## Freshness, retention and supersession

The caller supplies an explicit UTC `as_of`; the reference tool reads no clock.
Capture must precede verification, and neither can be in the future. Expiration
at the exact boundary, used-evidence retention expiry, or a successor makes the
effective state stale while preserving original state, clocks and citations.
Missing freshness/retention cannot support a positive evidence label. Re-running
a renderer cannot make old evidence fresh. Raw evidence may expire before a
claim's nominal window, so the earlier effective deadline wins.

Supersession names a different stable claim ID and retains the old record. A
consumer must resolve that ID and check subject/lineage/cycles at its canonical
owner; this single-record reference does not fetch or authenticate successors.
Do not overwrite historical claims when a command or revision changes. A new
record can supersede the prior result without relabelling its original scope.

## Safe access and human-readable views

Public raw references are caller-reviewed HTTPS locations without credentials,
query strings, fragments or unsafe Markdown characters. This lexical restriction
is not proof a destination is public or immutable. Restricted or unavailable
evidence uses an opaque `evidence:identifier` handle, never an internal URL,
filename, private title or local path. Access, redaction and retention remain
with the raw-evidence owner. No private logs, datasets or credentials are required
in public output; an opaque reference explicitly limits inspectability.

The pure public projector requires both public visibility and an independently
admitted repository allowlist. It excludes protected/unadmitted sources before
inspecting payloads. The linked Markdown view includes only identifiers, current
qualifier, revision, procedure, attributed workflow/source/reviewer identifier,
verification/expiry and safe raw references. Provider statements identify the
provider in that attribution field; unknown attribution remains visible.
It never echoes arbitrary statements, commands, limitations or protected content.
It intentionally omits the numeric value and its interpretation; a benchmark
renderer must additionally present metric/unit/aggregation/sample/uncertainty
and visible limits under the same qualification, not strip them for a headline.
Callers still authenticate source admission and publication selection separately.
This helper performs no publication.

## Existing evidence and ownership

The policy binds immutable versions/digests of the existing Intelligence alpha.2
schema, presentation/badge alpha.1 policy and release policy from Hygiene
`627b448f655afb2f4366654ba3ca3050389e464a`. They retain their actual proposed
lifecycle. It references Aether's artifact-record schema at immutable
`c1a27ed29a21d70e7c09dd76d1999b2363aa4940`, including identity/source digest,
compatibility, lifecycle and release fields. A source schema does not prove
consumer acceptance or release eligibility. Universal distribution
[Hygiene #29](https://github.com/egohygiene/hygiene/issues/29) remains a separate
open design input: no unimplemented contract or native-installability proof is
invented. Existing RI/report/AI/release artifacts remain canonical; link their
owner IDs and exact bytes rather than duplicating their stores or translating
states into unqualified success.

| Owner | Responsibility |
| --- | --- |
| Hygiene | state vocabulary, provenance shape, wording and policy lifecycle |
| Aether | AI artifact identity/provenance and authoring |
| Relay | renderer/workflow integration and safe evidence transport |
| EgoLint | production deterministic claim validation and normalized findings |
| Observatory | privacy-safe observation and freshness projection |
| Identity / Holon | evidence-linked visual assets / reviewed new-repo composition |
| Consumer repository | facts, measurement method, access/retention, revision scope and final review |

## Report-only migration and rollback

Inventory existing public claims without rewriting history. Link exact owning
evidence and fill honest unknowns, then preview qualifiers and suppressed positive
labels in report-only mode. Review representative methods, privacy and scope;
pin the exact policy revision/digest and compatible consumer implementation
together. Human policy disposition and separate production review precede
enforcement. Roll back by restoring the previous compatible policy/renderer
selection and stopping new enforcement; preserve old claims, raw references and
diagnostics. This change performs no fleet migration or policy activation.

## Executable synthetic pilot

[Six fixtures](../../fixtures/claims) cover a benchmark, compatibility probe,
provider-reported value, estimate, expired claim and blocked qualification.
All values, digests, clocks and responsible actors are synthetic demonstration
data. They are not actual product measurements or verified platform support.

```bash
python3 -E tools/claims.py fixtures/claims/benchmark.json --as-of 2026-11-14T00:00:00Z
python3 -I -m unittest discover -s tests -p test_claims.py -v
```

Both JSON schemas check shape. The dependency-free reference also checks bounded
IDs/versions, safe references, uniqueness, clock ordering, evidence membership
and current effective states. The executable tests exercise all eleven states,
missing evidence, stale retention, supersession, future clocks, privacy,
nonfinite/boolean values and ambiguous JSON. Scientific validity, actual raw
bytes, provenance authenticity and downstream/native behavior remain untested
by these source fixtures.
