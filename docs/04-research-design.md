# Research questions, evaluation and publication plan

> Proposal for study design; no results have been collected.

## Research objective

Assess whether a constrained Markdown requirements profile with typed traceability, verifiable acceptance criteria, and an explicit agent interpretation step provides measurable improvements over current requirements representations for human and agent workflows.

## Candidate research questions

- **RQ1 — Representation:** Can a lightweight Markdown profile represent the essential requirement metadata, links, constraints and verification obligations without unacceptable authoring cost?
- **RQ2 — Interpretation:** Does the profile improve an agent's *observable* interpretation accuracy and ambiguity identification compared with unstructured Markdown?
- **RQ3 — Implementation:** Does it improve compliance with independent acceptance oracles, especially on negative cases and invariants?
- **RQ4 — Traceability:** Does typed linking improve precision, recall and change-impact identification across requirement → design → code → test → evidence?
- **RQ5 — Human factors:** Can engineers review, modify and approve the format as effectively as conventional prose and templates?
- **RQ6 — Interoperability:** What information is preserved or lost through JSON, HTML, PDF and (later) ReqIF exports?

## Baselines (subject to feasibility)

1. **B0:** Plain Markdown requirements without enforced structure.
2. **B1:** Markdown with a conventional structured template (e.g. EARS-informed statements).
3. **B2:** Existing spec-driven development workflow such as GitHub Spec Kit, configured fairly.
4. **Treatment:** IntentSpec candidate profile, with/without agent interpretation gate in an ablation study.

The same requirement intent, tools, model versions, budgets and independent tests should be used across conditions where possible. Do not treat a deliberately weak baseline as evidence of superiority.

## Tasks and data

Create or obtain a diverse benchmark of realistic requirements: functional, non-functional, interface, concurrency, security, error handling, and cross-component change scenarios. Include:
- complete, unambiguous requirements;
- intentionally ambiguous or contradictory cases;
- negative examples, boundary conditions and non-obvious invariants;
- change requests requiring downstream impact analysis.

Where practical, use open-source projects and externally reviewed requirements. Record licensing, anonymization and benchmark leakage risks.

## Proposed outcome measures

| Measure | Operationalization |
| --- | --- |
| Interpretation accuracy | Compare agent-produced structured interpretation with independently authored reference answers |
| Clarification quality | Precision/recall of detecting ambiguities; usefulness of clarification questions |
| Implementation compliance | Fraction of hidden independent tests passed; property/invariant checks; regression failures |
| Traceability accuracy | Precision/recall/F1 for typed links and impacted artifact identification |
| Requirements quality | Independent reviewer ratings for clarity, atomicity, verifiability and completeness |
| Human authoring effort | Time, edit count, perceived workload, reviewer error rate |
| Parser correctness | Conformance suite, malformed input rejection, stable JSON output |
| Export fidelity | Preservation of IDs, normative text, links, tables, diagrams and accessibility |
| Cost and repeatability | Agent token usage, wall time, model/temperature, prompts, seed and tool versions |

**Important:** No agent self-report of "I understand" or "I verified it" counts as ground truth. Acceptance must come from an independent oracle or authorized human review.

## Experimental safeguards

- Pre-register or at least version hypotheses and evaluation metrics before running experiments.
- Randomize task/condition order and separate training examples from evaluation cases.
- Include more than one agent/model and multiple runs if resources allow.
- Use blinded human evaluation where feasible.
- Report failures, non-significant results, effect sizes and confidence intervals.
- Disclose threats: task representativeness, leakage, author bias, small sample sizes, benchmark contamination and model changes.
- Use tests written independently of the implementation agent; preserve test and evidence provenance.

## Reference implementation status and goals

**Implemented in the experimental Python prototype:**
- `intentspec validate <paths>` — parse front matter, recognized headings, identified acceptance criteria and Mermaid fences, required fields and typed requirement links;
- `intentspec validate <paths> --json` — machine-readable structural diagnostics;
- `intentspec export-json <paths> --output requirements.json` — JSON representation of structurally valid requirement sets;
- GitHub Actions conformance tests and example validation.

**Not yet implemented:**
- `intentspec lint` — heuristic quality warnings for missing cases, ambiguous terms and suspicious contradictions (not semantic proofs);
- HTML/PDF export, diagram rendering, trace graph/coverage reports and evidence freshness checks;
- ReqIF/OSLC adapters, richer typed constraints, provenance and editor tooling.

Passing structural validation does **not** establish that the requirement is correct, complete or unambiguous.

## Candidate paper structure (REFSQ Research Preview)

1. Motivation and problem framing
2. Related work and explicit differentiation
3. Research questions and design principles
4. Preliminary IntentSpec profile and example
5. Python prototype architecture / proof of concept
6. Proposed evaluation methodology
7. Limitations, threats and future work

**Submission rules, deadlines, review policies and page limits must be rechecked on the official venue website before submission.** Keep public proposal notes separate from an anonymized paper submission if required.

## Falsifiability

The proposal is weakened if (a) an existing tool already provides the same features with equivalent ergonomics, (b) agents show no measurable interpretation/compliance improvement, or (c) human authoring overhead outweighs benefits. Those are useful research outcomes, not failures to report.
