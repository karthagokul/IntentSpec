# ReqMD — Requirements Proposal

Research workspace and **experimental Python prototype** for a human-readable, AI-agent-consumable software requirements language.

**Current state:** draft **ReqMD v0.1 profile**, working parser/validator and JSON exporter, two example requirements with Mermaid diagrams, and automated conformance tests. **Not** a published standard, verified requirements corpus, semantic prover, or evaluated research result.

## Read the draft language

- [ReqMD v0.1 language specification](docs/07-reqmd-v0.1-spec.md) — syntax, reserved Markdown headings, authority model, diagram/acceptance IDs, and structural validation.
- [Atomic update example](examples/REQ-DB-018.req.md) — structured, in-review functional requirement with Mermaid, acceptance criteria and verification plan.
- [Notification example](examples/REQ-DB-017.req.md) — draft performance requirement that intentionally retains unresolved questions.
- [Concept inventory](docs/02-concept-inventory.md) — ideas to assess before expanding the language.

## Run the Python prototype

Requires Python 3.10 or newer:

```bash
python -m pip install -e .
reqmd validate examples
reqmd validate examples --json
reqmd export-json examples --output requirements.json
python -m unittest discover -s tests -v
```

A failed validation exits with status **1** and reports file, line, error code and message. JSON export is allowed only for a structurally valid set of requirements. When typed links are present, validate the **complete referenced set** rather than a single isolated file.

The parser recognizes exact top-level `##` headings; it does **not** infer headings from synonyms. It checks YAML metadata, IDs, reserved sections, identified acceptance criteria, Mermaid fence placement, approval gates, duplicate IDs and typed requirement links. Diagrams are informative by default. It does **not** validate Mermaid syntax, execute Gherkin, judge prose ambiguity, detect arbitrary semantic contradictions, or verify evidence.

GitHub Actions runs the test suite and validates/exports the examples on pushes and pull requests.

## Research context

- [Problem statement](docs/01-problem-statement.md)
- [Related work](docs/03-related-work.md) — seed list, not a systematic review
- [Research questions and evaluation](docs/04-research-design.md)
- [Agent interpretation and evidence](docs/05-agent-interpretation-and-evidence.md)
- [Decisions and roadmap](docs/06-decisions-and-roadmap.md)

**Research hypothesis:** a constrained Markdown requirements profile plus a structured interpretation/clarification protocol may improve observable agent interpretation, typed traceability and independent verification without excessive human authoring overhead.

We cannot inspect an agent's internal understanding. We can measure its *external interpretation* and independently test the resulting implementation. Those improvements have **not yet been demonstrated**.

## Why a new profile?

Existing standards and tools—including ISO/IEC/IEEE 29148, OMG ReqIF, EARS, Doorstop, StrictDoc, Sphinx-Needs and GitHub Spec Kit—already cover substantial parts of requirements authoring, traceability, and spec-driven development. A new Markdown profile is not novel merely because it uses YAML, diagrams, or acceptance criteria. This project must test a **specific, falsifiable** contribution against strong existing baselines.

## Design principles

1. Human-readable source with a deterministic machine-parsed structure.
2. Normative statements and acceptance criteria separated from informative diagrams and guidance.
3. Stable requirement IDs and typed links.
4. Unresolved ambiguity surfaced rather than silently guessed away.
5. No claim of verification without independent evidence.
6. Small, versioned language profile with explicit validation limits.

## Contributions

Open an issue or pull request to challenge semantics, propose concepts, add related work, or contribute examples. A particularly useful contribution is a requirement that **looks valid but is ambiguous, contradictory or misleading to an AI agent**: it helps us design stronger review and evaluation methods.

**ReqMD** and `.req.md` remain working names; the v0.1 profile is subject to review.
