# Diagram Sources

These three files express the current topology view:

- `ecosystem.mmd` — Mermaid source for Markdown and documentation sites.
- `ecosystem.puml` — PlantUML source for deterministic CI rendering.
- `ecosystem.excalidraw` — editable visual canvas for collaborative design.

The diagrams show capability ownership and artifact/contract direction. An arrow does **not** imply a source-code dependency. The prose architecture and machine-readable repository catalog remain authoritative if a visual becomes stale.

The [authority map](../ARCHITECTURE.md#authority-and-evidence) distinguishes
the historical five-plane ADR-0001 baseline from the current view. The Filament
plane follows proposed ADR-0003. Sanctuary's incubation role and Empathy's
strict baseline follow proposed ADR-0004 at organization scope and have
separate local implementation evidence. Firmament remains deferred.
Use these sources for future infographics and archive approved renders with
their architecture release.

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
