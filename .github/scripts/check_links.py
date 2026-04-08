#!/usr/bin/env python3
"""Scan Markdown files, validate links, and write a broken-link report."""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


REFERENCE_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
REFERENCE_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)", re.MULTILINE)
AUTOLINK_RE = re.compile(r"<((?:https?://|mailto:|tel:)[^>\s]+)>")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
EXPLICIT_ANCHOR_RE = re.compile(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)


@dataclasses.dataclass(frozen=True)
class LinkOccurrence:
    source: pathlib.Path
    line_number: int
    raw_target: str


@dataclasses.dataclass(frozen=True)
class ResolvedTarget:
    key: str
    display: str
    is_external: bool


def normalize_reference_label(label: str) -> str:
    return " ".join(label.strip().lower().split())


def split_link_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if not destination:
        return ""

    # Handle malformed nested markdown syntax like [label](https://...)
    nested_markdown_match = re.match(r"^\[[^\]]+\]\((.+)\)$", destination)
    if nested_markdown_match:
        return split_link_destination(nested_markdown_match.group(1))

    if destination.startswith("<"):
        end = destination.find(">")
        if end != -1:
            return destination[1:end].strip()

    out: List[str] = []
    escaped = False
    nesting = 0
    for ch in destination:
        if escaped:
            out.append(ch)
            escaped = False
            continue

        if ch == "\\":
            escaped = True
            continue

        if ch == "(":
            nesting += 1
        elif ch == ")" and nesting > 0:
            nesting -= 1

        if ch.isspace() and nesting == 0:
            break

        out.append(ch)

    return "".join(out).strip()


def extract_reference_definitions(content: str) -> Dict[str, str]:
    definitions: Dict[str, str] = {}
    for match in REFERENCE_DEF_RE.finditer(content):
        label = normalize_reference_label(match.group(1))
        destination = split_link_destination(match.group(2))
        if destination:
            definitions[label] = destination
    return definitions


def extract_inline_link_destinations(line: str) -> Iterable[str]:
    i = 0
    length = len(line)

    while i < length:
        if line[i] != "[":
            i += 1
            continue

        j = i + 1
        bracket_depth = 1
        escaped = False

        while j < length:
            ch = line[j]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == "[":
                bracket_depth += 1
            elif ch == "]":
                bracket_depth -= 1
                if bracket_depth == 0:
                    break
            j += 1

        if bracket_depth != 0:
            i += 1
            continue

        k = j + 1
        while k < length and line[k].isspace():
            k += 1

        if k >= length or line[k] != "(":
            i = j + 1
            continue

        k += 1
        start = k
        paren_depth = 1
        escaped = False
        in_angle_brackets = False

        while k < length:
            ch = line[k]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == "<" and not in_angle_brackets:
                in_angle_brackets = True
            elif ch == ">" and in_angle_brackets:
                in_angle_brackets = False
            elif not in_angle_brackets:
                if ch == "(":
                    paren_depth += 1
                elif ch == ")":
                    paren_depth -= 1
                    if paren_depth == 0:
                        destination = split_link_destination(line[start:k])
                        if destination:
                            yield destination
                        break
            k += 1

        i = k + 1


def iter_links_from_markdown(file_path: pathlib.Path) -> Iterable[LinkOccurrence]:
    content = file_path.read_text(encoding="utf-8", errors="replace")
    definitions = extract_reference_definitions(content)

    for line_number, line in enumerate(content.splitlines(), start=1):
        for destination in extract_inline_link_destinations(line):
            yield LinkOccurrence(file_path, line_number, destination)

        for match in REFERENCE_LINK_RE.finditer(line):
            text_label = match.group(1)
            explicit_label = match.group(2)
            label = explicit_label if explicit_label else text_label
            target = definitions.get(normalize_reference_label(label))
            if target:
                yield LinkOccurrence(file_path, line_number, target)

        for match in AUTOLINK_RE.finditer(line):
            yield LinkOccurrence(file_path, line_number, match.group(1))


def github_slugify(heading: str) -> str:
    heading = re.sub(r"<.*?>", "", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\-\s]", "", heading)
    heading = re.sub(r"\s+", "-", heading)
    heading = re.sub(r"-+", "-", heading)
    return heading.strip("-")


def collect_anchors(markdown_path: pathlib.Path) -> Set[str]:
    anchors: Set[str] = set()
    content = markdown_path.read_text(encoding="utf-8", errors="replace")

    for line in content.splitlines():
        heading_match = HEADING_RE.match(line)
        if heading_match:
            anchors.add(github_slugify(heading_match.group(1)))

        for anchor_match in EXPLICIT_ANCHOR_RE.finditer(line):
            anchors.add(anchor_match.group(1).strip())

    return anchors


