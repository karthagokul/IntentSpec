"""Conformance tests for IntentSpec 0.1. Tests assert structural rules, not semantics."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from intentspec.cli import main
from intentspec.parser import collect_files, parse_text, validate_files


def sample(
    identifier: str = "REQ-DB-001",
    status: str = "draft",
    extra_metadata: str = "",
    extra_sections: str = "",
) -> str:
    return (
        '---\n'
        'intentspec: "0.1"\n'
        f'id: {identifier}\n'
        'title: Sample\n'
        'type: functional\n'
        f'status: {status}\n'
        f'{extra_metadata}'
        '---\n\n'
        f'# {identifier} — Sample\n\n'
        '## Statement\n\n'
        'The system SHALL store the update.\n\n'
        f'{extra_sections}'
    )


CRITERIA = (
    "## Acceptance Criteria\n\n"
    "### AC-01: Successful update\n\n"
    "Given an update, when it commits, then the new value is stored.\n\n"
)

VERIFICATION = "## Verification\n\nIndependent integration test planned.\n\n"

DIAGRAM = (
    "## Diagrams\n\n"
    "### D-01: Commit flow\n\n"
    "```mermaid\n"
    "flowchart TD\n"
    "  A[Update] --> B[Commit]\n"
    "```\n\n"
)


def codes(doc) -> set[str]:
    return {diagnostic.code for diagnostic in doc.diagnostics}


class ParseTests(unittest.TestCase):
    def test_minimal_draft_is_valid(self) -> None:
        self.assertTrue(parse_text(sample()).valid)

    def test_approved_with_criteria_and_verification_is_valid(self) -> None:
        doc = parse_text(sample(status="approved", extra_sections=CRITERIA + VERIFICATION))
        self.assertTrue(doc.valid, doc.diagnostics)
        self.assertEqual(doc.acceptance_criteria[0]["id"], "AC-01")

    def test_missing_front_matter(self) -> None:
        self.assertIn("E_FRONT_MATTER", codes(parse_text("## Statement\n\nHello")))

    def test_duplicate_yaml_keys(self) -> None:
        self.assertIn("E_YAML", codes(parse_text(sample(extra_metadata="id: REQ-DB-002\n"))))

    def test_unsafe_yaml_tag(self) -> None:
        text = sample().replace('title: Sample', 'title: !!python/object/apply:os.system ["echo bad"]')
        self.assertIn("E_YAML", codes(parse_text(text)))

    def test_unquoted_version_is_rejected(self) -> None:
        text = sample().replace('intentspec: "0.1"', "intentspec: 0.1")
        self.assertIn("E_VERSION", codes(parse_text(text)))

    def test_invalid_requirement_id(self) -> None:
        self.assertIn("E_ID", codes(parse_text(sample(identifier="not-a-valid-id"))))

    def test_unknown_metadata_is_error(self) -> None:
        self.assertIn("E_UNKNOWN_FIELD", codes(parse_text(sample(extra_metadata="mystery: value\n"))))

    def test_unknown_section_is_error(self) -> None:
        self.assertIn("E_UNKNOWN_SECTION", codes(parse_text(sample(extra_sections="## Surprise\n\nHello\n"))))

    def test_duplicate_section_is_error(self) -> None:
        self.assertIn("E_DUP_SECTION", codes(parse_text(sample(extra_sections="## Statement\n\nRepeated\n"))))

    def test_heading_in_code_fence_is_not_section(self) -> None:
        text = sample(extra_sections="## Notes\n\n```\n## Surprise\n```\n")
        self.assertTrue(parse_text(text).valid)

    def test_heading_in_blockquote_is_not_section(self) -> None:
        text = sample(extra_sections="## Notes\n\n> ## Surprise\n")
        self.assertTrue(parse_text(text).valid)

    def test_missing_statement(self) -> None:
        text = sample().replace("## Statement", "## Notes")
        self.assertIn("E_STATEMENT", codes(parse_text(text)))

    def test_h1_mismatch(self) -> None:
        text = sample().replace("# REQ-DB-001 — Sample", "# REQ-DB-001 — Wrong")
        self.assertIn("E_H1", codes(parse_text(text)))

    def test_valid_criterion(self) -> None:
        doc = parse_text(sample(extra_sections=CRITERIA))
        self.assertTrue(doc.valid, doc.diagnostics)
        self.assertEqual(doc.acceptance_criteria[0]["id"], "AC-01")

    def test_unnamed_criterion(self) -> None:
        text = sample(extra_sections="## Acceptance Criteria\n\n### A test\n\nHello\n")
        self.assertIn("E_ELEMENT_HEADING", codes(parse_text(text)))

    def test_empty_criterion(self) -> None:
        text = sample(extra_sections="## Acceptance Criteria\n\n### AC-01: Empty\n")
        self.assertIn("E_EMPTY_AC", codes(parse_text(text)))

    def test_duplicate_criterion(self) -> None:
        text = sample(extra_sections=CRITERIA + "### AC-01: Again\n\nAnother case.\n")
        self.assertIn("E_DUP_AC", codes(parse_text(text)))

    def test_diagram_parsed_as_informative(self) -> None:
        doc = parse_text(sample(extra_sections=DIAGRAM))
        self.assertTrue(doc.valid, doc.diagnostics)
        self.assertEqual(doc.diagrams[0]["id"], "D-01")
        self.assertEqual(doc.diagrams[0]["role"], "informative")
        self.assertIn("flowchart", doc.diagrams[0]["source"])

    def test_diagram_requires_mermaid_fence(self) -> None:
        text = sample(extra_sections="## Diagrams\n\n### D-01: No diagram\n\nJust prose.\n")
        self.assertIn("E_DIAGRAM", codes(parse_text(text)))

    def test_mermaid_fence_must_be_inside_diagram(self) -> None:
        text = sample(extra_sections="## Notes\n\n```mermaid\nflowchart TD\nA-->B\n```\n")
        self.assertIn("E_MERMAID_PLACEMENT", codes(parse_text(text)))

    def test_approved_requires_acceptance_and_verification(self) -> None:
        self.assertIn("E_APPROVAL_GATE", codes(parse_text(sample(status="approved"))))

    def test_approved_cannot_have_open_questions(self) -> None:
        text = sample(
            status="approved",
            extra_sections=CRITERIA + VERIFICATION + "## Open Questions\n\nWhat is local?\n",
        )
        self.assertIn("E_OPEN_QUESTIONS", codes(parse_text(text)))

    def test_self_reference(self) -> None:
        text = sample(extra_metadata="trace:\n  depends_on: [REQ-DB-001]\n")
        self.assertIn("E_SELF_REF", codes(parse_text(text)))

    def test_duplicate_reference(self) -> None:
        text = sample(extra_metadata="trace:\n  depends_on: [REQ-DB-002, REQ-DB-002]\n")
        self.assertIn("E_DUP_REF", codes(parse_text(text)))

    def test_json_model_preserves_roles(self) -> None:
        exported = parse_text(sample(extra_sections=CRITERIA + DIAGRAM)).export()
        self.assertEqual(exported["sections"][0]["role"], "normative")
        self.assertEqual(exported["diagrams"][0]["role"], "informative")
        json.dumps(exported)


class CollectionTests(unittest.TestCase):
    def test_resolved_and_unresolved_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "REQ-DB-001.req.md"
            second = Path(tmp) / "REQ-DB-002.req.md"
            first.write_text(
                sample(extra_metadata="trace:\n  depends_on: [REQ-DB-002]\n"),
                encoding="utf-8",
            )
            docs = validate_files([first])
            self.assertIn("E_UNRESOLVED_REF", codes(docs[0]))
            second.write_text(sample(identifier="REQ-DB-002"), encoding="utf-8")
            docs = validate_files(collect_files([Path(tmp)]))
            self.assertTrue(all(doc.valid for doc in docs), docs)

    def test_duplicate_ids_across_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("a.req.md", "b.req.md"):
                (Path(tmp) / name).write_text(sample(), encoding="utf-8")
            docs = validate_files(collect_files([Path(tmp)]))
            self.assertTrue(all("E_DUP_ID" in codes(doc) for doc in docs))

    def test_cli_validate_and_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "a.req.md").write_text(sample(), encoding="utf-8")
            self.assertEqual(main(["validate", str(folder)]), 0)
            output = folder / "export.json"
            self.assertEqual(main(["export-json", str(folder), "-o", str(output)]), 0)
            parsed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(parsed["requirements"][0]["metadata"]["id"], "REQ-DB-001")
            self.assertEqual(parsed["intentspec"], "0.1")

    def test_cli_invalid_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "a.req.md"
            file.write_text(sample(extra_sections="## Unknown\n"), encoding="utf-8")
            self.assertEqual(main(["validate", str(file)]), 1)


if __name__ == "__main__":
    unittest.main()
