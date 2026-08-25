# ADR-002 ratification record

This document maps Hygiene issue
[#15](https://github.com/egohygiene/hygiene/issues/15) to reviewable contract
evidence and keeps contract completion separate from human policy authority.

## Acceptance evidence

| Issue requirement | Canonical evidence |
| --- | --- |
| Versioned global specification | [`POLICY.md`](POLICY.md) and `egohygiene.architecture-decision/v1` |
| Explicit required and optional fields | Policy section 5 and [`architecture-decision.v1.schema.json`](../../schemas/architecture-decision.v1.schema.json) |
| Lifecycle and supersession semantics | Policy sections 9-10 plus accepted, rejected, and invalid approval fixtures |
| Organization and repository ownership | Policy section 2 and ADR-002 |
| Inheritance by reference and version | Policy section 6 and `egohygiene.architecture-decision-policy-reference/v1` |
| Permitted extensions and invalid overrides | Policy section 7, both schemas, and hostile fixtures |
| Stable IDs and index requirements | Policy section 4 |
| Relay/Egolint validation requirements | [`VALIDATION.md`](VALIDATION.md) and [`tools/decisions.py`](../../tools/decisions.py) |
| Existing-repository migration | [`MIGRATION.md`](MIGRATION.md) |

The matrix establishes that the proposal is complete enough to decide. It does
not make ADR-002 accepted.

## Human activation gate

A maintainer ratifying ADR-002 must review one exact commit and leave durable
GitHub evidence that names both the decision and policy version. Recommended
approval text:

```text
I approve egohygiene/hygiene ADR-002 and the Organization Architecture
Decision Record Policy v1.1.0 at commit <full-commit-sha> for organization use.
```

After that statement exists, a ratification commit may:

1. set ADR-002 `status: accepted`;
2. populate `approval.date`, `approval.by`, and the exact evidence URL;
3. add the ratification review or comment to `evidence`;
4. set the policy document status to `accepted`;
5. activate the ADR and inheritance contracts in `catalog/contracts.yaml`;
6. update the decision index and roadmap gate; and
7. rerun all contract and generated-file checks.

An agent may prepare or validate that commit after approval is visible. It must
not create the approval statement, infer approval from assignment, or treat a
merge as ratification. Issue #15 remains open until the ratification commit is
merged with resolvable approval evidence.