def should_skip_target(target: str) -> bool:
    lowered = target.lower()
    return (
        not lowered
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
        or lowered.startswith("javascript:")
        or lowered.startswith("data:")
    )


def resolve_target(occurrence: LinkOccurrence, root: pathlib.Path) -> Optional[ResolvedTarget]:
    target = occurrence.raw_target.strip()
    if should_skip_target(target):
        return None

    parsed = urllib.parse.urlparse(target)

    if parsed.scheme in {"http", "https"}:
        normalized = urllib.parse.urlunparse(parsed)
        return ResolvedTarget(
            key=f"external::{normalized}",
            display=normalized,
            is_external=True,
        )

    path_part = urllib.parse.unquote(parsed.path)
    fragment = urllib.parse.unquote(parsed.fragment)

    if path_part.startswith("/"):
        resolved_file = root / path_part.lstrip("/")
    elif path_part:
        resolved_file = occurrence.source.parent / path_part
    else:
        resolved_file = occurrence.source

    resolved_file = resolved_file.resolve()

    display = resolved_file.relative_to(root).as_posix() if resolved_file.is_relative_to(root) else str(resolved_file)
    display = f"{display}#{fragment}" if fragment else display

    key = f"local::{resolved_file.as_posix()}#{fragment}"
    return ResolvedTarget(key=key, display=display, is_external=False)


def validate_local_target(
    occurrence: LinkOccurrence,
    root: pathlib.Path,
    anchor_cache: Dict[pathlib.Path, Set[str]],
) -> Tuple[ResolvedTarget, Optional[str]]:
    resolved = resolve_target(occurrence, root)
    if not resolved:
        # This path is skipped and never evaluated as broken.
        return ResolvedTarget("skip::", "", False), None

    target = occurrence.raw_target.strip()
    parsed = urllib.parse.urlparse(target)
    path_part = urllib.parse.unquote(parsed.path)
    fragment = urllib.parse.unquote(parsed.fragment)

    if path_part.startswith("/"):
        target_file = (root / path_part.lstrip("/")).resolve()
    elif path_part:
        target_file = (occurrence.source.parent / path_part).resolve()
    else:
        target_file = occurrence.source.resolve()

    if not target_file.exists():
        return resolved, "Target file does not exist"

    if target_file.is_dir():
        return resolved, "Target points to a directory"

    if fragment and target_file.suffix.lower() in {".md", ".markdown"}:
        anchors = anchor_cache.get(target_file)
        if anchors is None:
            anchors = collect_anchors(target_file)
            anchor_cache[target_file] = anchors
        if fragment not in anchors:
            return resolved, f"Missing anchor '#{fragment}'"

    return resolved, None


def check_external_link(url: str, timeout: float) -> Optional[str]:
    headers = {"User-Agent": "markdown-link-checker/1.0"}

    req = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status >= 400 and status not in {401, 403, 429}:
                return f"HTTP {status}"
            return None
    except urllib.error.HTTPError as err:
        if err.code in {405, 501}:
            pass
        elif err.code in {401, 403, 429}:
            return None
        else:
            return f"HTTP {err.code}"
    except urllib.error.URLError as err:
        return f"Network error: {err.reason}"
    except Exception as err:  # defensive fallback
        return f"Unexpected error: {err}"

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status >= 400 and status not in {401, 403, 429}:
                return f"HTTP {status}"
            return None
    except urllib.error.HTTPError as err:
        if err.code in {401, 403, 429}:
            return None
        return f"HTTP {err.code}"
    except urllib.error.URLError as err:
        return f"Network error: {err.reason}"
    except Exception as err:  # defensive fallback
        return f"Unexpected error: {err}"


def should_exclude(path: pathlib.Path, root: pathlib.Path, exclude_patterns: Sequence[str]) -> bool:
    rel_path = path.relative_to(root).as_posix()
    return any(path.match(pattern) or pathlib.PurePosixPath(rel_path).match(pattern) for pattern in exclude_patterns)


def find_markdown_files(root: pathlib.Path, exclude_patterns: Sequence[str]) -> List[pathlib.Path]:
    files: List[pathlib.Path] = []
    for candidate in root.rglob("*"):
        if candidate.is_file() and candidate.suffix.lower() in {".md", ".markdown"}:
            if not should_exclude(candidate, root, exclude_patterns):
                files.append(candidate)
    return sorted(files)


