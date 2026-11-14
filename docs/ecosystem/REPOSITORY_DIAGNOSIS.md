# Repository diagnosis capability

Status: **proposed alpha.1, observe only**. This policy implements the bounded
source contract in [Hygiene #41](https://github.com/egohygiene/hygiene/issues/41).
[ADR-0021](../decisions/ADR-0021-repository-diagnosis-applicability.md) is proposed
with no approval. Merging source does not mandate records or activate enforcement.

The stable capability is `repository.diagnosis-records`.
[The policy](../../catalog/repository-diagnosis-policy.json) and
[declaration schema](../../schemas/repository-diagnosis-capability.v1.schema.json)
describe applicability and access. Aether owns the record format and authoring:
[specification](https://github.com/egohygiene/aether/blob/e9aa58bb70c8b29179329c1c989aed38c620f7fd/library/organization/specs/quality/diagnosis-record.spec.md)
and [schema](https://github.com/egohygiene/aether/blob/e9aa58bb70c8b29179329c1c989aed38c620f7fd/catalog/schemas/aether.diagnosis-record.v1.schema.json).
The policy pins that exact revision, version 1.0.0, both SHA-256 digests and its
actual **draft, not released** lifecycle. This review pin supplies no production
eligibility. No record schema or authoring skill is copied into Hygiene.

| Condition | Applicability |
| --- | --- |
| Ordinary active repository | optional |
| Repeated or cross-session bounded investigation | recommended |
| Explicit repository-owned reviewed requirement | required |
| Archived, mirror or generated-only repository without owned investigations | not-applicable |
| Applicability not reviewed or evidence unavailable | unknown |
| Privacy, access or compatible contract prevents adoption | blocked |

These are declaration conditions, not an automatic fleet classifier. A repository
records a reason and independently selects enabled, opted-out or undecided
adoption. Required adoption with an opt-out remains a visible review gap; it is
not silently N/A. No record is required for every debugging interaction.

## Paths and indexes

The recommended directory is `.github/diagnostics/records/`. The declaration
stores its literal form without a trailing slash. An alternative needs an
explicit bounded repository-relative directory and reason. No absolute paths,
traversal, `.git`, URL escapes, globs or unbounded scanning are permitted.
The reference check does not open this directory. A production consumer must
resolve filesystem boundaries, refuse symlink escapes and read only admitted
regular files; lexical validation cannot prove filesystem containment.

Markdown records remain canonical. Indexes default to ephemeral, but a repository
may select tracked or none. The repository owns regeneration and review; Relay
may execute it and Observatory may observe an approved projection. A generated
index binds the observed source revision, source digest, observation time and
generation time. Its age comes from observation time: regenerating old evidence
does not refresh it. A different represented revision yields `source-mismatch`.
Future/inverted clocks are refused. Freshness defaults to a repository-declared
seven-day example window, not a universal health promise.

`not-collected`, `no-records`, `no-recent-records`, `available` and `unavailable`
stay distinct. They all leave repository health **unknown**. No records or no
recent activity cannot establish health, incident absence or successful testing.
Schema conformance validates structure, not the truth of a diagnosis. A narrow
probe supports only the behavior it exercised.

## Privacy, retention and publication

Default sensitivity is restricted and default publication is none, including
in a public repository. The declaration permits only internal/restricted default
classification; individual public records require their own review under Aether.
Record content, filenames, counts and clocks can disclose protected work.
Neither a public repository nor a valid declaration authorizes publication.

The pure public projection first excludes private, internal and unknown visibility
without inspecting protected payloads. Even explicit public-summary selection
can expose only capability, applicability, adoption and freshness. It emits no
identity, path, record count, timestamp, free-form reason, evidence payload or
placeholder for excluded sources. Its caller must independently authenticate
visibility and publication selection; a caller declaration is not approval.
Redact raw evidence before any separately approved publication and preserve the
kind/extent of omissions. Do not put credentials or private context in records.

Every declaration names a retention window or an explicit undecided/null window,
with a reason. Null means no automatic expiry/deletion, not a promise of indefinite
retention. Review security/legal holds, links and raw-evidence owners before
deleting. This contract performs no deletion or redaction. Opt-out stops future
collection/projection but preserves existing records and history pending separate
authorized review. Correction/supersession must preserve stable record IDs and
provenance; never rewrite a diagnosis to fabricate a historical success.

## Boundaries and adoption

Diagnosis records are bounded investigation narratives and evidence references.
ADRs retain architecture decision and human lifecycle authority; security
advisories retain coordinated disclosure; incident postmortems retain incident
severity, communications and learning; audit logs retain event chronology;
ordinary debug logs remain raw evidence. Link them instead of replacing them.
Diagnosis-only activity grants neither remediation nor publication permission.

| Owner | Handoff |
| --- | --- |
| Hygiene | applicability/path/privacy/retention/index policy and proposed lifecycle |
| Aether | pinned record schema, specification and authoring skill |
| EgoLint | production declaration/record validation and normalized findings |
| Observatory | privacy-safe source/freshness projections; no health inference |
| Relay | reusable execution and approved presentation; no site facts/approval |
| Pace | reviewed reversible adoption proposals for existing repositories |
| Repository | applicability, record facts, sensitivity, retention/holds and final review |

Start report-only with an exact reviewed policy revision/digest and Aether pin.
Inventory only explicitly selected paths and safe metadata; preview changes and
opt-outs without moving/deleting authored records. Retain old pins/paths and
rollback by stopping the new collector/projection and restoring the prior
selection. Only explicit maintainer disposition and eligible owner artifacts can
promote required enforcement. No downstream implementation or fleet adoption
is claimed here.

## Executable synthetic examples

[Fixtures](../../fixtures/repository-diagnosis) cover an opted-out repository,
a private repository, a public repository with restricted evidence, and an
explicit safe summary with an alternative bounded path. They are synthetic
declarations, not real investigations or production visibility approvals.

```bash
python3 -E tools/diagnosis.py fixtures/repository-diagnosis/public-restricted.json --as-of 2026-11-14T00:00:00Z
python3 -I -m unittest discover -s tests -p test_diagnosis.py -v
```

The dependency-free reference checks declaration shape and cross-field refusal,
privacy allowlists, exact upstream selection and explicit-clock freshness. It
does not parse records, fetch references, crawl files, authenticate observations,
verify diagnosis truth or infer current fleet state. JSON Schema checks shape;
the reference check adds source equality, clock ordering and privacy semantics.
