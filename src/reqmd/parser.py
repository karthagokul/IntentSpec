"""Draft ReqMD 0.1 parser and deterministic structural validator.

This module does not establish semantic correctness of natural-language statements,
execute Mermaid/Gherkin, or certify verification evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any, Iterable

from markdown_it import MarkdownIt
import yaml
from yaml.constructor import ConstructorError

VERSION = "0.1"
ID_PATTERN = re.compile(r"^REQ-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3,}$")
AC_PATTERN = re.compile(r"^(AC-\d{2,}): (.+)$")
DIAGRAM_PATTERN = re.compile(r"^(D-\d{2,}): (.+)$")

REQUIRED_FIELDS = {"reqmd", "id", "title", "type", "status"}
OPTIONAL_FIELDS = {"priority", "component", "source", "trace"}
TYPES = {"functional", "performance", "interface", "security", "safety", "constraint", "quality"}
STATUSES = {"draft", "in_review", "approved", "deprecated"}
PRIORITIES = {"must", "should", "could", "wont"}
TRACE_RELATIONS = {"depends_on", "refines", "related_to"}

# Order is a display recommendation, not a syntactic requirement.
SECTION_ROLES = {
    "Statement": "normative",
    "Definitions": "normative",
    "Preconditions": "normative",
    "Invariants": "normative",
    "Acceptance Criteria": "normative",
    "Diagrams": "informative",
    "Rationale": "informative",
    "Open Questions": "informative",
    "Verification": "administrative",
    "Traceability": "informative",
    "Agent Guidance": "informative",
    "Notes": "informative",
}

MARKDOWN = MarkdownIt("commonmark", {"html": False}).enable("table")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise ConstructorError(None, None, "YAML mapping keys must be strings", key_node.start_mark)
        if key in result:
            raise ConstructorError(None, None, f"duplicate YAML key: {key}", key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


@dataclass(frozen=True)
class Diagnostic:
    path: str
    line: int
    severity: str
    code: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }


@dataclass
class Requirement:
    path: str
    metadata: dict[str, Any] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)
    acceptance_criteria: list[dict[str, str]] = field(default_factory=list)
    diagrams: list[dict[str, str]] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not any(d.severity == "error" for d in self.diagnostics)

    def export(self) -> dict[str, Any]:
        """Structured, JSON-compatible representation (not a semantic proof)."""
        return {
            "metadata": self.metadata,
            "sections": [
                {"name": name, "role": SECTION_ROLES[name], "markdown": markdown}
                for name, markdown in self.sections.items()
            ],
            "acceptance_criteria": self.acceptance_criteria,
            "diagrams": self.diagrams,
        }


def _add(req: Requirement, code: str, message: str, line: int = 1) -> None:
    req.diagnostics.append(Diagnostic(req.path, line, "error", code, message))


def _front_matter(req: Requirement, text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        _add(req, "E_FRONT_MATTER", "file must begin with a YAML '---' delimiter")
        return text, 1

    closing = next(
        (i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"),
        None,
    )
    if closing is None:
        _add(req, "E_FRONT_MATTER", "missing closing YAML '---' delimiter")
        return "", len(lines) + 1

    raw_yaml = "".join(lines[1:closing])
    try:
        loaded = yaml.load(raw_yaml, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        _add(req, "E_YAML", str(exc), (mark.line + 2) if mark else 2)
        loaded = None
    if not isinstance(loaded, dict):
        _add(req, "E_METADATA", "front matter must contain a YAML mapping", 2)
    else:
        req.metadata = loaded

    return "".join(lines[closing + 1 :]), closing + 2


def _validate_metadata(req: Requirement) -> None:
    meta = req.metadata
    for field_name in sorted(REQUIRED_FIELDS - meta.keys()):
        _add(req, "E_REQUIRED_FIELD", f"missing required field '{field_name}'")

    for key in meta:
        if key not in REQUIRED_FIELDS | OPTIONAL_FIELDS:
            _add(req, "E_UNKNOWN_FIELD", f"unknown metadata field '{key}'")

    for key in (REQUIRED_FIELDS | {"component", "source", "priority"}) & meta.keys():
        value = meta[key]
        if not isinstance(value, str) or not value.strip():
            _add(req, "E_FIELD_TYPE", f"'{key}' must be a nonempty string")

    if "reqmd" in meta and meta["reqmd"] != VERSION:
        _add(req, "E_VERSION", f"reqmd must be the quoted string '{VERSION}'")
    if isinstance(meta.get("id"), str) and not ID_PATTERN.fullmatch(meta["id"]):
        _add(req, "E_ID", "invalid requirement ID; expected e.g. REQ-DB-018")
    if isinstance(meta.get("type"), str) and meta["type"] not in TYPES:
        _add(req, "E_TYPE", f"unsupported requirement type '{meta['type']}'")
    if isinstance(meta.get("status"), str) and meta["status"] not in STATUSES:
        _add(req, "E_STATUS", f"unsupported status '{meta['status']}'")
    if isinstance(meta.get("priority"), str) and meta["priority"] not in PRIORITIES:
        _add(req, "E_PRIORITY", f"unsupported priority '{meta['priority']}'")

    trace = meta.get("trace")
    if trace is None:
        return
    if not isinstance(trace, dict):
        _add(req, "E_TRACE", "'trace' must be a mapping")
        return

    for relation, targets in trace.items():
        if relation not in TRACE_RELATIONS:
            _add(req, "E_TRACE", f"unsupported trace relation '{relation}'")
            continue
        if not isinstance(targets, list):
            _add(req, "E_TRACE", f"trace.{relation} must be a list")
            continue
        seen: set[str] = set()
        for target in targets:
            if not isinstance(target, str) or not ID_PATTERN.fullmatch(target):
                _add(req, "E_TRACE", f"invalid target in trace.{relation}: {target!r}")
                continue
            if target in seen:
                _add(req, "E_DUP_REF", f"duplicate trace.{relation} target '{target}'")
            if target == meta.get("id"):
                _add(req, "E_SELF_REF", f"requirement cannot {relation} itself")
            seen.add(target)


def _markdown_sections(req: Requirement, body: str, body_first_line: int) -> None:
    tokens = MARKDOWN.parse(body)
    lines = body.splitlines(keepends=True)
    h2_headers: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    seen_sections: set[str] = set()
    h1_count = 0

    for index, token in enumerate(tokens):
        # Markdown headings nested in quotes or lists do not define sections.
        if token.type != "heading_open" or token.level != 0:
            continue
        level = int(token.tag[1:])
        heading = tokens[index + 1].content.strip()
        start = token.map[0] if token.map else 0
        line = body_first_line + start

        if level == 1:
            h1_count += 1
            expected = f"{req.metadata.get('id')} — {req.metadata.get('title')}"
            if req.metadata.get("id") and req.metadata.get("title") and heading != expected:
                _add(req, "E_H1", f"H1 must match '{expected}'", line)
            if h1_count > 1:
                _add(req, "E_H1", "only one top-level H1 is permitted", line)
        elif level == 2:
            current = {"name": heading, "start": start, "line": line, "elements": []}
            h2_headers.append(current)
            if heading not in SECTION_ROLES:
                _add(req, "E_UNKNOWN_SECTION", f"unknown reserved heading '## {heading}'", line)
            elif heading in seen_sections:
                _add(req, "E_DUP_SECTION", f"duplicate section '## {heading}'", line)
            else:
                seen_sections.add(heading)
        elif level == 3 and current and current["name"] in {"Acceptance Criteria", "Diagrams"}:
            kind = current["name"]
            pattern = AC_PATTERN if kind == "Acceptance Criteria" else DIAGRAM_PATTERN
            match = pattern.fullmatch(heading)
            if not match:
                _add(
                    req, "E_ELEMENT_HEADING",
                    f"invalid {kind} heading; expected '### {'AC-01' if kind == 'Acceptance Criteria' else 'D-01'}: Title'",
                    line,
                )
            else:
                current["elements"].append(
                    {"id": match.group(1), "title": match.group(2), "start": start, "line": line}
                )

    seen_ac: set[str] = set()
    seen_diagrams: set[str] = set()
    for i, section in enumerate(h2_headers):
        end = h2_headers[i + 1]["start"] if i + 1 < len(h2_headers) else len(lines)
        name = section["name"]
        if name not in SECTION_ROLES:
            continue
        markdown = "".join(lines[section["start"] + 1 : end]).strip("\r\n")
        if name not in req.sections:
            req.sections[name] = markdown
        if name not in {"Acceptance Criteria", "Diagrams"}:
            continue

        elements = section["elements"]
        if not elements:
            _add(
                req, "E_NO_ELEMENTS",
                f"'## {name}' requires identified '###' entries",
                section["line"],
            )
        for j, element in enumerate(elements):
            element_end = elements[j + 1]["start"] if j + 1 < len(elements) else end
            source = "".join(lines[element["start"] + 1 : element_end]).strip("\r\n")
            identifier = element["id"]
            if name == "Acceptance Criteria":
                if identifier in seen_ac:
                    _add(req, "E_DUP_AC", f"duplicate criterion '{identifier}'", element["line"])
                seen_ac.add(identifier)
                if not source.strip():
                    _add(req, "E_EMPTY_AC", f"criterion '{identifier}' is empty", element["line"])
                req.acceptance_criteria.append(
                    {"id": identifier, "title": element["title"], "markdown": source}
                )
            else:
                if identifier in seen_diagrams:
                    _add(req, "E_DUP_DIAGRAM", f"duplicate diagram '{identifier}'", element["line"])
                seen_diagrams.add(identifier)
                fences = [
                    tok for tok in tokens
                    if tok.type == "fence"
                    and tok.level == 0
                    and tok.info.strip() == "mermaid"
                    and tok.map is not None
                    and element["start"] < tok.map[0] < element_end
                ]
                if len(fences) != 1 or not fences[0].content.strip():
                    _add(
                        req, "E_DIAGRAM",
                        f"diagram '{identifier}' requires exactly one nonempty mermaid fence",
                        element["line"],
                    )
                req.diagrams.append(
                    {
                        "id": identifier,
                        "title": element["title"],
                        "language": "mermaid",
                        "source": fences[0].content if len(fences) == 1 else "",
                        "role": "informative",
                    }
                )

    if "Statement" not in req.sections or not req.sections["Statement"].strip():
        _add(req, "E_STATEMENT", "a nonempty '## Statement' is required")

    if req.metadata.get("status") == "approved":
        for required in ("Acceptance Criteria", "Verification"):
            if not req.sections.get(required, "").strip():
                _add(req, "E_APPROVAL_GATE", f"approved requirement needs '## {required}'")
        if req.sections.get("Open Questions", "").strip():
            _add(req, "E_OPEN_QUESTIONS", "approved requirement has unresolved open questions")

    # A Mermaid fence outside a named diagram is an error, even if it renders.
    for token in tokens:
        if token.type != "fence" or token.info.strip() != "mermaid" or token.map is None:
            continue
        start = token.map[0]
        in_diagram = any(
            section["name"] == "Diagrams"
            and any(
                el["start"] < start < (
                    section["elements"][j + 1]["start"]
                    if j + 1 < len(section["elements"])
                    else (
                        h2_headers[i + 1]["start"]
                        if i + 1 < len(h2_headers)
                        else len(lines)
                    )
                )
                for j, el in enumerate(section["elements"])
            )
            for i, section in enumerate(h2_headers)
        )
        if not in_diagram:
            _add(
                req, "E_MERMAID_PLACEMENT",
                "mermaid fence must appear inside a named '### D-NN: Title' entry",
                body_first_line + start,
            )


def parse_text(text: str, path: str = "<memory>") -> Requirement:
    """Parse a single document and collect errors without executing its content."""
    req = Requirement(path=path)
    body, body_first_line = _front_matter(req, text)
    _validate_metadata(req)
    _markdown_sections(req, body, body_first_line)
    return req


def parse_file(path: Path) -> Requirement:
    try:
        return parse_text(path.read_text(encoding="utf-8"), str(path))
    except (OSError, UnicodeError) as exc:
        req = Requirement(path=str(path))
        _add(req, "E_READ", f"cannot read UTF-8 requirement: {exc}")
        return req


def collect_files(inputs: Iterable[Path]) -> list[Path]:
    """Expand files/directories into a deterministic, de-duplicated file list."""
    found: dict[str, Path] = {}
    for item in inputs:
        if item.is_dir():
            paths = item.rglob("*.req.md")
        else:
            paths = [item]
        for path in paths:
            found[str(path.resolve())] = path
    return sorted(found.values(), key=lambda p: str(p))


def validate_files(paths: Iterable[Path]) -> list[Requirement]:
    docs = [parse_file(path) for path in paths]
    by_id: dict[str, Requirement] = {}
    for req in docs:
        identifier = req.metadata.get("id")
        if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier):
            continue
        if identifier in by_id:
            _add(req, "E_DUP_ID", f"duplicate requirement ID '{identifier}'")
            _add(by_id[identifier], "E_DUP_ID", f"duplicate requirement ID '{identifier}'")
        else:
            by_id[identifier] = req

    for req in docs:
        trace = req.metadata.get("trace")
        if not isinstance(trace, dict):
            continue
        for relation, targets in trace.items():
            if relation not in TRACE_RELATIONS or not isinstance(targets, list):
                continue
            for target in targets:
                if (
                    isinstance(target, str)
                    and ID_PATTERN.fullmatch(target)
                    and target != req.metadata.get("id")
                    and target not in by_id
                ):
                    _add(req, "E_UNRESOLVED_REF", f"trace.{relation} target '{target}' is absent")
    return docs
