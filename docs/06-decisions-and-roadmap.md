# Open decisions and staged roadmap

> Decisions are **proposed**, not approved. Keep decisions and experiments versioned.

## Decision backlog

| ID | Question | Candidate direction | Status |
| --- | --- | --- | --- |
| D01 | Name and extension | **IntentSpec** (provisional project/language name); `.req.md` retained as format extension | Provisional |
| D02 | Markdown dialect | CommonMark core with explicitly specified tables/fences/front matter | Open |
| D03 | Requirement granularity | One requirement per file initially | Open |
| D04 | Normative vs informative | Prose + typed constraints normative; Mermaid and examples informative by default | Open |
| D05 | Metadata | Small YAML front matter, validated with JSON Schema | Open |
| D06 | Relationships | Typed, directed links with stable IDs | Open |
| D07 | Quantities | Typed value + unit, conditions and measurement method | Open |
| D08 | Acceptance criteria | Plain cases + optional Gherkin, independent test mapping | Open |
| D09 | Agent protocol | Structured interpretation and mandatory clarification on unresolved conflicts | Open |
| D10 | Canonical export | JSON intermediate representation | Open |
| D11 | Publishing | Python HTML/PDF rendering; Mermaid diagrams and cross-references | Open |
| D12 | Interoperability | Investigate ReqIF/OSLC compatibility rather than replace them | Open |
| D13 | Research contribution | Measure interpretation, traceability and compliance vs strong baselines | Open |
| D14 | Public repository and review anonymity | Confirm venue policy before posting paper/preprint | Open |

## Suggested sequence

**Phase A — research framing**
- Expand literature map and direct prior-art comparisons.
- Select a narrow, falsifiable contribution and realistic evaluation tasks.
- Decide minimal normative semantics and authority rules.

**Phase B — profile v0.1 (initial draft implemented; further conformance work open)**
- Specify grammar/metadata schema, required sections, typed relationships and error classes.
- Write 10–20 examples, including malformed, contradictory and ambiguous cases.
- Establish a conformance test suite.

**Phase C — Python prototype (parser, validator and JSON export implemented; other tools pending)**
- Implement parse/validate/lint, canonical JSON export and link graph.
- Add HTML/PDF rendering, Mermaid diagrams, stable cross-references.
- Keep automated "quality" checks as warnings unless objectively decidable.

**Phase D — experiments**
- Compare against plain Markdown, structured templates and relevant agentic workflows.
- Test interpretation accuracy, traceability, compliance, human effort and export fidelity.
- Publish data/protocol/results with limitations.

**Phase E — paper**
- Write an evidence-grounded research preview or full paper, following the venue's current rules.
- Separate the proposed language from claims established by evaluation.

## Immediate next discussion

1. What is the **smallest requirement unit**?
2. Which parts of a `.req.md` file are **authoritative**?
3. What is the **minimum required metadata**?
4. What is a **verifiable acceptance criterion**?
5. What does a coding agent **have to prove or ask before implementation**?

See [example requirement](../examples/REQ-DB-017.req.md) as a design discussion aid, not an approved schema.
