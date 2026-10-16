#!/usr/bin/env python3
"""Generate complete, package-scoped proposals from guidance_full.yaml.

Usage (run from this directory):
    Windows PowerShell: python generate_guidance_subsets.py
    WSL:                python3 generate_guidance_subsets.py

The script reads ../guidance_full.yaml and scans every section-04/section-NN.adoc
file. Generated YAML subsets and subset_generation.log are written beside this
script. It uses only the Python standard library.
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
GUIDANCE_FILE = SCRIPT_DIR.parent / "guidance_full.yaml"
SECTION_DIR = SCRIPT_DIR.parents[1] / "001-cg3pre" / "sections" / "section-04"
LOG_FILE = SCRIPT_DIR / "subset_generation.log"

CLASS_LINE = re.compile(r"^- name:\s*(.*)$")
MACRO_LINE = re.compile(r"^\s*lutaml_klass_table::[^\[]+\[([^\]]*)\]")
MACRO_ATTRIBUTE = re.compile(r'([\w-]+)="((?:\\.|[^"])*)"')


@dataclass(frozen=True)
class GuidanceClass:
    name: str
    package_path: tuple[str, ...]
    source_block: str

    @property
    def class_name(self) -> str:
        return self.name.rsplit("::", 1)[-1]

    @property
    def package_name(self) -> str:
        return self.package_path[-1]


@dataclass(frozen=True)
class TableCall:
    package: str | None
    name: str | None
    location: str


def fail(message: str) -> None:
    raise SystemExit(f"Error: {message}")


def parse_class_name(lines: list[str], line_index: int) -> str:
    match = CLASS_LINE.match(lines[line_index].rstrip("\r\n"))
    if not match:
        fail(f"Could not parse guidance class header: {lines[line_index].rstrip()}")
    value = match.group(1).strip()
    if not value.startswith(('"', "'")):
        return value

    quote = value[0]
    parts: list[str] = []
    remainder = value[1:]
    current_line = line_index
    while True:
        index = 0
        while index < len(remainder):
            if quote == '"' and remainder[index] == "\\":
                index += 2
                continue
            if remainder[index] == quote:
                if quote == "'" and remainder[index : index + 2] == "''":
                    index += 2
                    continue
                parts.append(remainder[:index])
                scalar = " ".join(part.strip() for part in parts)
                if quote == "'":
                    return scalar.replace("''", "'")
                return scalar.replace(r"\"", '"').replace(r"\\", "\\")
            index += 1

        parts.append(remainder.strip())
        current_line += 1
        if current_line >= len(lines):
            fail(f"Unterminated quoted guidance class name: {lines[line_index].rstrip()}")
        remainder = lines[current_line].strip()


def package_path_for(class_name: str) -> tuple[str, ...]:
    parts = tuple(part for part in class_name.split("::") if part)
    try:
        model_index = parts.index("Model")
    except ValueError:
        fail(f"Class is outside the expected model namespace: {class_name}")

    package_path = parts[model_index + 1 : -1]
    if not package_path:
        fail(f"Class has no package component: {class_name}")
    return package_path


def parse_guidance_classes(path: Path) -> list[GuidanceClass]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    starts = [
        index
        for index, line in enumerate(lines)
        if CLASS_LINE.match(line.rstrip("\r\n"))
    ]
    if not starts:
        fail(f"No top-level class entries found in {path}")

    classes: list[GuidanceClass] = []
    for start_index, start in enumerate(starts):
        end = starts[start_index + 1] if start_index + 1 < len(starts) else len(lines)
        name = parse_class_name(lines, start)
        block = "".join(lines[start:end]).rstrip() + "\n"
        classes.append(
            GuidanceClass(
                name=name,
                package_path=package_path_for(name),
                source_block=block,
            ),
        )
    return classes


def parse_table_calls(section_dir: Path) -> tuple[list[TableCall], int]:
    section_files = sorted(section_dir.glob("section-*.adoc"))
    if not section_files:
        fail(f"No section-*.adoc files found in {section_dir}")

    calls: list[TableCall] = []
    for section_file in section_files:
        for line_number, line in enumerate(
            section_file.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            stripped = line.lstrip()
            if stripped.startswith("//"):
                continue
            match = MACRO_LINE.match(line)
            if not match:
                continue

            attributes: dict[str, str] = {}
            for attribute in MACRO_ATTRIBUTE.finditer(match.group(1)):
                attributes[attribute.group(1)] = (
                    attribute.group(2).replace(r"\"", '"').replace(r"\\", "\\")
                )
            calls.append(
                TableCall(
                    package=attributes.get("package"),
                    name=attributes.get("name"),
                    location=f"{section_file.name}:{line_number}",
                ),
            )
    return calls, len(section_files)


def output_filenames(
    package_names: set[str],
) -> dict[str, str]:
    filenames: dict[str, str] = {}
    used_names: set[str] = set()
    for package_name in sorted(package_names):
        safe_scope = "".join(
            character if character.isalnum() or character in "._-" else "_"
            for character in package_name
        ).strip("._-")
        filename = f"guidance_{safe_scope}.yaml"
        if filename.casefold() in used_names:
            digest = hashlib.sha256(package_name.encode("utf-8")).hexdigest()[:8]
            filename = f"guidance_{safe_scope}_{digest}.yaml"
            if filename.casefold() in used_names:
                fail(f"Package paths produce the same output filename: {filename}")
        used_names.add(filename.casefold())
        filenames[package_name] = filename
    return filenames


def collect_call_report(
    classes: list[GuidanceClass],
    calls: list[TableCall],
) -> list[str]:
    classes_by_name: dict[str, list[GuidanceClass]] = defaultdict(list)
    for guidance_class in classes:
        classes_by_name[guidance_class.class_name].append(guidance_class)

    matched_classes: set[str] = set()
    counts_by_full_name = Counter(guidance_class.name for guidance_class in classes)
    report = [
        f"DUPLICATE CANONICAL ENTRY: {name} appears {count} times; all copies retained"
        for name, count in counts_by_full_name.items()
        if count > 1
    ]
    for call in calls:
        if not call.name:
            report.append(f"INCOMPLETE TABLE CALL: {call.location} has no name selector")
            continue
        candidates = classes_by_name.get(call.name, [])
        if not candidates:
            continue

        if call.package is None:
            candidate_scopes = {candidate.package_name for candidate in candidates}
            if len(candidate_scopes) == 1:
                matched_classes.update(candidate.name for candidate in candidates)
            else:
                report.append(
                    f"AMBIGUOUS TABLE CALL: {call.location} selects name={call.name!r} "
                    f"without a package; it occurs in {len(candidate_scopes)} guidance scopes",
                )
            continue

        exact_matches = [
            candidate
            for candidate in candidates
            if candidate.package_name == call.package
        ]
        exact_scopes = {candidate.package_name for candidate in exact_matches}
        if len(exact_scopes) == 1:
            matched_classes.update(candidate.name for candidate in exact_matches)
        elif len(exact_scopes) > 1:
            report.append(
                f"AMBIGUOUS PACKAGE MATCH: {call.location} package={call.package!r}, "
                f"name={call.name!r} matches {len(exact_scopes)} guidance scopes",
            )
        elif len({candidate.package_name for candidate in candidates}) == 1:
            report.append(
                f"PACKAGE MISMATCH: {call.location} package={call.package!r}, "
                f"name={call.name!r}; guidance class is {candidates[0].name}",
            )
        else:
            report.append(
                f"UNRESOLVED TABLE CALL: {call.location} package={call.package!r}, "
                f"name={call.name!r} matches no unique guidance class",
            )

    for guidance_class in classes:
        if guidance_class.name not in matched_classes:
            report.append(
                f"NO SECTION-04 TABLE CALL: {guidance_class.name}",
            )
    return report


def write_subsets(
    classes: list[GuidanceClass],
    filenames: dict[str, str],
) -> list[tuple[str, int]]:
    grouped: dict[str, list[GuidanceClass]] = defaultdict(list)
    for guidance_class in classes:
        grouped[guidance_class.package_name].append(guidance_class)

    written: list[tuple[str, int]] = []
    for package_name in sorted(grouped):
        filename = filenames[package_name]
        subset_classes = grouped[package_name]
        output = SCRIPT_DIR / filename
        yaml_text = "---\nclasses:\n" + "".join(
            guidance_class.source_block for guidance_class in subset_classes
        )
        output.write_text(yaml_text, encoding="utf-8", newline="")
        reparsed_classes = parse_guidance_classes(output)
        expected_names = Counter(item.name for item in subset_classes)
        actual_names = Counter(item.name for item in reparsed_classes)
        if expected_names != actual_names:
            fail(f"Generated subset does not preserve all class entries: {output}")
        if any(item.package_name != package_name for item in reparsed_classes):
            fail(f"Generated subset contains a class from another package: {output}")
        written.append((filename, len(subset_classes)))
    return written


def main() -> int:
    if not GUIDANCE_FILE.is_file():
        fail(f"Canonical guidance file not found: {GUIDANCE_FILE}")
    if not SECTION_DIR.is_dir():
        fail(f"Section directory not found: {SECTION_DIR}")

    classes = parse_guidance_classes(GUIDANCE_FILE)
    calls, section_file_count = parse_table_calls(SECTION_DIR)
    package_names = {guidance_class.package_name for guidance_class in classes}
    filenames = output_filenames(package_names)

    report = collect_call_report(classes, calls)
    written = write_subsets(classes, filenames)

    log_lines = [
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Canonical guidance: {GUIDANCE_FILE}",
        f"Scanned section directory: {SECTION_DIR}",
        f"Section files scanned: {section_file_count}",
        f"Active lutaml_klass_table calls found: {len(calls)}",
        f"Canonical class entries: {len(classes)}",
        "Subset grouping: immediate containing package in each qualified class name",
        f"Package subsets generated: {len(written)}",
        "",
        "Generated files:",
    ]
    log_lines.extend(
        f"  {filename}: {class_count} class entries"
        for filename, class_count in written
    )
    log_lines.extend(["", f"Cross-check notes: {len(report)}"])
    log_lines.extend(f"  {item}" for item in report)
    LOG_FILE.write_text("\n".join(log_lines) + "\n", encoding="utf-8", newline="")

    print(f"Generated {len(written)} package subset file(s) from {len(classes)} classes.")
    print(f"Log: {LOG_FILE}")
    for filename, class_count in written:
        print(f"  {filename}: {class_count} class entries")
    if report:
        print(f"Cross-check notes written to log: {len(report)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
