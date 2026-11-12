# Hygiene completeness, contract integrity, and work-ledger audit

- **Assessment ID:** `hygiene-completeness-20261020T040335Z`.
- **Assessment date:** 2026-10-20 UTC and America/New_York. The identifier anchors this assessment; later executed receipts retain their actual times.
- **Repository:** [egohygiene/hygiene](https://github.com/egohygiene/hygiene).
- **Frozen source:** [`aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d`](https://github.com/egohygiene/hygiene/tree/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d).
- **Git tree:** `b1e0a67191e8c86ea89c25e1e8f67a12237cac7c`.
- **Governing audit:** [Aether auditor specification 2.0.0, approved][auditor], with [audit-repository 1.1.0, draft][audit-skill] and continuity **Resume** behavior, selected at immutable Aether revision `dc8a16851f452763ef4f7fbe4bf057d4500b1921`.
- **Report status:** **partial**. Repository source, local checks, bounded counterexamples, historical audits, public tracker evidence, and exact hosted job results were inspected. This is a Hygiene repository audit, not a fresh full-organization audit, security certification, policy ratification, release, or live-site acceptance.
- **Validation receipt:** [data/hygiene-completeness-20261020T040335Z.validation.json](data/hygiene-completeness-20261020T040335Z.validation.json).
- **Tracker boundary:** 31 original open Hygiene issues and no open PRs at the baseline. Candidate issue keys in this dated report are uncreated proposals; subsequent issue numbers and execution ordering belong in the live repository roadmap. Existing issues, historical reports, accepted decisions, and human authority remain preserved.

## Executive summary

Hygiene already provides substantial working infrastructure: a repository registry, dependency boundaries, an organization contract index, twelve focused test modules, eleven reference tools, eighteen schemas, and a consumer-owned source-admission/publication path composed from immutable Relay inputs. Its ownership model consistently separates policy from execution, scaffolding, observation, agent guidance, and fleet convergence. The useful next step is a bounded correctness and evidence-reconciliation cycle rather than another architecture framework.

The normal local path is green: **194 tests, zero skips**, all 24 retained baseline check commands exit 0, all eighteen JSON Schemas validate against their selected metaschemas, generated catalog/boundary views match their sources, and temporary Excalidraw regeneration is byte-identical. Those checks do not establish complete instance-schema coverage, full current CI coverage, current policy applicability, or a deployed site. Negative cases below demonstrate where explicit evidence, dates, contract identity, or integration selections can still disagree while reference validation reports success.

The exact-main Hygiene Pages workflow is successful as a process, but its build and deployment jobs are **skipped**. The known ADR-0001 metadata/human-disposition gap remains correctly visible under existing #47; this audit neither invents approval nor applies its prepared review patch. A separate workflow/configuration generator-pin mismatch is latent behind that gate and also belongs to #47. Present release verification has its own bounded contract-composition gap, independent of the future successor release-design program.

The existing issue portfolio should be retained intact. Several issues are organization initiatives coordinating other repositories, not a complete Hygiene execution ledger. A repository-local roadmap can preserve those initiatives while identifying immediately startable fixes, human-review gates, and longer-term opt-in policy work. A proposed minimum usable baseline need not make all research, commercial-platform, confidentiality, or fleet-adoption work prerequisites for ordinary development.

## Scope and evidence rules

The authorized outcome is an evidence-backed repository audit, reconciliation against every open issue, focused gap issues, and a complete dependency-aware roadmap. Collection is read-only; publishing the report and managing the tracker are separately authorized follow-on actions in this workflow. Audit guidance itself grants no permission to repair source, change accepted policy, assign human disposition, create credentials, publish a release/site, or delete migration evidence.

The inspected source contains **182 tracked Git entries** and **2,122,968 bytes of blob payload**. Counts describe the frozen Git tree, not on-disk allocation, released maturity, or fleet adoption.

| Inventory | Observed count |
| --- | ---: |
| Root Markdown files | 22 |
| JSON Schemas | 18 |
| Python reference tools | 11 |
| Test modules | 12 |
| Repository-registry records | 27 |
| Organization contract-index entries | 16 |
| Contract lifecycle | 3 active, 12 proposed, 1 deprecated |
| Canonical numbered ADRs | 14 |
| Tracked staging files | 0 |
| Original open work issues | 31 |
| Open PRs at baseline | 0 |
| Observed GitHub releases / Git tags | 0 / 0 |

No current private-repository discovery was required. Historical catalog/audit content is not a license to disclose protected current names, counts, placeholders, or inferred gaps. Catalog reconciliation under #36 must use an explicit authorized inventory and public allowlist rather than automatically promoting every historical reference into public output.

Evidence labels throughout the report mean:

- **Observed:** directly inspected source, tracked inventory, provider response, or executed bounded result.
- **Inferred:** a conclusion drawn from those observations, with practical limits stated.
- **Recommended:** proposed repair, sequencing, acceptance, or human-review action; not delivered implementation.
- **Unverified:** evidence unavailable or not exercised; never silently treated as success or failure.

Findings use the auditor's normalized primary classification, severity, confidence, status, effort, and impact. Newly reproduced means newly established in this assessment, not a claim about the commit that introduced a defect. Synthetic invalid inputs establish only their tested behavior; no real secret disclosure, exploitation, wrong live exemption, fraudulent approval, or published invalid artifact is asserted.

## Discovery, methodology, and history

The audit read AGENTS, canonical ecosystem architecture, agent context, dependency boundaries, relevant accepted and proposed ADRs, the actual v1.2.0 policy and ratification evidence, current continuity, root architecture/navigation, catalogs, schemas, fixtures, source/reference tools, tasks/workflows, tests, publication guidance, and prior audits. Source inspections were divided into contract/registry correctness, policy/evidence semantics, publication/release integration, architecture/navigation, and the complete issue ledger, then reconciled for overlap.

The actual accepted ADR policy is **v1.2.0**, with its October 18 four-digit naming amendment recorded separately from the original September v1.1.0 ratification. The audit does not request duplicate ratification or interpret a historically accurate v1.1.0 statement as invalid policy. ADR-0001's preserved original body and its missing structured approval/metadata are a separate known #47 gate. Other canonical records retain their own proposed or accepted states; a merge is not human acceptance.

Existing reports under `.audits/` are organization-wide snapshots dated August 19 and August 24. They remain immutable. The current Aether audit contract selects `audits/{name}-{timestamp}.md` for this repository assessment; the new path does not migrate or supersede historical source files. Broader documentation layout remains the separate #64 policy scope.

| Historical observation | Current assessment |
| --- | --- |
| Hygiene lacks repository-owned CI and source/reference tooling | **Apparently resolved** for the bounded delivered tools and checked-in/hosted workflow; complete contract regression coverage is still a separate requirement. |
| Organization ADR policy awaits ratification | **Apparently resolved** for policy v1.1.0 and the explicit v1.2.0 naming amendment; do not repeat that approval gate. |
| Roadmaps lag implementation and active context is hard to resume | **Recurring** in the active roadmap handoff; **changed** continuity state after merged authoring work. |
| Repository catalog has a dated inventory and legacy identity | **Recurring**, already explicitly owned by #36; no current whole-organization topology is inferred here. |
| Immutable released consumption and publication are incomplete | **Unable to verify** as completed delivery. Source-admission/deployment limits remain explicit. |
| Canonical architecture combines original and later boundary choices | **Recurring** authority-navigation concern; original decisions and proposed amendments require a truthful current view, not silent status changes. |

Temporary copies and in-memory fixtures were used for negative cases. Existing source checks were executed with their actual arguments; no full-schema execution is inferred from a URL, a valid metaschema, or a happy-path helper result. Local reference tools intentionally remain dependency-free and do not replace native EgoLint production semantics. Their declared subset can still be checked for self-consistency and explicit cross-field policy invariants.

## Overall assessment

Hygiene is a useful working policy owner with partial delivery and qualification. Its main engineering need is to make current reference-validation claims, evidence semantics, selected integration pins, active navigation, and the issue ledger agree. Fixes should extend the existing tools and fixtures, preserve owner boundaries, and leave proposed policy meaning visible for review.

The assessment remains partial because a local passing suite does not establish downstream adoption, live source approval, a published immutable consumer artifact, actual current HTTPS/UI bytes, provider recovery, platform coverage, or a comprehensive security review. None of those limitations prevents beginning the bounded source correctness and navigation repairs identified here.

## Findings summary

| ID | Finding | Severity | History | Primary home at assessment |
| --- | --- | --- | --- | --- |
| AUDIT-001 | Regular CI omits most repository reference-contract regressions | medium | new | Uncreated `CI` |
| AUDIT-002 | Repository identities can escape the selected context-output directory | medium | new | Uncreated `CONTAINMENT` |
| AUDIT-003 | Boundary scanning misses quoted mutable sibling action references | medium | new | Uncreated `BOUNDARY` |
| AUDIT-004 | Continuity exception expiry defaults to the policy's historical update date | medium | new | Uncreated `CLOCK` |
| AUDIT-005 | Presentation can claim passing with only stale or unknown evidence | medium | new | Uncreated `PRESENTATION` |
| AUDIT-006 | ADR reference checks diverge from declared graph, identity, and verification rules | medium | recurring | Uncreated `ADR` |
| AUDIT-007 | Agent-Ready Web accepts malformed or credential-bearing evidence URLs | medium | new | Uncreated `WEB` |
| AUDIT-008 | Release verification omits owner-contract composition and misses inline triggers | medium | new | Uncreated `RELEASE` |
| AUDIT-009 | Publisher configuration and workflow select different Relay generators | medium | new | Existing #47 |
| AUDIT-010 | The active roadmap handoff retains superseded activation and publication assumptions | medium | recurring | Uncreated `DOCS` |
| AUDIT-011 | The active continuity checkpoint selects merged work and a closed tracker | low | changed | Uncreated `DOCS` |
| AUDIT-012 | Broad accepted topology labels obscure proposed ownership amendments | medium | recurring | Uncreated `DOCS` |

Twelve findings: **eleven medium and one low**. Nine proposed issue homes cover the independent current defects/navigation work; existing #47 retains publisher-selection and known source/human acceptance. No high or critical finding was confirmed.


## Findings by severity

### Critical and high severity

None confirmed within the inspected scope. This is not a comprehensive security assessment or a claim that no such defects could exist.

### Medium severity

#### AUDIT-001 — Regular CI omits most repository reference-contract regressions

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** ci-and-automation/testing. **Effort:** small. **Impact:** high. **History:** new.
- **Observation — observed:** The regular Hygiene Pages checks run only test_publication.py and test_decisions.py: eight plus fifteen local tests, compared with the complete 194-test suite. The regular workflow does not invoke the remaining boundary, context/catalog, continuity, Intelligence, presentation, Agent-Ready Web, site-surface, or release-policy test modules as a complete suite. It runs selected direct catalog/context/continuity checks; the manual release workflow only validates its handoff. HYG-Q03 still declares that every catalog/schema change should be validated before merge.
- **Evidence:** [publish-pages.yml:19–34][publication-workflow]; [release-policy.yml:14–32][release-workflow]; ROADMAP.md:106–126. The retained local full-suite command runs 194 tests with zero skips. Two focused workflow test invocations account for 23 of those tests. This is source/command coverage evidence, not a claim that a synthetic regression was merged or that every ignored test would have caught every finding.
- **Why it matters — inferred:** A green publisher check leaves much of the policy owner's actual regression corpus unexercised at the ordinary change boundary. The existing native ADR path and successful publication process do not substitute for every local reference contract.
- **Recommendation — recommended:** Add one bounded read-only full repository regression/contract gate using the existing tests and supported source checks. Keep source admission and publication eligibility separate so a known human gate does not prevent unrelated contract validation. Document the exact coverage and any intentionally excluded capabilities rather than creating one issue per missing test module.
- **Suggested validation:** The full suite executes at the changed revision on ordinary PRs and the supported trusted-branch path; representative deliberate invalid fixtures fail their owning checks; generated-source checks remain reproducible; unavailable optional/native evidence is explicit; no deployment, credential, automatic policy acceptance, or broad new enforcement is introduced by this CI repair.
- **Dependencies or risks:** Independently startable. Preserve source/deployment permissions and the known #47 human-admission gate. This is a finite delivered-reference regression gap, not the entire organization continuous-loop initiative in #58.
- **Primary coverage:** Uncreated `CI` candidate.

#### AUDIT-002 — Repository identities can escape the selected context-output directory

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** catalog/context/filesystem integrity. **Effort:** medium. **Impact:** medium. **History:** new.
- **Observation — observed:** The catalog preflight checks a repository name is nonempty and that full_name/source_url match that supplied name, but does not enforce the name constraint declared by its schema. The context validator does call catalog preflight; that preflight is insufficient. A synthetic repository named ../escaped with matching identity fields, an adjusted count and no consumes validates through both catalog and context checks. render-all exits 0 and writes escaped.md outside the selected output directory.
- **Evidence:** tools/catalog.py:84–95; schemas/repository-catalog.v1.schema.json:44; tools/context.py:53 and 513–521. A temporary-fixture negative case proves the actual CLI output escape. Only harmless temporary paths were used; no private host file or destructive overwrite was exercised.
- **Why it matters — inferred:** A malformed declared identity can cross the command's chosen filesystem boundary while both source validators claim the record is acceptable. Correctly matching one untrusted identity field to another does not establish a safe output component.
- **Recommendation — recommended:** Validate repository identities against the declared semantic constraint before constructing output names and enforce resolved output containment independently. Preserve legitimate configured output directories and existing normal generated bytes.
- **Suggested validation:** Reject traversal, absolute/separator/unsafe identity forms before output; prove no outside temporary write; valid repository identities still render into the selected root; catalog/context preflight and direct rendering agree; generated inventory and ordinary checks remain unchanged.
- **Dependencies or risks:** Independently startable. Repair present source/helper semantics without requiring fresh organization discovery, new policy ratification, or consumer adoption. Do not infer code execution, privilege escalation, secret access, or real data loss from this synthetic write proof.
- **Primary coverage:** Uncreated `CONTAINMENT` candidate.

#### AUDIT-003 — Boundary scanning misses quoted mutable sibling action references

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** dependency boundary validation. **Effort:** medium. **Impact:** medium. **History:** new.
- **Observation — observed:** The boundary scanner's action-reference regular expression recognizes an unquoted uses value but misses equivalent valid quoted YAML. An unquoted egohygiene sibling action pinned to main produces BOUNDARY-002 at line 5; single- or double-quoted forms of the same dependency produce no diagnostic in the bounded fixture.
- **Evidence:** tools/boundaries.py:515–520 and 617; docs/ecosystem/DEPENDENCY_BOUNDARIES.md:31–35 and 96–111. The local negative fixture uses an already-known sibling and the same mutable reference, changing only valid YAML quoting. The source rule explicitly intends to detect mutable sibling workflow/configuration dependencies.
- **Why it matters — inferred:** Equivalent supported configuration syntax can hide a policy violation from a scan that is used as conformance evidence. A clean local result then means less than the documented boundary suggests.
- **Recommendation — recommended:** Recognize the intended supported YAML action/reference forms structurally or through a deliberate quoting-aware parser; keep ordinary documentation links excluded and unknown syntax visible. Preserve the reference scanner's bounded scope rather than claiming exhaustive dependency or originality detection.
- **Suggested validation:** Quoted/unquoted actions and reusable workflows at main/master/develop/trunk/HEAD are diagnosed consistently; immutable full revisions and accepted versioned pins retain intended treatment; comments, normal documentation links and unrelated providers do not become false positives; actual file/line attribution remains correct.
- **Dependencies or risks:** Independently startable. No fleet execution or new external scan is needed. This finding does not establish that a production mutable dependency was executed or that every language/manifest parser is required in this bounded repair.
- **Primary coverage:** Uncreated `BOUNDARY` candidate.

#### AUDIT-004 — Continuity exception expiry defaults to the policy's historical update date

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** applicability/temporal evidence. **Effort:** small. **Impact:** medium. **History:** new.
- **Observation — observed:** For a synthetic approved exception expiring 2026-10-01, a policy updated 2026-09-08 remains structurally valid. The documented default API/CLI resolve exempt; explicitly evaluating the same API at 2026-10-20 resolves required. The CLI exposes no assessment-date input, and its output does not identify the implicit historical date. The baseline profile has no exception records, so an actual wrong repository exemption was not demonstrated.
- **Evidence:** tools/continuity.py:549–556,680–710,817–856; docs/ecosystem/REPOSITORY_CONTINUITY.md:103–105,146–163. The existing API already supports as_of and the proposed profile’s declared rule allows only approved unexpired exceptions. A frozen-date temporary case retains both outcomes in the validation sidecar.
- **Why it matters — inferred:** An operational caller can receive an approved-unexpired label indefinitely after expiry because policy authorship time is being treated as assessment time. Reproducibility does not require hiding the represented date.
- **Recommendation — recommended:** Expose an explicit reproducible assessment date and return it in the assessment. Use that date consistently for expiry validation and applicability, while preserving deliberate historical replay rather than silently moving stored review or approval dates.
- **Suggested validation:** Fixed before/at/after-expiry cases; CLI/API agreement; explicit date provenance; proposed/revoked exceptions never exempt; unchanged frozen inputs remain deterministic. Positive current profiles remain valid.
- **Dependencies or risks:** Independently startable. Preserve approvals and historical dates; do not imply a production enforcement bypass or grant an exemption. Existing #36 covers organization checkpoint/catalog freshness, not this implemented applicability clock.
- **Primary coverage:** Uncreated `CLOCK` candidate.

#### AUDIT-005 — Presentation can claim passing with only stale or unknown evidence

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** policy/evidence semantics. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** The rich presentation fixture validates. Changing every evidence record to freshness stale and assertion unknown, while retaining passing slot, assessment, and badge states, still yields zero errors and derives passing. Reference validation currently derives the summary from slot states and checks evidence enum/list shape without requiring current support for the passing claim.
- **Evidence:** tools/presentation.py:334–354 and 445–468; docs/ecosystem/REPOSITORY_PRESENTATION.md:34–41,118–120,204–213. The policy explicitly says unknown/stale evidence must not appear passing and that passing requires current evidence. A bounded in-memory mutation retains the conflicting declared fields in one input.
- **Why it matters — inferred:** The policy owner's example/reference semantics can accept a badge assessment that contradicts its own evidence. This is not a demand for implicit network verification or a replacement for native EgoLint; the contradiction is explicit in the supplied record.
- **Recommendation — recommended:** Define and enforce evidence-to-slot support rules. A passing required/recommended slot must have qualifying current support. Specify intentional behavior for mixed supporting/unknown evidence without fabricating freshness or requiring every record to be authoritative.
- **Suggested validation:** Current supported passing remains valid; all-stale/all-unknown support cannot retain passing; mixed evidence has deliberate outcomes; top-level status derives from consistent slot states; policy, schemas and downstream fixtures agree.
- **Dependencies or risks:** Independently startable. The profile remains proposed; a correctness proposal does not activate it or certify a real repository. General claim policy in #30/#31 remains distinct from this delivered reference defect.
- **Primary coverage:** Uncreated `PRESENTATION` candidate.

#### AUDIT-006 — ADR reference checks diverge from declared graph, identity, and verification rules

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** ADR policy/reference semantics. **Effort:** medium. **Impact:** medium. **History:** recurring. The proposed-supersession incompatibility is already documented in the selected Aether authoring guide; the additional verification, legacy-reference, and ID-range cases are newly reproduced here.
- **Observation — observed:** Four bounded cases reveal source-policy/reference divergence. A valid accepted predecessor with empty superseded_by plus a proposed replacement with supersedes is rejected with E_SUPERSESSION_BACKLINK even though the policy first calls for proposing a replacement before human acceptance. A verified implementation backed only by approval evidence validates. A dangling three-digit local ADR-999 reference is skipped while equivalent four-digit ADR-0999 is diagnosed. ADR-0000 is accepted despite the declared canonical range 0001–9999.
- **Evidence:** tools/decisions.py:61–66,238–240,318–325,343–388; schemas/architecture-decision.v1.schema.json:34–38,234–251,273–280; accepted POLICY.md sections 4,9,10; VALIDATION.md:64–79. The pinned [decision-record guide:52–66][decision-record-guide] already identifies the older helper’s proposed-supersession incompatibility and directs real consumer replay through native EgoLint/Relay. All fifteen existing decision tests pass; the test rejecting an already-superseded predecessor with a proposed replacement does not cover a still-accepted predecessor plus pending proposal.
- **Why it matters — inferred:** The decoded source checker can reject a valid review-stage graph or accept unsupported verification/unresolved local identity. It need not authenticate a person or fetch evidence to distinguish named evidence kinds or locally supplied references. Pending and effective supersession must not be conflated.
- **Recommendation — recommended:** Model pending replacement separately from human-approved effective supersession, retaining strict backlinks/authority for the latter. Align canonical ID range and supported legacy-reference diagnostics. Require structurally qualifying validation evidence for verified implementation; approval alone is not that evidence. Reconcile policy/schema/reference fixtures deliberately.
- **Suggested validation:** Accepted predecessor plus proposed replacement is represented as pending without changing old disposition; effective supersession requires accepted replacement and reciprocal links; cycles/rejected effective replacements remain invalid; dangling legacy references are visible; 0000 fails while 0001/9999 pass; approval-only verification fails and appropriate validation evidence is accepted structurally.
- **Dependencies or risks:** Independently startable. Preserve historical IDs/dispositions, explicit external pins, and human authority. If intended staged-supersession semantics require clarification, review that ambiguity rather than pretending a proposed replacement is effective. Existing #47 owns concrete ADR-0001 migration/publication; #69 owns the finite Intelligence compatibility/authority set.
- **Primary coverage:** Uncreated `ADR` candidate.

#### AUDIT-007 — Agent-Ready Web accepts malformed or credential-bearing evidence URLs

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** evidence integrity/origin binding. **Effort:** small. **Impact:** medium. **History:** new.
- **Observation — observed:** The Agent-Ready Web evidence-location helper accepts any string beginning https:// without parsing it. Its origin helper rejects some components but still accepts malformed host text and raw browser-normalization ambiguities. Starting with the valid application whole-profile fixture, five malformed or synthetic credential-bearing evidence URL cases and four weak-origin cases yield zero errors. The actual validate-conformance CLI exits 0 and prints agent-ready web valid after bare https:// evidence and a space-containing origin are supplied together.
- **Evidence:** tools/agent_ready_web.py:571–602,1613–1680,1961–2192; docs/ecosystem/AGENT_READY_WEB.md:131–153. No real credential was used and no URL was fetched. The neighboring site-surfaces helper already uses stricter checks at tools/site_surfaces.py:343–377.
- **Why it matters — inferred:** A provenance location can be unusable or contain inline authentication material while the raw origin is not one unambiguous HTTPS browser origin. That weakens the record-validation boundary; it does not prove stored secret disclosure, capability execution, exploitation, or site conformance.
- **Recommendation — recommended:** Validate HTTPS scheme, nonempty valid host, absent userinfo, control/whitespace/backslash ambiguity and deliberate port semantics; retain safe relative evidence locations. Reconcile existing local patterns instead of silently broadening contracts or adding live URL acquisition.
- **Suggested validation:** Valid relative/ordinary HTTPS/IPv6/exact-origin inputs pass; malformed authority, userinfo and browser-ambiguous forms fail through the public CLI; diagnostics identify fields without echoing credentials; shared mechanism-reference/registration-evidence paths get equivalent coverage.
- **Dependencies or risks:** Independently startable. Both policy families remain proposed. Repair does not implement browser capabilities, grant publication, or certify sites. No separate public-site semantic false-pass was confirmed in this review.
- **Primary coverage:** Uncreated `WEB` candidate.

#### AUDIT-008 — Release verification omits owner-contract composition and misses inline triggers

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** release validation/contract composition. **Effort:** medium. **Impact:** medium. **History:** new.
- **Observation — observed:** The documented validate-declaration path and four Taskfile handoffs use local token checks without composing validation of the selected immutable Aether declaration contract. The helper checks task keys but not their declared values and accepts an empty version-authority object. Its intended manual-only trigger check misses a valid inline YAML push mapping. Three independently restored synthetic cases pass: wrong automation.tasks.plan, empty components[0].version_authority, and an inline push trigger.
- **Evidence:** tools/releases.py:419–431,453–483; .tasks/release.yml; .github/workflows/release-policy.yml:21–22; docs/ecosystem/REPOSITORY_RELEASE.md baseline/dogfood sections. The selected Aether schema at `8a2a3d08f3aa9da3847bd5277843506ab855192e` requires version_authority.kind and exact release:plan/prepare/verify/publish task values. Executing jsonschema 4.23.0 Draft202012Validator against those exact owner bytes gives zero errors for the real declaration, rejects missing:plan through its task constant, and rejects the empty authority through required kind. The current checked-in declaration and workflow are valid; no bad release occurred.
- **Why it matters — inferred:** A successful local release plan/verify proves only a subset of the composed baseline while declared authority/task binding or intended trigger semantics can be wrong. Merely linking a schema is not evidence it executed.
- **Recommendation — recommended:** Compose a pinned owner-contract validation result with repository-specific checks rather than copying Aether semantics. Verify declared-to-actual handoff identity and parse supported workflow triggers structurally. If required validation is unavailable, represent incomplete evidence instead of a complete valid-baseline claim.
- **Suggested validation:** Current positive input; wrong task, missing authority kind, unsupported/duplicate fields and actual owner-validator execution; valid manual trigger and commented/inline/flow-style forms; explicit deterministic source/evidence inputs. Preserve read-only preparation and human publication handoff.
- **Dependencies or risks:** Independently startable. Current-v1 correctness need not wait for successor egohygiene/aether#95 or egohygiene/hygiene#65, and broad distribution #29 stays separate. No foundation issue is reopened, publication authorized, or version/lifecycle promoted by this finding.
- **Primary coverage:** Uncreated `RELEASE` candidate.

#### AUDIT-009 — Publisher configuration and workflow select different Relay generators

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** publication/integration/provenance. **Effort:** small. **Impact:** high. **History:** new.
- **Observation — observed:** All five reusable Relay calls in the current publisher workflow select ac2600f4619f64c75a0e499e0540d8f48d516f9c, while publication/site.json and the active runbook still select6cddad3124bdda1b1e3d54a40931f23322b7be26. The seal deliberately compares actual manifest generator revision with configuration. A synthetic transport fixture with the actual workflow revision fails with Relay build revision differs from the reviewed selection; changing only the fixture to the older configuration pin seals successfully.
- **Evidence:** publication/site.json:4; publication/README.md:28–31; publish-pages.yml:38,95,100,112,162; tools/publication.py:121–127; tests/test_publication.py:32–35,103–109. The selected immutable Relay action derives its generator commit from the actual action ref and passes that to its manifest builder. This is a bounded helper/manifest fixture, not a real strict Relay build or deployment.
- **Why it matters — inferred:** After the separate ADR source-admission gate is met, a correctly identified current generator still fails the transport seal. Tests seeded from the configuration prove rejection but do not establish workflow/configuration parity. The seal is properly failing closed; the mismatched selection is the defect.
- **Recommendation — recommended:** Reconcile one compatible exact Relay selection across workflow, consumer configuration and runbook, and add a parity check before source admission. Keep exact-generator sealing rather than relabeling manifest provenance.
- **Suggested validation:** All relevant workflow/action pins agree with the local selection; an actual workflow-selected manifest fixture seals; an unintended generator fails; strict source/build/live acceptance is collected only after independently authorized gates.
- **Dependencies or risks:** Local pin/configuration repair can start independently of human ADR-0001 disposition. Primary home is existing #47, which already owns source/consumer publication truth. No second Pages initiative, approval, review-patch application, release or deployment is proposed here.
- **Primary coverage:** Existing #47.

#### AUDIT-010 — The active roadmap handoff retains superseded activation and publication assumptions

- **Classification:** documentation gap. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** current navigation/roadmap truth. **Effort:** medium. **Impact:** medium. **History:** recurring.
- **Observation — observed:** The root roadmap's dated August block is still described as the issue-generation and visual-roadmap handoff. Its current gate is to merge ADR-0002 activation, even though HYG-Q02 in that same document records ratification complete. It retains no-CI/publication observations and the earlier central-roadmap route selection without a superseding current checkpoint explaining the actual repository-owned Hygiene Intelligence publisher.
- **Evidence:** ROADMAP.md:29–53,80–126; README.md:10–15; current publication/runbook/workflow sources. HYG-Q03's full every-catalog/schema-before-merge acceptance is distinct from the bounded publisher checks. The earlier date label correctly preserves when old observations occurred; the gap is using the old block as the only active handoff, not that history was false at the time.
- **Why it matters — inferred:** A new worker or roadmap projection can select delivered activation work or obsolete publication assumptions rather than current source admission and the tactical backlog. The older central aggregate route and current repository-owned Intelligence route also need an explicit relationship, not an assumed global replacement.
- **Recommendation — recommended:** Reconcile one explicitly current execution checkpoint while retaining stable HYG-Q identities, strategic context, and historical citations. Link the complete repository execution tracker. Refresh counts only where the prose asserts current evidence; keep full CI, source admission, process success, deployment and live acceptance separate.
- **Suggested validation:** A fresh README→AGENTS→ROADMAP→tactical-ledger walkthrough selects the actual next checkpoint; links resolve; represented revisions and counts agree; accepted history and source identity remain reopenable. No blanket completion of HYG-Q03 follows from a green Pages workflow.
- **Dependencies or risks:** Independently startable factual/navigation repair. DOCS is distinct from #64's organization-wide layout policy; #36 retains catalog truth; #47 retains actual source approval/publication acceptance. No file relocation, fleet migration or route/policy mutation is implied.
- **Primary coverage:** Uncreated `DOCS` candidate.

#### AUDIT-012 — Broad accepted topology labels obscure proposed ownership amendments

- **Classification:** architectural concern. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** authority/lifecycle navigation. **Effort:** medium. **Impact:** medium. **History:** recurring.
- **Observation — observed:** The canonical ecosystem architecture is labeled accepted v0.1/last reconciled August 18 while its six-plane view includes Filament ownership, Sanctuary incubation and Empathy's strict golden role. Preserved ADR-0001 still states five planes and Empathy as a bounded incubator. ADR-0003/0004 describing later changes remain proposed with null approval. The diagram guide attributes written boundaries to accepted ADR-0001 and its PlantUML title labels the resulting topology accepted v0.1 without per-amendment status.
- **Evidence:** docs/ecosystem/ARCHITECTURE.md:1–5,21,35–56,96–108; original ADR-0001:21–35; ADR-0003:5,24,39,58–83; ADR-0004:5,27,42,55–77; diagram README:3–14; ecosystem.puml:10. The source-backfill packet explicitly preserves dated wording and says merges do not ratify proposals.
- **Why it matters — inferred:** Canonical narrative/visual labels do not directly distinguish original accepted context, later proposals and observed implementation. This is an authority-view inconsistency; original human instructions for every historical change were not comprehensively reconstructed here, so the audit does not declare all changes unauthorized or invalidate their implementation.
- **Recommendation — recommended:** Provide a concise current authority/evidence map and qualify proposed amendments in active prose and diagram metadata. Preserve records and their present dispositions. Route any needed human approval or successor through existing #47's decision inventory and the proper decision process; do not silently rewrite accepted rationale or mark proposals accepted.
- **Suggested validation:** The canonical entry path names the exact source, accepted/proposed/observed state, and approval evidence or uncertainty for consequential amendments; diagrams agree; unchanged historical citations reopen; native conformance and human approval stay distinct.
- **Dependencies or risks:** DOCS can clarify labels/evidence now; #47 retains actual historical authority/metadata and source admission, #59 general future coherence applicability, and #69 Intelligence-specific support-set authority. No duplicate approval of already-ratified ADR policy v1.2.0 and no new blanket architecture-ratification issue is warranted.
- **Primary coverage:** Uncreated `DOCS` candidate.



### Low severity

#### AUDIT-011 — The active continuity checkpoint selects merged work and a closed tracker

- **Classification:** documentation gap. **Severity:** low. **Confidence:** high. **Status:** confirmed. **Area:** continuity/resumption. **Effort:** small. **Impact:** medium. **History:** changed.
- **Observation — observed:** Active CONTINUITY selects merging the four-digit adoption, closing #73 and preserving egohygiene/identity#114 as a parallel draft. Verified public provider state shows Hygiene PR #74 merged 2026-10-18T21:31:09Z, issue #73 closed completed, and Identity PR #114 merged 2026-10-19T10:02:22Z. Older time-qualified base/date and null candidate fields are not themselves invalid.
- **Evidence:** CONTINUITY.md:35–74,117–147; selected live issue/PR reads retained in the sidecar. Verified main remains the frozen source. The next action and current prose, rather than a historical receipt, are superseded by those merges.
- **Why it matters — inferred:** A resumed worker must disprove its selected next step before returning to actual work. Correct AGENTS live-reconciliation instructions limit the risk; this is not proof of malformed continuity or unauthorized operation.
- **Recommendation — recommended:** The separately authorized repository-changing publication workflow should Refresh/Verify the checkpoint after domain checks and before PR handoff, retaining exact source/candidate/live states, limitations, parallel work and a viable next action. The read-only auditor grants no mutation authority.
- **Suggested validation:** Actual front matter validates against the selected Aether schema; twelve headings and budgets hold; privacy/links pass; fresh live state and selected next action agree; proposed publication is not claimed merged.
- **Dependencies or risks:** Independently startable. DOCS owns any remaining current-entry-point repair; if the audit-publication PR proposes a refresh, this immutable baseline finding remains dated evidence until actual merge/remediation is separately verified.
- **Primary coverage:** Uncreated `DOCS` candidate.



## Positive observations

- **Observed:** policy ownership is distinct from Aether guidance, Holon materialization, EgoLint semantics, Relay execution, Observatory evidence, Pace convergence, and consumer facts/publication. The audit did not find a need to centralize those implementations in Hygiene.
- **Observed:** 194 local tests run without skips and the retained positive CLI checks pass. Existing focused fixtures make bounded negative-case repairs possible without inventing another toolchain.
- **Observed:** the eighteen JSON Schema documents pass metaschema validation. That is a useful schema-authoring check, with instance and semantic coverage reported separately.
- **Observed:** accepted ADR policy and naming authorization preserve original rationale, dates, migration maps, and human lifecycle authority. The canonical fourteen-record index links actual ratification and proposed records explicitly.
- **Observed:** the publisher preserves exact immutable inputs, default read-only permissions, source admission, exact artifact transport, digest/inventory sealing, recovery preparation, and byte-level verification boundaries. Its current source gate prevents an invalid ADR corpus from being deployed.
- **Observed:** public-site semantics already distinguish applicability, availability, validation, maturity, publication, and capability authority. A structurally valid evidence record is not automatically a conformant live site.
- **Observed:** the repository contains no tracked staging corpus. The old Empathy migration inventories are historical planning inputs, not current Hygiene files to evacuate.
- **Observed:** bounded inline-relative Markdown destination checking found zero missing paths; external URLs, anchors, placeholders, and exhaustive Markdown syntax were outside that check.
- **Observed:** a temporary Excalidraw regeneration is byte-identical to the tracked artifact, SHA-256 `6373bcb8e5a65dc7925347061d1bceebcc51e5505cdf0769f030c88a4f69ed15`.

## Opportunities, scope boundaries, and existing work

| Area | Observed boundary / unresolved work | Existing home or next proof |
| --- | --- | --- |
| Live repository catalog | 27 dated records, legacy website identity and known later inventory reconciliation. No new whole-organization discovery was performed. | #36 owns authorized discovery/public allowlist, aliases, current gates, cadence, privacy and freshness. Do not duplicate it or publish inferred protected topology. |
| Intelligence authority | Delivered alpha source/interfaces remain proposed; ADR policy 1.2.0 is separately accepted. | #69 freezes the finite supported matrix, exact compatibility and human disposition or documented prerelease support. Existing supported ADR consumers need not wait for every broader policy. |
| Original ADR-0001 | Original bytes and unapplied null-approval review material remain preserved; native admission is invalid. | #47 owns actual human disposition, metadata, exact source admission, immutable build, live verification and recovery. This audit cannot fill that approval. |
| Global documentation layout | Current eighteen-document root set concerns Hygiene's repository; broader docs/architecture/applicability policy is proposed. | #64 owns the reviewed location policy and Aether/Empathy/consumer pilots. Immediate factual navigation is the bounded DOCS candidate; no bulk move is needed for it. |
| Architecture-coherence review | Reusable policy and human-review record semantics remain open. | #59 and egohygiene/aether#87 remain separate policy/guidance owners. AUDIT-012 asks for truthful current labels/evidence, not automatic ratification. |
| Foundation/migration target prose | docs/foundation is absent, and MIGRATION_PLAN describes a future ledger/schema. No current Hygiene staging corpus exists. | Reconcile useful residual scope with #36/#58/#61/#64 and consumer-owned migration ledgers before creating ceremonial files or a duplicate database. These targets alone do not establish mandatory v1 defects. |
| Native conformance breadth | Exact native owner validation also emits automatic release/portability diagnostics outside its focused ADR scope. | Retain compatibility/availability distinctions; inspect intended applicability and exact pins before classifying every diagnostic as a new Hygiene defect. Do not call the repository native-clean or hide the results behind194 green tests. |
| Initiative versus execution | #31/#43/#58/#61 are cross-repository programs; #60 defines future organization strategic-roadmap composition. | Use one new repository-execution parent, preserving scope, comments, owner issues and the human-owned organization focus queue. |


## Original 31-issue coverage and recommended journey

At baseline, all 31 issues were open, each native child summary was 0, and every parent GET explicitly returned No parent issue found. All 31 comment collections were fetched; six comments across #58 (three), #17 (two), and #23 (one) were read. Their requirements remain part of owning scope. None of the existing initiative issues is a complete repository-backlog parent; creating a new tactical parent preserves their original coordination role.

The table uses proposed focus order. `*` means a named unmet prerequisite or explicit gate before the **full outcome**, while bounded preparation may begin. An unstarred item is independently startable, not automatically small, high priority, merge-ready, or accepted policy. Dependency detail belongs in the owning issue for the clean live roadmap; this dated assessment records the reasoning behind the classification.

| Order | Original issue | * | Delivered/partial foundation | Next bounded checkpoint |
| --- | --- | --- | --- | --- |
| 1 | [#36](https://github.com/egohygiene/hygiene/issues/36) Define recurring organization health checkpoints and keep the repository catalog live | — | Current catalog/context/boundary source, generated views and executable tools exist; the catalog retains its August observation boundary, legacy website identity and unresolved inventory work. | Reconcile a fresh authorized inventory/public allowlist, rename/alias semantics and first gates; define a bounded reproducible freshness/checkpoint policy using the existing Aether auditor semantics. |
| 2 | [#69](https://github.com/egohygiene/hygiene/issues/69) 🏗️ [architecture] Freeze the Intelligence authority and compatibility gate | — | Closed #19/#25 delivered Intelligence/vocabulary/coverage and surface source contracts, which remain proposed. The current ADR policy is accepted 1.2.0, not the issue's older 1.1.0 wording. | Freeze the finite supported-version/authority matrix, prepare a human disposition or documented prerelease-support boundary, then give exact compatible upgrade/rollback handoffs. |
| 3 | [#64](https://github.com/egohygiene/hygiene/issues/64) 📚 Define canonical documentation layout, architecture navigation, and agent entry points | — | Repository-presentation, continuity and architecture-authoring foundations exist; the issue contains an explicit October 17 proposed layout and scoped consumer sequence. | Settle one small documentation-location/applicability proposal with synthetic legacy/new-layout examples; reconcile affected Aether/Empathy/consumer paths only after review. |
| 4 | [#37](https://github.com/egohygiene/hygiene/issues/37) Define the canonical commit, pull-request title, and change-history contract | — | EgoLint's existing commit validator and several divergent consumer conventions provide inputs; no current canonical Hygiene commit/change-history profile exists. | Define one prospective versioned subject/type/emoji/release-semantics contract with bot/merge/revert/breaking fixtures and map existing configurations. |
| 5 | [#29](https://github.com/egohygiene/hygiene/issues/29) policy(distribution): define the universal tool distribution and native-installability profile | — | egohygiene/aether#61, egohygiene/hygiene#27 and egohygiene/relay#4, egohygiene/relay#47 provide current release foundations; target/channel policy remains open. | Define applicability, target/channel/support/evidence and symbolic publisher-ownership vocabulary with contrasting tool fixtures. |
| 6 | [#26](https://github.com/egohygiene/hygiene/issues/26) Define the organization software supply-chain assurance profile | — | Existing release and claim-safety foundations give bounded inputs; no dedicated supply-chain assurance profile is currently delivered. | Propose one applicability/evidence control schema spanning source/build/package/container subjects, with synthetic positive/unknown/exception cases and producer-owned interfaces. |
| 7 | [#30](https://github.com/egohygiene/hygiene/issues/30) Define an evidence-backed quantitative and compatibility claims policy | — | Repository Intelligence, presentation/badge, Aether provenance and current release sources exist; a general quantitative/compatibility claim envelope remains open. | Define a compact claim/evidence-state/freshness schema and four falsifiable synthetic benchmark/compatibility/reported/stale fixtures. |
| 8 | [#59](https://github.com/egohygiene/hygiene/issues/59) Define architecture-coherence ratification policy and review applicability | — | Existing ADR policy and Aether reflector/anchor/audit foundations provide semantics; no Hygiene coherence applicability/ratification profile is delivered. | Define review applicability, material triggers, human-only disposition, represented revisions and stale/deferred/unknown fixtures. |
| 9 | [#41](https://github.com/egohygiene/hygiene/issues/41) Define repository applicability for diagnosis records | — | egohygiene/aether#74 is completed and [Aether PR #75](https://github.com/egohygiene/aether/pull/75) merged; canonical diagnosis-record/spec/authoring artifacts already exist. egohygiene/hygiene#15, egohygiene/hygiene#19 foundations are completed. | Define applicability, path declarations, pinning, privacy/retention/index freshness and optional/unknown/no-record states with synthetic consumers. |
| 10 | [#44](https://github.com/egohygiene/hygiene/issues/44) 🏠 Define workstation configuration and OS provisioning ownership boundaries | — | Canonical architecture names Realm provisioning and Mantle shell-runtime boundaries, while legacy user/tool/OS configuration ownership remains an explicit design question. | Inventory finite configuration classes and propose one ownership/disposition map plus portable migration guidance. |
| 11 | [#49](https://github.com/egohygiene/hygiene/issues/49) Build a corpus-assisted canonical configuration synthesis workflow | — | The issue proposes corpus acquisition, official-document reconciliation and config synthesis; no dedicated implementation is delivered. | First decide the semantic owner and bounded first-file pilot, then define source provenance/option matrix/native validation/output promotion checkpoints. |
| 12 | [#17](https://github.com/egohygiene/hygiene/issues/17) Define the universal public-site legal, policy, trust, and disclosure profile | — | Agent-Ready Web #16, route registry #25 and egohygiene/holon#4 foundations are delivered/proposed with explicit limits. No complete legal/trust publication policy is delivered. | Define applicability and canonical surface aliases/content/review evidence through a small synthetic policy package; preserve all comments' Impressum, privacy-signal and AI Reference requirements. |
| 13 | [#23](https://github.com/egohygiene/hygiene/issues/23) Define a people-first helpful-content and editorial quality profile | — | The canonical helpful-content profile remains open; egohygiene/aether#56 is its downstream authoring consumer. Editorial/legal surfaces are separately owned by #17. | Propose a source-mapped editorial applicability/review/freshness profile with good/partial/stale/archived fixtures and human judgment separate from checks. |
| 14 | [#34](https://github.com/egohygiene/hygiene/issues/34) Evaluate queryable field-level encryption for applicable Postgres workloads | — | No queryable-encryption adoption is established. The issue is an optional applicability/threat-model evaluation with a synthetic pilot only if a qualifying Postgres workload exists. | Inventory qualifying workloads and compare simpler baselines; record adopt/adapt/defer/reject or not-applicable with bounded evidence before any implementation. |
| 15 | [#35](https://github.com/egohygiene/hygiene/issues/35) Extend the assurance profile with ISO/IEC 27001 and ISO/IEC 27701 readiness | — | egohygiene/empathy#51 and the public Trust Center/security/legal issue family supply existing assurance intent; no specific ISO readiness mapping is delivered here. | Propose a finite versioned ISO applicability/control mapping and synthetic readiness/certification/freshness records, explicitly reconciling canonical normative versus template ownership. |
| 16 | [#33](https://github.com/egohygiene/hygiene/issues/33) Define an organization-wide Hugging Face presence and publication profile | — | egohygiene/reflector#108, egohygiene/reflector#130 are completed experience inputs, while the organization-wide Hugging Face policy/inventory remains open. | Define applicable artifact classes, card/source/version/privacy/publication rules and two synthetic or separately approved canaries; preserve not-applicable outcomes. |
| 17 | [#39](https://github.com/egohygiene/hygiene/issues/39) Define the confidential AI workload and information-flow policy | — | No dedicated multi-dimensional information-classification/flow policy is delivered; current public/private owner boundaries and proposed profile restrictions provide inputs. | Define independent visibility/persistence/execution/publication/review dimensions, sensitivity inheritance and human declassification with synthetic denial/unknown examples. |
| 18 | [#62](https://github.com/egohygiene/hygiene/issues/62) Define the canonical System Status and incident-communication contract | — | Closed #25 supplies a proposed route registry and ownership foundation; egohygiene/relay#41/egohygiene/pace#15 remain downstream status implementation/adoption work. | Define provider-neutral status/component/incident/freshness/disclosure schema and honest unmonitored/unknown/stale/redacted fixtures. |
| 19 | [#66](https://github.com/egohygiene/hygiene/issues/66) 🏆 [Progress 1/4] Define achievement rules and register the Progress surface | — | egohygiene/hygiene#25 and egohygiene/observatory#25 foundations are completed; achievements/rule semantics and the optional Progress surface remain open. | Register the proposed optional route/rule catalog and scope/denominator/award-history examples while retaining actual lifecycle authority. |
| 20 | [#60](https://github.com/egohygiene/hygiene/issues/60) Define the canonical organization roadmap and repository-roadmap inheritance contract | — | Closed #19 supplies graph/provenance vocabulary and repository-roadmap source exists; a separate canonical organization strategic-roadmap contract is not delivered. | Define organization initiative identity/composition/privacy/state metadata with synthetic cross-repo and repository-only cases, plus a stable path separate from Hygiene's own strategic roadmap. |
| 21 | [#42](https://github.com/egohygiene/hygiene/issues/42) Define the portable organization-foundation contract and platform distribution lock | — | Existing semantic-capability/manifest materialization and owner contracts provide concrete inputs; no portable organization-profile/distribution-lock schema exists. | Define organization-neutral consumer/profile/compatibility-lock/resolved-state contracts and synthetic non-Ego fixtures; make unavailable producers explicit and bound the later private pilot. |
| 22 | [#47](https://github.com/egohygiene/hygiene/issues/47) Backfill repository ADR history and enable continuous decision capture | * | The October 18 checkpoint accurately records completed policy 1.2/four-digit/current native authoring and publisher wiring. ADR-0001 lacks structured metadata and durable historical architecture approval; native admission remains invalid and build/deploy skipped. | Obtain the specifically missing human disposition, finish the preserved ADR-0001 metadata review, reconcile current publisher pins, then rerun exact native/admission/build/live verification and recovery proof. |
| 23 | [#32](https://github.com/egohygiene/hygiene/issues/32) Define an evidence-based application architecture quality profile | * | The application architecture quality profile remains open; it explicitly must reuse general claim/evidence semantics from #30. | After pinning compatible #30 evidence semantics, define applicability and objective-versus-human criteria with deployable/CLI/static contrasting fixtures. |
| 24 | [#40](https://github.com/egohygiene/hygiene/issues/40) Define a verifiable local AI isolation and privacy assurance profile | * | No local-AI assurance profile is delivered; it normatively translates confidential policy #39 and requires claims and supply-chain evidence. | Consume compatible #39/#30/#26 inputs, then map concrete control IDs to independently testable network/storage/runtime/lifecycle/negative evidence fixtures. |
| 25 | [#65](https://github.com/egohygiene/hygiene/issues/65) 📜 [Release checkpoint 3] Review the common release policy and migration gates | * | Closed egohygiene/hygiene#27 and egohygiene/aether#61 provide the current proposed v1 release baseline; this issue owns the successor common release policy. | Consume the reviewed compatible egohygiene/aether#95 design, reconcile one proposed common release applicability/migration policy, then give staged adoption and rollback handoffs. |
| 26 | [#38](https://github.com/egohygiene/hygiene/issues/38) Design a provenance-preserving commit-history normalization program | * | Prospective canonical commit policy and several migration assurances remain open; no history rewrite is authorized. | After relevant #37/audit/governance/provenance inputs exist, produce repository-risk/eligibility and immutable mappings/backup/rollback plans, then a separately authorized disposable pilot. |
| 27 | [#31](https://github.com/egohygiene/hygiene/issues/31) Roadmap: make compatibility, evaluation, and agent claims inspectable | * | The nine-seed disposition/ownership program exists; its policy, capability, lint, comparison, orientation and benchmark children remain open. | Track #30 then egohygiene/aether#64 and the existing owner issues to an actual falsifiable integration/evaluation proof; preserve negative/unknown outcomes. |
| 28 | [#58](https://github.com/egohygiene/hygiene/issues/58) Roadmap: make audits, hygiene, and organization intelligence a continuous control loop | * | The architectural continuous-loop program and three comments map canonical audit/evidence/UI/rollout owners; several bounded foundations exist but the complete loop remains unproved. | Consume the existing Aether/Reflector/Observatory/Relay/Pace issues in bounded lanes; prove one safe audit-to-candidate-to-reviewed-work feedback path when inputs are ready. |
| 29 | [#61](https://github.com/egohygiene/hygiene/issues/61) Roadmap: converge the federated Second Brain through reference journeys | * | The federated Second Brain steering issue contains two explicit reference journeys, current owner map, privacy invariants and a low-priority environment clarification. Mindcap bookmark acquisition foundation egohygiene/mindcap#23 is completed. | Recheck its existing small closeout queue, ratify owning boundaries, stabilize source/knowledge/context handoffs and prove the bounded synthetic bookmark journey before any private pilot or recurring capture. |
| 30 | [#43](https://github.com/egohygiene/hygiene/issues/43) Roadmap: prove Ego Hygiene as a reusable organization platform with a second consumer | * | The reusable-platform/second-consumer program exists. Its current focus appendix still calls [organization PR #43](https://github.com/egohygiene/.github/pull/43) and [Relay PR #110](https://github.com/egohygiene/relay/pull/110) review candidates, although both merged. | Consume #42's portable profile and owner-produced capability interfaces, prove synthetic external intent, then bounded private second-organization and greenfield/recovery evidence. |
| 31 | [#7](https://github.com/egohygiene/hygiene/issues/7) Architect a self-hostable organization compiler and hybrid business model | — | All named nondeferred foundations #2/#5, egohygiene/holon#1, egohygiene/holon#3, egohygiene/aether#36, egohygiene/realm#2, egohygiene/pace#1 and egohygiene/observatory#1 are completed. The issue is explicitly P3 long-term product/architecture design, not implementation. | When deliberately selected, define product journey, target users, self-hosted/business/trust architecture and the smallest future vertical slice using existing owners. |

**22 original issues are independently startable; nine have gated full outcomes.** The nine independent audit-gap candidates would bring the complete work ledger to 40 items: 31 independently startable and 9 marked with `*`, excluding the new parent. The priority of a long-term design such as #7 is distinct from whether its named foundations are delivered. Preserve the text-based program/parent references in #69/#66/#65 when adding native repository hierarchy.


### Recommended finite journey

1. **Establish trustworthy current checks:** CI, CONTAINMENT, BOUNDARY, CLOCK, PRESENTATION, ADR, WEB and RELEASE. These are present-source correctness/coverage repairs, not prerequisites invented from every related downstream issue.
2. **Restore current navigation and an explicit public owner map:** DOCS plus existing #36. Preserve dated audits, stable strategic step IDs, original decisions and authorized inventory/privacy boundaries.
3. **Finish the finite current support/publication checkpoint:** #69's compatible authority matrix and #47's specific human/source gate, publisher-pin reconciliation, strict build/live verification/recovery. Preparation can run in parallel; actual human disposition and publication retain their own authorization.
4. **Advance policy foundations one bounded issue at a time:** use the original sequence in the table, distinguishing policy design from downstream implementation/adoption. #64/#37/#29/#26/#30/#59/#41 unblock reusable work without requiring all consumers first.
5. **Keep broader programs and optional research visible:** preserve all 31 original scopes. #31/#58/#61/#43 remain coordination programs; #7 stays long-term P3 product/architecture work despite delivered named entry foundations. None is a blanket requirement to finish every platform feature before useful product development.

A proposed usable baseline is finite: honest current sources, complete regression evidence, corrected local reference semantics, a current authorized registry/support view, and the smallest valid publication/consumer proof after its specific human gates. It does not require every speculative profile, automatic agent execution, a hosted organization compiler, full fleet adoption, or historical commit rewriting.

Reconciliation must retain #17's two legal/trust comments and #23's downstream authoring comment; preserve #58's three architecture/visual-control-plane comments and its separate organization execution owner. #41 should consume delivered Aether diagnosis artifacts, #43 should recognize merged organization/Relay preparation PRs, and #69 should select current ADR policy 1.2.0 without pretending Intelligence profiles were ratified by implementation.


## Suggested backlog and no-duplicate decisions

The following keys are **uncreated candidates in this dated assessment**, not issue numbers or completed repairs. The later authorized live roadmap should map the created numbers and retain exactly one primary remediation home per finding.

| Primary home | Findings | Bounded outcome |
| --- | --- | --- |
| `CI` — uncreated | AUDIT-001 | Full repository regression/reference-contract gate with honest coverage and separate publication authority. |
| `CONTAINMENT` — uncreated | AUDIT-002 | Declared repository identity validation and independent resolved context-output containment. |
| `BOUNDARY` — uncreated | AUDIT-003 | Equivalent quoted/unquoted mutable sibling references receive equivalent supported diagnostics. |
| `CLOCK` — uncreated | AUDIT-004 | Explicit reproducible assessment date, expiry and CLI/API evidence agreement. |
| `PRESENTATION` — uncreated | AUDIT-005 | Passing claims require qualifying current support; unknown/stale remain truthful. |
| `ADR` — uncreated | AUDIT-006 | Pending/effective supersession, evidence-kind, supported legacy-reference and canonical-ID range parity. |
| `WEB` — uncreated | AUDIT-007 | Valid evidence URL/exact-origin syntax and safe non-echoing diagnostics. |
| `RELEASE` — uncreated | AUDIT-008 | Actual pinned owner-contract composition plus declared handoff/trigger validation. |
| `DOCS` — uncreated | AUDIT-010–012 | Current navigation/handoff and qualified architecture-authority labels; preserve historical decisions and route actual human disposition through #47. |
| Existing #47 | AUDIT-009 | One compatible exact Relay generator selection, parity check, preserved strict seal and existing source/publication acceptance. |

Existing #36, #47, #59, #64 and #69 are not replaced by these candidates. Closed foundation issues remain historical delivery evidence; a missing negative case does not warrant reopening them. Issue creation and repository publication are separately authorized reconciliation outputs, not automatic behavior of the read-only auditor.


## Validation notes

| Check | Observed result | Practical limit |
| --- | --- | --- |
| Full local unit suite | 194 tests, zero skips, exit 0 | Local source/fixtures; not a live policy or deployment assertion. |
| Retained baseline commands | 24 commands, all exit 0 | Happy paths, fixture validators, review-patch syntax, generated views, and clean source status; negative cases expose separate limitations. |
| JSON Schema metaschemas | All 18 pass | Schema-document validity only; not instance validation or full semantic/reference parity. |
| Catalog and boundary generated views | Current source renders match tracked views | Does not make the dated repository inventory current. |
| Boundary scan | No supported violation reported | Supported local scan, not provenance originality, exhaustive dependency analysis, or security certification. |
| Continuity applicability and repository check | Pass | Does not reconcile live next-action truth or prove current exception expiry without the correct assessment input. |
| ADR review patch | `git apply --check --unidiff-zero` exits 0 | Syntax/preimage check only; the patch remains unapplied and approval remains absent. |
| Diagram regeneration | Exit 0; byte-identical | Deterministic generated diagram bytes, not architecture ratification. |
| Exact-main Pages run | Run 39168195558 overall success | Source-evidence/admission process ran; site build and deploy jobs skipped. |
| Bounded mutation reproductions | Outcomes described in findings and sidecar | A reproduced defect is not a product-readiness pass. All writes used temporary fixtures. |
| Pinned Relay native collector suite | 31 tests, zero skips, exit 0 | Separate from Hygiene’s 194-test suite; proves bounded runtime/review behavior, not valid source or deployment. |
| Exact owner release-schema counterexamples | Baseline valid; wrong task and empty authority rejected | Tests the actual selected Aether schema; does not imply every current declaration contract has complete instance coverage. |
| Native source admission | Exact source-pinned EgoLint d917ea524962639494e5bb4b3196192238ba57d9 runs and exits 1; ADR status invalid with13 metadata-bearing records/16 diagnostics and zero owner-contract mismatches. | Existing #47 owns real ADR-0001 metadata/human disposition and publication proof. |


### Native interpretation

The native binary was built with frozen inputs using installed Rust/Cargo 1.97.1; source toolchain 1.85.1 was not executed. Its focused Intelligence report represents the audited commit, inspects13 metadata-bearing ADRs and99commits, and returns16 diagnostics: two explicit unknown adoption surfaces, one missing ADR metadata diagnostic, one index diagnostic, and twelve lineage diagnostics. The original ADR-0001 identity cannot enter that graph; this known gap remains #47, with **zero owner-contract mismatches**.

The direct CLI also evaluates automatic portability and release checks. The normalized run is partial and reports 25 findings across three tools; the release assessment is invalid/incomplete with 6 checks completed, 1 failed, and 1 unavailable external-evidence item. Those outputs are retained as compatibility/applicability evidence, not silently ignored or automatically promoted into 25 new Hygiene bugs. No container lint engine, full security scan, actual source approval, or live deployment is established by this native invocation.

The actual immutable Relay `ac2600f4619f64c75a0e499e0540d8f48d516f9c` review pipeline was also prepared with its exact locked owner files and offline native build. The separate native collector suite ran **31 tests with zero skips**, exit 0. Actual collection against the audited source returned **2**, retained 23 source blobs and 19 bounded diagnostics, and returned an invalid/partial decision review with publication denied. Review envelopes deny publication by design; valid projection/coverage shape and normalized Observatory candidate output do not make those candidates admitted production inputs. The declared external decision key is not an independently acquired target observation. No source approval or deployment occurred.

Exact-main [run 39168195558](https://github.com/egohygiene/hygiene/actions/runs/39168195558) succeeds for publisher checks, native source evidence collection, and admission evaluation. Its **Build admitted immutable site** and **Deploy and verify canonical HTTPS bytes** jobs are skipped. AUDIT-009 is a separate latent pin defect behind the known source gate, not the observed cause of those skips.

## Deferred scope, uncertainty, and continuation

- **Unverified:** current full-organization inventory, protected topology, every downstream consumer, fleet applicability, or complete cross-repository issue completion. This repository audit does not replace the organization campaigns in #58/#61/#43/#31.
- **Unverified:** actual live HTTPS site payload/UI/accessibility, deployment recovery, environment approval settings, authenticated publication, or broad platform canaries. GitHub release collection and local Git tag inspection observed no releases or tags; absence of those artifacts is known, not inferred from a failed access attempt. No workflow dispatch, deployment, site setting, credential use, tag, or registry write was performed.
- **Unverified:** comprehensive security scanning, third-party advisory review, fuzzing, every external URL, complete heading anchors, or malformed-input coverage beyond the retained counterexamples.
- **Observed:** current ADR policy v1.2.0 is accepted, while other profiles and amendments keep their own lifecycle. Correctness repairs must not silently activate proposed policy or infer new human approval.
- **Recommended continuation:** repair focused evidence/contract defects, restore current navigation, reconcile #36's authorized public catalog, resolve the specific remaining #47 human/source gate, and keep source checks, release eligibility, hosted process success, deployment, and adoption separately evidenced.

## Evidence index

The [normalized validation sidecar](data/hygiene-completeness-20261020T040335Z.validation.json) retains source identity, executed command receipts, bounded reproduction results, source/native pins, inventory, hosted observations, and limits. Raw intermediate logs and private execution locations are not public deliverables merely because their integrity digests are retained.

| Evidence group | Frozen source or observed record | Meaning |
| --- | --- | --- |
| Repository instructions | [AGENTS][agents], [architecture][ecosystem-architecture], [agent context][agent-context], [boundaries][boundary-guide] | Scope, owner boundaries, precedence, and current policy navigation. |
| Audit procedure | [Auditor 2.0.0][auditor], [audit skill 1.1.0][audit-skill] | Finding model, evidence labels, immutability, read-only collection and partial reporting. |
| Registry/context/boundary tools | [catalog tool][catalog-tool], [context tool][context-tool], [boundary tool][boundary-tool], [catalog][catalog], [boundary register][boundary-register] | Current implemented reference behavior and fixture counterexamples. |
| Intelligence | [Intelligence tool][intelligence-tool], [contract][intelligence-guide], [coverage][intelligence-coverage] | Snapshot identity/coverage semantics and proposed owner boundaries. |
| Policy/evidence helpers | [presentation][presentation-tool], [continuity][continuity-tool], [ADR reference][decisions-tool], [Agent-Ready Web][arw-tool], [site surfaces][surfaces-tool] | Current semantic checks and bounded malformed/contradictory inputs. |
| Release/publication | [release tool][release-tool], [publisher][publication-tool], [consumer workflow][publication-workflow], [release declaration][release-declaration], [runbook][publication-guide] | Current selected pins, source gate, local contract composition and hosted process/delivery distinctions. |
| Authority/history | [Policy v1.2.0][adr-policy], [ratification][ratification], [canonical ADR index][adr-index], [original ADR-0001][adr-one], [root roadmap][roadmap], [continuity][continuity] | Accepted/proposed/historical/current distinctions. |
| Historical audits | [August 19][audit-aug19], [August 24][audit-aug24] | Original organization observations and recurring/resolved/unverified history; not rewritten by this assessment. |
| Provider observations | [exact-main run 39168195558](https://github.com/egohygiene/hygiene/actions/runs/39168195558), initial issue bodies/comments/relationships and selected upstream statuses in sidecar | Dated observed workflow and work-ledger state, not permanent proof. |

[agents]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/AGENTS.md
[ecosystem-architecture]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/ecosystem/ARCHITECTURE.md
[agent-context]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/ecosystem/AGENT_CONTEXT.md
[boundary-guide]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/ecosystem/DEPENDENCY_BOUNDARIES.md
[catalog-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/catalog.py
[context-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/context.py
[boundary-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/boundaries.py
[catalog]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/catalog/repositories.yaml
[boundary-register]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/catalog/dependency-boundaries.yaml
[intelligence-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/intelligence.py
[intelligence-guide]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/ecosystem/REPOSITORY_INTELLIGENCE.md
[intelligence-coverage]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/ecosystem/REPOSITORY_INTELLIGENCE_COVERAGE.md
[presentation-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/presentation.py
[continuity-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/continuity.py
[decisions-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/decisions.py
[arw-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/agent_ready_web.py
[surfaces-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/site_surfaces.py
[release-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/releases.py
[publication-tool]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/tools/publication.py
[publication-workflow]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/.github/workflows/publish-pages.yml
[release-workflow]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/.github/workflows/release-policy.yml
[release-declaration]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/.egohygiene/release.json
[publication-guide]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/publication/README.md
[adr-policy]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/decisions/POLICY.md
[ratification]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/decisions/RATIFICATION.md
[adr-index]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/decisions/README.md
[adr-one]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/docs/decisions/ADR-0001-holistic-architecture-v0.1.md
[roadmap]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/ROADMAP.md
[continuity]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/CONTINUITY.md
[audit-aug19]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/.audits/2026-08-19-organization-audit.md
[audit-aug24]: https://github.com/egohygiene/hygiene/blob/aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d/.audits/2026-08-24-organization-audit.md
[auditor]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/specs/quality/auditor.spec.md
[audit-skill]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/quality/audit-repository/SKILL.md


[decision-record-guide]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/architecture/create-decisions-document/references/decision-record-guide.md