def build_report(
    root: pathlib.Path,
    report_path: pathlib.Path,
    markdown_files_count: int,
    links_checked_count: int,
    broken: Dict[str, Dict[str, object]],
) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines: List[str] = []

    lines.append("# Broken Links Report")
    lines.append("")
    lines.append(f"- Generated: {now}")
    lines.append(f"- Root scanned: {root.as_posix()}")
    lines.append(f"- Markdown files scanned: {markdown_files_count}")
    lines.append(f"- Links checked: {links_checked_count}")
    lines.append(f"- Broken links found: {len(broken)}")
    lines.append("")

    if not broken:
        lines.append("No broken links found.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Broken Link | Reason | Referenced From |")
    lines.append("| --- | --- | --- |")

    for broken_link in sorted(broken.keys()):
        entry = broken[broken_link]
        reason = entry["reason"]
        pages = sorted({
            occ.source.relative_to(root).as_posix()
            for occ in entry["occurrences"]
        })
        pages_display = "<br>".join(pages)
        lines.append(f"| {broken_link} | {reason} | {pages_display} |")

    lines.append("")
    lines.append("## Detailed References")
    lines.append("")

    for broken_link in sorted(broken.keys()):
        entry = broken[broken_link]
        lines.append(f"### {broken_link}")
        lines.append("")
        lines.append(f"Reason: {entry['reason']}")
        lines.append("")
        lines.append("Referenced from:")
        for occurrence in sorted(
            entry["occurrences"],
            key=lambda occ: (occ.source.as_posix(), occ.line_number),
        ):
            rel = occurrence.source.relative_to(root).as_posix()
            lines.append(f"- [{rel}]({rel}) (line {occurrence.line_number})")
        lines.append("")

    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).resolve()
    report_path = pathlib.Path(args.report).resolve()

    if not root.exists() or not root.is_dir():
        print(f"Root directory not found: {root}", file=sys.stderr)
        return 2

    default_excludes = ["**/.git/**"]
    exclude_patterns = default_excludes + args.exclude

    markdown_files = find_markdown_files(root, exclude_patterns)
    markdown_files = [path for path in markdown_files if path.resolve() != report_path]
    occurrences: List[LinkOccurrence] = []

    for markdown_file in markdown_files:
        occurrences.extend(iter_links_from_markdown(markdown_file))

    local_cache: Dict[str, Optional[str]] = {}
    external_cache: Dict[str, Optional[str]] = {}
    anchor_cache: Dict[pathlib.Path, Set[str]] = {}

    external_jobs: Dict[str, str] = {}
    local_occurrences: Dict[str, List[LinkOccurrence]] = defaultdict(list)
    external_occurrences: Dict[str, List[LinkOccurrence]] = defaultdict(list)

    for occurrence in occurrences:
        resolved = resolve_target(occurrence, root)
        if not resolved:
            continue

        if resolved.is_external:
            external_jobs.setdefault(resolved.key, resolved.display)
            external_occurrences[resolved.key].append(occurrence)
        else:
            local_occurrences[resolved.key].append(occurrence)

    for key, local_refs in local_occurrences.items():
        first = local_refs[0]
        resolved, reason = validate_local_target(first, root, anchor_cache)
        if resolved.key == "skip::":
            continue
        local_cache[key] = reason

    if args.check_external and external_jobs:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_key = {
                executor.submit(check_external_link, url, args.timeout): key
                for key, url in external_jobs.items()
            }
            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    external_cache[key] = future.result()
                except Exception as err:  # defensive fallback
                    external_cache[key] = f"Unexpected worker error: {err}"

    broken: Dict[str, Dict[str, object]] = {}

    for key, refs in local_occurrences.items():
        reason = local_cache.get(key)
        if reason:
            broken_display = resolve_target(refs[0], root).display
            broken[broken_display] = {
                "reason": reason,
                "occurrences": refs,
            }

    for key, refs in external_occurrences.items():
        reason = external_cache.get(key)
        if reason:
            broken_display = resolve_target(refs[0], root).display
            broken[broken_display] = {
                "reason": reason,
                "occurrences": refs,
            }

    links_checked = len(local_occurrences) + (len(external_occurrences) if args.check_external else 0)

    report = build_report(
        root=root,
        report_path=report_path,
        markdown_files_count=len(markdown_files),
        links_checked_count=links_checked,
        broken=broken,
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    print(f"Scanned {len(markdown_files)} Markdown files.")
    print(f"Checked {links_checked} unique links.")
    print(f"Found {len(broken)} broken links.")
    print(f"Report written to: {report_path}")

    return 1 if broken else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan Markdown files and report broken links.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--report",
        default="broken-links-report.md",
        help="Path to output Markdown report file.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout in seconds for external link checks.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=12,
        help="Number of concurrent workers for external link checks.",
    )
    parser.add_argument(
        "--no-external",
        action="store_true",
        help="Skip checking HTTP/HTTPS links.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern to exclude (can be repeated).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.check_external = not args.no_external

    if args.workers < 1:
        parser.error("--workers must be >= 1")

    if args.timeout <= 0:
        parser.error("--timeout must be > 0")

    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
