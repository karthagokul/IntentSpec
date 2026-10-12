# Problem statement — requirements for humans and software agents

> Working notes, 2026-10-12. **Hypotheses, not validated findings.** Working name: **IntentSpec**.

## Motivation

Software requirements are consumed by stakeholders, engineers, tooling, and increasingly autonomous coding agents. Plain natural-language documents are accessible to people but often omit machine-checkable meaning, stable identity, verification evidence, and links to downstream artifacts. Formal specifications can offer precision but require greater authoring effort and specialist skills. Existing tools and formats address parts of this problem; a new format must demonstrate a concrete benefit over them.

**Proposed research problem:** Can a constrained, Git-native Markdown requirements profile support human authoring and review while improving agents' *observable interpretation accuracy*, requirements traceability, and independent verification?

We do **not** claim to observe an agent's internal understanding. We can evaluate its explicit interpretation and resulting behavior against an independently established oracle.

## Candidate problems to investigate

| ID | Problem | Observable failure | Potential response |
| --- | --- | --- | --- |
| P01 | Ambiguity and underspecification | Agents make different assumptions from the same prose | Glossary, scoped terms, assumptions, ambiguity reporting |
| P02 | Missing requirement identity | References break when headings or files move | Stable IDs, cross-file reference resolution |
| P03 | Broken end-to-end traceability | No evidence linking need → requirement → design → code → test → result | Typed relationship graph and coverage reports |
| P04 | Conflicting representations | Prose, YAML, Mermaid, and Gherkin disagree | Explicit normative precedence; consistency checks |
| P05 | Weak acceptance criteria | A plausible implementation passes superficial examples but violates invariants | Measurable oracles, negative cases, boundary cases |
| P06 | Agent interpretation drift | Agent paraphrases a constraint incorrectly | Structured interpretation proposal, validation, clarification gate |
| P07 | Unverified self-attestation | Agent declares compliance without independent evidence | CI-produced evidence with provenance and immutable references |
| P08 | Change-impact blindness | Requirement changes but tests and designs remain stale | Dependency graph, version-aware impact analysis |
| P09 | High authoring burden | Authors avoid a complex DSL | Markdown-first authoring with optional typed structures |
| P10 | Limited interoperability | Requirements cannot move between repositories, tools, and reports | JSON intermediate model; later ReqIF adapters |
| P11 | Untrusted embedded content | Agent follows instructions inside examples or external artifacts | Trust boundaries, safe rendering, explicit authority model |
| P12 | Difficult document publishing | Requirements are only usable in their authoring tool | Reproducible HTML/PDF with Mermaid rendering and stable links |

## Proposed artifact

A versioned `*.req.md` profile combining:

1. **YAML front matter:** identity, classification, lifecycle, provenance, typed links.
2. **Markdown sections:** normative requirement, rationale, context, glossary, assumptions.
3. **Structured constraints:** typed quantities, units, conditions, interfaces, invariants.
4. **Examples and tests:** Gherkin scenarios, negative examples, boundary conditions.
5. **Diagrams:** Mermaid as informative by default, unless a subset is explicitly given normative semantics.
6. **Verification:** independent oracle, method, evidence reference, result provenance.
7. **Agent interaction:** an interpretation/clarification protocol and constraints on permissible changes.
8. **Exports:** canonical JSON model, HTML, PDF; later ReqIF interoperability.

The Python parser should distinguish **syntactic validity**, **semantic consistency**, **quality warnings**, and **actual verification results**. It must not report that a requirement is verified just because metadata says so.

## Boundaries and cautions

- This is **not** a claim that Markdown requirements do not already exist.
- YAML structure alone does not make natural-language meaning deterministic.
- Gherkin becomes executable only when linked to working step definitions or another verified oracle.
- Mermaid is useful for communication, but a rendered diagram is not automatically a formal specification.
- Generated tests are not independent proof if the agent invents both implementation and expected result.
- A parser can validate schema and links, but cannot guarantee completeness, truth, or absence of contradictions.
- Keep the paper's proposed contributions separate from experimental findings.

## Desired outcomes

A small, documented language profile; a reference Python parser/validator/exporter; a reproducible benchmark; and evidence showing where the profile does and does not improve outcomes compared with relevant baselines.

See [concept inventory](02-concept-inventory.md), [related work](03-related-work.md), and [research design](04-research-design.md).
