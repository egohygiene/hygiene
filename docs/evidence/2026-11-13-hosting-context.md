# Organization hosting context integration — 2026-11-13

The organization hosting catalog added three `.github` inputs without their
existing context-policy source mappings. The strict context generator correctly
rejected the incomplete policy; the correction supplies the canonical owners:

| Declared input | Owner |
| --- | --- |
| `Hygiene organization surface declaration` | `egohygiene/hygiene` |
| `Relay sealed-export intake` | `egohygiene/relay` |
| `website-owned organization Intelligence static export` | `egohygiene/egohygiene.io` |

Functional source `dbaf7eeb408b2104daf8acb16c0d43adb55d7605` contains the real
catalog, policy and unchanged generator inputs. The current Hygiene projection,
current generated Sanctuary example and current context contract deliberately
select that immutable revision. Their regenerated canonical links do not falsely
attribute the new mappings to the previous `1c7209` selection. Older immutable
pins and the deprecated v1 contract remain unchanged in Git.

The canonical ownership/catalog facts, public membership, model clocks, release
and hosting owner pins, provider settings, human dispositions and all validator
semantics are unchanged by this follow-up. No dependency is reclassified as an
external input merely to bypass the missing mapping. The traversal regression
uses the actual append index while retaining its precise unsafe-identity check.

On clean integrated source `0dc16cac245b6fc47db5d925f31fef7cd3762d26`, after
the selected Hygiene six-source batch through main `0011b7e`:

- All 27 focused context tests passed, including the new exact `.github`
  upstream-owner assertion and a missing-mapping fail-closed negative case.
- Exact owner checks for both current projections and the context contract
  passed. A disposable complete render also covered all 29 canonical catalog
  entries; this is not public discovery or a new organization-total assertion.
- Independent Journey source review proved the declared `dbaf7ee` inputs and
  unchanged v1/helper resources before the final main/continuity reconciliation.

An earlier complete local reference gate at `1c1643d` was **not passing**:
its isolated whole-unit command hit the unchanged 60-second limit, and its
release-declaration check lacked the prepared exact Aether owner checkout.
It used the environment's global schema dependency rather than the selected
locked release-owner environment. Context and generated checks passed, but that
does not upgrade the complete gate. The final merged whole-gate run is owned
separately with the prepared immutable owner/cache and locked dependencies;
no timeout, validator or failure state is waived here.

ADR not required: this repairs a missing source-map composition under existing
ADR-0008/ADR-0020 without changing ownership or policy lifecycle. No issue is
closed, no native release/ADR admission is promoted, and no Pages publication
or human ratification is supplied by a context projection.
