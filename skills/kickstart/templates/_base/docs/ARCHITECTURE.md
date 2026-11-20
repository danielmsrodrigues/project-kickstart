<!--
Template for docs/ARCHITECTURE.md. Fill from the design (spec or mini-design answers)
and from what exists in the repo. Write what is decided; mark open points as "Open:".
Delete this comment block.
-->
# Architecture

## Purpose

{{WHAT THE SYSTEM DOES AND FOR WHOM, 2-4 sentences}}

## Context

{{WHO/WHAT TALKS TO THIS SYSTEM: users, other services, external APIs, data stores. A short list or a small text diagram.}}

```
{{OPTIONAL TEXT DIAGRAM, e.g.
[client] --HTTP--> [api] --SQL--> [database]
                     \--> [payment provider]
}}
```

## Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| {{NAME}} | `{{PATH}}` | {{ONE LINE}} |

## Boundaries and rules

{{BULLETS: dependency direction (what may import what), where business logic lives, where I/O lives, what must stay framework-free.}}

## Data

{{MAIN ENTITIES OR DATA FLOWS, storage, migrations approach. "None yet" is a valid answer.}}

## Cross-cutting concerns

- Configuration: {{HOW CONFIG AND SECRETS ARE LOADED}}
- Errors and logging: {{APPROACH}}
- Testing: {{TEST LEVELS AND WHERE THEY LIVE}}

## Open questions

{{BULLETS, or delete the section}}

## Related

- Decisions: [decisions/](decisions/)
- Conventions: [CONVENTIONS.md](CONVENTIONS.md)
{{SPEC_LINK: if a design spec exists, link it here, e.g. - Design spec: [superpowers/specs/<file>](superpowers/specs/<file>)}}
