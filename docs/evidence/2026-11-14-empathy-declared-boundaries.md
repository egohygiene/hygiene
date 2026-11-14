# Empathy declared-consumer boundary reconciliation

Tracking: [Hygiene #76](https://github.com/egohygiene/hygiene/issues/76),
[Empathy #105](https://github.com/egohygiene/empathy/issues/105) and
[#98](https://github.com/egohygiene/empathy/issues/98). Observed 2026-11-14 UTC.

## Existing intent and exact mismatch

The canonical repository catalog declares Empathy's golden-consumer role and
its consumption of `mantle runtime` and `egolint profiles`. The context mapping
resolves those terms to Mantle and EgoLint. The existing
[architecture](../ecosystem/ARCHITECTURE.md) and
[repository catalog](../ecosystem/REPOSITORY_CATALOG.md) retain that intended
role. Declared integration is separate from runtime adoption; Mantle extraction
and planned released consumption through Realm do not establish an installed
runtime or completed migration.

However, `RELATIONSHIP-006` permitted Mantle only to Realm and
`RELATIONSHIP-008` permitted EgoLint only to Relay. Exact native collection of
the public declarations therefore rejected Empathy's first unresolved edge with
`BOUNDARY`; a complete read-only precondition enumeration identified both gaps.
Neither edge was explicitly forbidden. Deleting intended declarations or
disabling dependency collection would discard the authored intent.

## Narrow owner correction

The two existing relationships now name `egohygiene/empathy` explicitly alongside
their original consumers. There is no wildcard addition, new capability owner,
exception or contract activation. Existing interfaces, `required`/null contract
state, immutable/versioned pinning, every forbidden edge and the default deny
policy remain unchanged. Removing only the two new memberships makes the full
register exactly equal to baseline `044b3f1797937092a36e4d51ebb67b1b760b1916`.

Only the generated dependency-boundary view is regenerated. The public roster,
catalog observation date and provider observation timestamps remain unchanged.
Downstream admission and declaration locks must select the same new immutable
Hygiene revision/tree after source review; no lock equality is relaxed here.

## Executed qualification

Clean functional source `d5c65d9` passes all **25 complete reference checks and
303 tests**, with zero failures/errors/skips under the unchanged 60-second
command deadline. All **29 focused boundary tests**, canonical registered-format
schema validation and generated boundary/public-catalog checks pass.

The [bounded native-function receipt](2026-11-14-empathy-declared-boundaries.json)
uses the exact existing Relay `d7c60473626f8dcc901210a208ad01a6474e8c1d`
public-selection and graph functions against candidate canonical owner
declarations/public rows. It selects the expected four direct edges to Realm,
Mantle, Relay and EgoLint. Removing either corrected membership still fails with
`BOUNDARY`; adding a forbidden edge still overrides an allow and fails closed.
This is explicitly a function fixture, not a newly locked source admission,
consumer publication result or runtime-adoption claim.

## Integration boundary

Root source review/integration precedes the compatible Relay admission and
declaration profile upgrade; the Empathy consumer then adopts that reviewed
immutable Relay source and obtains fresh execution evidence. Historical captures
and report clocks are not retimed to qualify later source.

Original ADR-0001 source/human/publication and provider-enforcement limitations
stay under Hygiene #76/#47; Agent-Ready Web lifecycle stays #95. Empathy's
current/rollback and report-source gates retain their separate actual evidence.
No issue closure, human ratification, deployment or publication is claimed here.

Decision impact: ADR not required for reconciling machine-consumer entries with
the existing canonical golden-consumer intent. Existing ownership, producer
contracts and actual ADR dispositions remain unchanged.
