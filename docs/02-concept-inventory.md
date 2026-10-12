# IntentSpec concept inventory (candidate features)

> Brainstorming inventory, **not** a frozen schema. P0 = investigate for minimal profile; P1 = possible extension; P2 = future research.

## Core requirements engineering concepts

| Priority | Concept | Intended role | Questions to resolve |
| --- | --- | --- | --- |
| P0 | Stable requirement ID | Refer to requirements independently of file path/title | ID format; rename/deprecation policy |
| P0 | Atomic requirement statement | Keep one verifiable obligation per item where feasible | Multi-part requirements; exceptions |
| P0 | Requirement type | Functional, performance, interface, security, safety, constraint, etc. | Fixed vs extensible taxonomy |
| P0 | Lifecycle status | Draft, reviewed, approved, implemented, verified, deprecated | Approval authority; status transitions |
| P0 | Source and rationale | Preserve intent, stakeholder and decision context | Privacy and source authenticity |
| P0 | Priority and criticality | Support planning without conflating urgency with safety | Separate priority, severity, risk |
| P0 | Normative vocabulary | Define SHALL, SHALL NOT, SHOULD, MAY | How to handle implicit obligations |
| P0 | Typed relationships | parent, refines, depends_on, conflicts_with, implements, verifies | Directionality, cycles, unresolved links |
| P0 | Preconditions / trigger / outcome | Explain when a rule applies and observable effects | Natural language vs typed semantics |
| P0 | Acceptance criteria | Explicit pass/fail conditions and edge cases | Gherkin vs tables vs properties |
| P0 | Verification specification | Test, inspection, analysis, demonstration, benchmark | What counts as independent evidence |
| P0 | Assumptions and open questions | Prevent agent from silently guessing | When an agent must block |
| P0 | Terminology / glossary | Stabilize meanings across documents | Scope and conflicting definitions |
| P0 | Constraints and invariants | Protect behavior beyond happy-path examples | Units, ranges, concurrency, ordering |
| P0 | Schema and parser validation | Reject malformed metadata and broken links | Versioning, strictness, error codes |
| P0 | Provenance | Human/agent origin, reviewer, approved version | Attestation and audit trail |
| P0 | Canonical intermediate representation | Tool-independent parsed form | JSON Schema, deterministic ordering |
| P0 | PDF / HTML output | Publish reviewable, accessible documents | Diagrams, references, code, page breaks |

## Human + agent concepts

| Priority | Concept | Intended role | Questions to resolve |
| --- | --- | --- | --- |
| P0 | Agent interpretation record | Externalize trigger, expected behavior, constraints, uncertainty | What is machine-checkable? |
| P0 | Clarification gate | Escalate unresolved ambiguity before implementation | Which uncertainties block progress? |
| P0 | Examples and counterexamples | Show allowed and disallowed behavior | Prevent example overfitting |
| P0 | Change restrictions | State interfaces/invariants agents must preserve | Normative status and authorization |
| P0 | Evidence linkage | Tie requirement to test ID, run, artifact and version | Tamper resistance and stale evidence |
| P1 | Change-impact analysis | Find potentially affected requirements, designs, tests, code | Manual vs inferred links |
| P1 | Semantic consistency lint | Flag disagreement between prose, tables, diagrams and metadata | Soundness and false positives |
| P1 | Review workflow | Require human approval for changed normative meaning | PR integration, signed decisions |
| P1 | Risk and hazard links | Trace safety/security risks and mitigations | Integration with domain models |
| P1 | Design / API links | Reference OpenAPI, JSON Schema, ADRs, source symbols | Stable linking across refactors |
| P1 | Traceability matrix / graph | Explore coverage and change impact | Export graph formats |
| P1 | Interoperability | ReqIF import/export and external tool links | Lossless vs lossy mappings |
| P1 | Requirement templates | Reusable EARS-inspired patterns | Avoid over-constraining authors |
| P1 | Property-based or model-based oracles | Verify invariants beyond individual scenarios | Required runtime/tooling |
| P2 | Formal-language bridges | TLA+, Alloy, temporal logic | Which subset is tractable? |
| P2 | Multi-agent review | Independent author, critic and verifier roles | Independence and cost |
| P2 | Semantic diff | Detect meaningful change vs reformatting | Ground truth and false positives |
| P2 | Safety case / assurance argument | Link claims, evidence, assumptions | Domain-specific governance |

## Embedded content: possible first-class blocks

- **Markdown prose** for requirements, rationale and definitions.
- **YAML front matter** for metadata and typed links.
- **Tables** for conditions, decisions, units and boundary values.
- **Mermaid** for sequence/state/flow diagrams; render as supporting views.
- **Gherkin** for behavior examples; step definitions required for execution.
- **YAML/JSON** for typed interface contracts and constraints.
- **Code examples** for usage; distinguish examples from required implementations.
- **Math/LaTeX** for equations, with a specified units model.
- **External links** for OpenAPI, JSON Schema, standards, ADRs, tests and evidence.
- **Images/attachments** only with provenance and accessibility fallback.

## Open semantics decisions

1. Is each `.req.md` file one atomic requirement, or can it contain a hierarchy?
2. Which sections are normative, informative, or evidence? Define precedence explicitly.
3. Are typed constraints canonical while prose is explanatory, or must both agree equally?
4. Are diagrams normative? If yes, what restricted subset and validation rules apply?
5. How are status changes authorized and how is version identity preserved?
6. What does an unresolved cross-reference mean: warning or hard error?
7. What does an agent do when a requirement is contradictory, unverifiable or underspecified?
8. How can independent verification avoid circular agent-generated tests?
9. What is the smallest schema that provides measurable improvement over plain Markdown?
10. How do we avoid creating a new tool silo when ReqIF and spec-driven workflows exist?

## Proposed minimum viable slice

A **single requirement per file** (initial hypothesis), required front matter (`id`, `title`, `type`, `status`), a normative `Requirement` section, optional `Rationale`/`Assumptions`/`Acceptance Criteria`/`Verification`/`Traceability` sections, typed links, schema validation, JSON export and HTML/PDF rendering.

An agent interpretation protocol should be evaluated experimentally; it need not be embedded into the language syntax until results justify it.
