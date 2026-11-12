# Prospective commit, PR-title and change-history policy

Status: **proposed `1.0.0-alpha.1`, observe only; approval null**.
Refs [Hygiene #37](https://github.com/egohygiene/hygiene/issues/37) and
[ADR-0018](../decisions/ADR-0018-prospective-change-history-policy.md).

The canonical machine proposal is
[`catalog/change-history-policy.json`](../../catalog/change-history-policy.json).
It defines prospective message semantics. It does not change a hook, branch
ruleset, merge method, required check, PR title, existing commit, tag, signature,
release declaration or consumer pin. Historical normalization remains
[Hygiene #38](https://github.com/egohygiene/hygiene/issues/38).

## One exact subject shape

```text
<type>(<scope>)[!]: <emoji> <description>
feat(api): ✨ add bounded selectors
fix(parser): 🐛 preserve empty values
feat(api)!: ✨ replace the selector format
```

The bracketed bang is optional syntax, not literal brackets. Scope is required:
one lowercase ASCII component key, at most64 characters, beginning with a digit
or letter and then letters/digits/dot/underscore/slash/hyphen. Empty, `.` or `..`
slash segments and trailing punctuation are invalid. Repositories own their
stable scope vocabulary; `repo`, `deps` and `release` are useful ordinary scopes,
not a universal list that replaces local components.

Use one ASCII space after the colon and after the exact mapped Unicode emoji.
Subjects are NFC and at most100 Unicode code points including prefix/emoji.
The description begins with a lowercase ASCII letter, has no terminal period,
leading/trailing or doubled spaces, and is meaningful rather than an exact
placeholder such as `wip`, `tmp`, `test` or `update`. The portable ASCII initial
and exact variation-selector spellings are explicit compatibility choices for
review; they are stricter than some existing authoring tools. No message is
rewritten to make it pass. Shortcodes and unrelated emoji do not satisfy this
proposed profile.

| Type | Exact emoji | Non-breaking release hint |
| --- | --- | --- |
| `build` | 📦 | none |
| `chore` | 🔧 | none |
| `ci` | 👷 | none |
| `docs` | 📝 | none |
| `feat` | ✨ | minor |
| `fix` | 🐛 | patch |
| `perf` | ⚡️ | patch |
| `refactor` | ♻️ | none |
| `revert` | ⏪ | explicit review required |
| `security` | 🔒 | patch |
| `style` | 🎨 | none |
| `test` | ✅ | none |

Every explicit breaking change gives a **major hint**, regardless of ordinary
type, except that a revert always requires net-effect review. The `!` belongs
after the closing scope parenthesis. A final `BREAKING CHANGE:` or
`BREAKING-CHANGE:` trailer also declares a break. A title bang is syntactically
valid without a body; a rationale and migration explanation are recommended in
the PR/commit body. A pre-1.0 repository still follows its declared version
authority; a hint cannot silently select `1.0.0` or publish anything.

## Bodies, trailers and revert semantics

Commit bodies follow a blank line after the subject. The final trailer block
follows another blank separator when preceded by prose. Its first line is
`Token: value`; continuation lines are indented by a space or tab. The exact
allowlisted tokens live in the machine profile. Unknown trailer tokens require
a registered versioned extension; they are not silently interpreted as release
or approval metadata. A recognized breaking line outside the bounded final
trailer block is rejected rather than quietly becoming a no-breaking hint.

`Reverts: <full lowercase 40-character Git SHA>` is required for canonical
`revert` messages. A message naming a prior commit does not prove that a release
was undone, a deployment rolled back, a finding resolved, or the original
change fully canceled. The release owner reviews the actual net effect and
retained source evidence. Existing Git-generated `Revert "..."` messages stay
historical evidence; they are not rewritten by this proposal.

`Signed-off-by`, `Co-authored-by` and `Reviewed-by` remain source assertions.
Message text does not verify DCO/CLA compliance, identity, signing keys, human
approval or provenance. `Release-As` remains a hint to the separately selected
Aether/repository release authority, never an override. Existing ADR and roadmap
trailers retain real stable identifiers; this parser does not invent them or
prove that a referenced issue/decision exists.

## PRs, automation and merge strategy

PR titles use the same single-line subject grammar; even a trailing newline is
invalid. Squash is the proposed default for future selected consumers so the
reviewed PR title can become one canonical default-branch subject. Preserve the
needed body, authorship, DCO and coauthor trailers. Rebase may be explicitly
selected when every retained commit satisfies the selected contract and the
repository's actual provenance requirements remain intact. This proposal does
not change any provider setting or silently disable merge commits.

Existing provider merge messages are **context only**, with at least two
declared parents. A merge title does not supply the semantics of its constituent
changes. Bot, dependency and generated commits use the same core grammar;
automation identity or generated output never exempts them. Release-preparation
commits use `chore(release): 🔧 ...`, with no breaking marker or inferred release
bump, preventing a release-metadata loop. A patching dependency change can use
`fix(deps)` when that is its actual meaning; dependency tooling must not invent a
breaking effect from a version-number change alone.

Emergency deviations need an explicit scoped reason, owner, durable human
disposition, expiry and exit criteria. An unverified exception JSON record
cannot waive syntax, approve a release or activate enforcement. There are no
approved exceptions in this proposal.

## Extensions, owners and version authority

Repository scope additions preserve the common grammar. Extra types require a
namespaced/versioned extension with an explicit core semantic mapping; they may
not redefine core emoji, breaking rules, release hints, provenance or authority.
The reference core rejects unregistered extensions. Stricter compatible local
limits, such as a72-character subject ceiling, may remain selected and visible.

Hygiene owns this policy and compatibility proposal. EgoLint owns production
lint/report semantics, Aether the existing release declaration/authoring
protocol, Relay safe reusable preview/apply/verification, Holon materialization
and Pace reviewed adoption. Repositories retain local facts, scope selection,
component version authority, actual release decisions, credentials and final
publication. The pinned
[release baseline](REPOSITORY_RELEASE.md) composes Aether
`8a2a3d08f3aa9da3847bd5277843506ab855192e`; commits are advisory evidence, not a
replacement version source. Neither a valid title nor a clean parser authorizes
tags, package publication, deployment, DCO acceptance or historical rewriting.

## Reference boundary and synthetic examples

`tools/change_history.py` exposes pure `analyze(record)` for the closed
`egohygiene.change-history-input/v1` envelope. Its file CLI reads only a bounded
regular non-symlink JSON file; it does not scan Git or execute a consumer. It
authenticates the exact shipped policy checksum and returns the closed
`egohygiene.change-history-analysis/v1` result: syntax, canonical type,
scope-presence state, breaking flag, release hint and static diagnostic codes.
It never echoes subject/body/scope prose, actor/trailer values or an input hash.
Nonpublic/unknown source claims are omitted before inspecting their payload.
The public flag is not independently authenticated provider visibility; results
remain local review data, not public fleet evidence.

The file reference requires a POSIX runtime with no-follow/nonblocking file
flags and fails closed with a neutral diagnostic when they are unavailable.
The machine scope grammar combines its lexical pattern with the explicit
forbidden slash-segment and terminal-character lists; all constraints apply.

The envelope is at most262144 UTF-8 bytes, and the message at most65536 UTF-8
bytes. JSON Schema's `maxLength: 65536` is an additional Unicode-code-point
structural ceiling; the byte ceiling is a separately named semantic check.
Malformed/unsupported input fails explicitly. The reference's bounded final
trailer language is not a general Markdown parser or a complete commitlint
replacement. Production adapters must retain these semantics and their actual
tool/parser coverage in reports.

The [synthetic cases](../../fixtures/change-history/examples.json) cover normal,
breaking, revert, bot/dependency, generated, release, merge, placeholder and
invalid syntax. They were authored as review material and **not executed**.
The [source migration map](../../fixtures/change-history/migration-map.json)
records exact public configurations and deferred restricted-source mapping.

## Compatibility, migration and activation

Start with immutable source/config inventory and an exact no-write preview;
distinguish canonical-type identity from emoji/scope/spacing compatibility.
Keep source messages and private issue/actor information outside public plans.
EgoLint's present scoped parser, Empathy's richer prompt types, Renderflow's
conventional configuration and Reflector's research/spec/sync/audit additions
are observed implementations, not evidence that this new policy is accepted.
Do not automatically map an unfamiliar purpose type to a release effect.

After explicit disposition of this proposal, select compatible owner adapters
in one advisory canary, preserve old pins/check contexts and capture actual
resulting squash/rebase subjects. Review drift, rollback and release-hint
compatibility before any ratchet/enforce stage or wider Pace adoption. Undo a
prospective tool upgrade by reselecting its previous immutable inputs; never
rewrite existing commits/tags/signatures or erase authored records.

Static source/AST/schema-meta and independent peer review are the only authoring
checks in this slice. No parser/helper, example, regression, native validation,
tests, builds, CI, Git/provider mutation, publication or fleet adoption ran.
The accepted ADR policy1.2.0 remains unchanged. New ADR-0018 and this policy keep
proposed lifecycle and null approval; merging source supplies no ratification.
