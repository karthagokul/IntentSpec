# Requirements Proposal — ReqMD (working name)

Research workspace for a **human- and AI-agent-readable software requirements representation**, tentatively called **ReqMD**.

**Status:** exploratory proposal; no language standard, Python parser, experiments, or published research results yet.

## Research premise

Can a constrained Markdown requirements profile, coupled with typed traceability and independently verified agent interpretation, improve software engineering outcomes without sacrificing human readability?

This repository separates **ideas**, **related work**, **research questions**, and **demonstration examples**. Nothing here should be interpreted as proof of novelty or effectiveness.

## Start here

- [Problem statement](docs/01-problem-statement.md) — candidate failures and boundaries.
- [Concept inventory](docs/02-concept-inventory.md) — proposed requirements, agent and tooling concepts.
- [Related work](docs/03-related-work.md) — initial primary-source map (not a systematic review).
- [Research design](docs/04-research-design.md) — falsifiable questions, baselines, metrics and evaluation safeguards.
- [Agent interpretation and evidence](docs/05-agent-interpretation-and-evidence.md) — externalized interpretation, clarification and independent verification.
- [Decisions and roadmap](docs/06-decisions-and-roadmap.md) — unresolved design choices and suggested phases.
- [Illustrative requirement](examples/REQ-DB-017.req.md) — Mermaid, Gherkin, metadata, traceability and explicit ambiguities.

## Candidate toolchain (future work)

```text
*.req.md
   │
   ├─ Python parser / validator / linter
   ├─ canonical JSON requirements model
   ├─ typed traceability graph
   ├─ agent interpretation + clarification workflow
   ├─ independent verification evidence
   └─ HTML / PDF exports (Mermaid diagrams included)
```

## Guiding principles

1. **Humans and agents share the same source**; no invisible parallel specification.
2. **Explicit authority:** distinguish normative obligations from explanatory examples and diagrams.
3. **Traceability with evidence:** links and verification results must be independently checkable.
4. **Ambiguity is surfaced, not guessed away.**
5. **Small, Git-native, interoperable:** use existing standards and tools where they fit.
6. **Empirical claims require experiments** against credible existing approaches.

## Prior art matters

Requirements standards and approaches already exist, including ISO/IEC/IEEE 29148, OMG ReqIF, EARS, Gherkin, and GitHub Spec Kit. In particular, **Markdown-based agent specifications are not new**. The research must demonstrate a narrower, measurable contribution.

## Contribution and review

Open a GitHub issue or pull request to propose concepts, challenge assumptions, contribute prior art, or suggest benchmark cases. Prefer source-backed claims with a DOI or official specification link. Keep hypotheses clearly labeled.

The name **ReqMD** and the file extension **.req.md** are placeholders until the profile is defined and compared with existing approaches.
