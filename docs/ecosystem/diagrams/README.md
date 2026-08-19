# Diagram Sources

These three files express the same reviewed topology:

- `ecosystem.mmd` — Mermaid source for Markdown and documentation sites.
- `ecosystem.puml` — PlantUML source for deterministic CI rendering.
- `ecosystem.excalidraw` — editable visual canvas for collaborative design.

The diagrams show capability ownership and artifact/contract direction. An arrow does **not** imply a source-code dependency. The prose architecture and machine-readable repository catalog remain authoritative if a visual becomes stale.

The written boundaries are accepted by
[`ADR-0001`](../../decisions/ADR-0001-holistic-architecture-v0.1.md). Future
infographics must use these diagram sources, not old PNGs, as semantic input and
must archive the approved render with its architecture release.

## Canonical path

```text
hygiene/
├── catalog/repositories.yaml
└── docs/ecosystem/
    ├── ARCHITECTURE.md
    ├── REPOSITORY_CATALOG.md
    └── diagrams/
        ├── ecosystem.mmd
        ├── ecosystem.puml
        ├── ecosystem.excalidraw
        └── rendered/
```

## Regeneration

Run `node generate-excalidraw.mjs` from this directory to regenerate the
editable Excalidraw file from the node list and relationships embedded in the
script. A clean regeneration must leave `ecosystem.excalidraw` unchanged.
