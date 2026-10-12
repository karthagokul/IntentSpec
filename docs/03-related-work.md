# Related work and prior-art map

> Initial desk research as of 2026-10-12. This is **not** a systematic literature review. Source URLs are supplied for verification; detailed novelty claims remain open.

| Work | What it contributes | Relationship to proposed ReqMD | Primary source |
| --- | --- | --- | --- |
| ISO/IEC/IEEE 29148:2018 | Requirements engineering processes, information items, characteristics and guidance for requirements | Baseline for what a good requirement should contain; a markup format must not replace the engineering process | [ISO](https://www.iso.org/standard/72089.html) |
| ISO/IEC/IEEE DIS 29148 (draft, 2026) | Revision in development | Check for updated guidance; **not** a published replacement yet | [ISO draft](https://www.iso.org/standard/94091.html) |
| OMG ReqIF 1.2 | Standardized requirements interchange model with XML schemas | Important interoperability baseline; compare coverage and export mapping | [OMG](https://www.omg.org/spec/ReqIF/1.2/) |
| EARS (Mavin et al., RE 2009) | Lightweight structured natural-language requirement templates | Candidate guidance for writing unambiguous statements; do not claim invention of controlled prose | [DOI 10.1109/RE.2009.9](https://doi.org/10.1109/RE.2009.9) |
| Gherkin / Cucumber | Given/When/Then executable-specification syntax with step definitions | Acceptance-criteria representation, not a complete requirements-management model | [Official reference](https://cucumber.io/docs/gherkin/reference/) |
| CommonMark | Precisely specified baseline Markdown parsing | Helps avoid parser dialect drift; tables/front matter require an explicit extension profile | [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) |
| GitHub Spec Kit | Markdown-based artifacts and structured agent workflows for spec-driven development | **Major overlap**. Compare requirement identity, typed semantics, traceability, evidence and independent agent interpretation evaluation | [Official docs](https://github.github.com/spec-kit/) |

## Preliminary synthesis

**Do not claim:** "There is no standard for requirements" or "Nobody uses Markdown with agents." These are contradicted by the existing standards and workflows above.

**Possible research gap to test:** Whether a constrained, standards-informed requirements representation plus a machine-checkable interpretation/evidence protocol improves *traceability correctness*, *ambiguity handling*, and *independently measured implementation compliance* without unacceptable human authoring overhead.

That is a **hypothesis**, not an established novelty claim. GitHub Spec Kit and other emerging spec-driven tools require careful direct comparison before submission.

## Further sources to investigate in deep research

- SysML v2 textual notation and requirements/verification modeling.
- OSLC Requirements Management and linked-data traceability.
- Requirements-as-code projects, Git-native requirement managers, and Markdown + YAML approaches.
- Requirements traceability recovery and change-impact analysis research.
- Requirements quality / ambiguity detection and LLM-assisted RE studies.
- Formal specification approaches (TLA+, Alloy, contracts, temporal logic).
- Agent-oriented spec-driven development (Spec Kit, Kiro, other current tools).
- Agent evaluation methods: controlled tasks, independent test oracles, leakage, replicability.
- Human factors: readability, editing effort, review accuracy and inter-rater agreement.
- Security: prompt injection in repository content and provenance of generated evidence.

## Literature review method (proposed)

Search ACM Digital Library, IEEE Xplore, SpringerLink, Scopus/Web of Science if accessible, arXiv and relevant official specifications. Track title, authors, year, DOI, research type, study context, empirical evidence, limitations, and exact overlap with each proposed contribution. Include negative results and related projects; do not assume novelty from search-result absence.

**Citation policy:** The paper should cite primary sources where possible. This file is an annotated seed list, not a bibliography ready for submission.
