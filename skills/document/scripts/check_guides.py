#!/usr/bin/env python3
"""Mechanical checks for the two guides written by the repo-documenter skill.

Usage:
    check_guides.py --repo REPO --dev DEVELOPER_GUIDE.md --user USER_GUIDE.md
    check_guides.py --self-test

Reports ERROR lines (must fix) and WARN lines (look at each one). Exits 1 when
there is at least one error. It checks form only: Mermaid syntax faults, the
minimum set of diagrams, paths and links that do not resolve, placeholders, and
source-code references in the user guide. It cannot tell whether a guide is true.

shortcut: Mermaid is linted with regular expressions, not parsed. Render with
`mmdc` when a diagram is in doubt.
"""
import argparse
import glob
import re
import sys
from pathlib import Path

DIAGRAM_TYPES = (
    "flowchart", "graph", "sequenceDiagram", "stateDiagram-v2", "stateDiagram",
    "erDiagram", "classDiagram", "journey", "gantt", "pie", "mindmap", "timeline",
    "gitGraph", "quadrantChart", "requirementDiagram", "C4Context", "C4Container",
)
SEQ_OPENERS = ("alt", "opt", "loop", "par", "critical", "break", "rect", "box")
SOURCE_EXT = (
    "py", "js", "jsx", "ts", "tsx", "mjs", "cjs", "go", "rs", "java", "kt", "rb",
    "php", "cs", "c", "cc", "cpp", "h", "hpp", "swift", "dart", "scala", "sql",
    "vue", "svelte", "mdx", "sh",
)
ANY_EXT = SOURCE_EXT + (
    "json", "yaml", "yml", "toml", "md", "html", "css", "scss", "xml", "ini",
    "cfg", "env", "lock", "txt", "proto", "graphql", "tf", "gradle",
)
# Template fields that were never filled in. Case-sensitive notes such as TODO are only a warning:
# a guide may quote them from the code, and a to-do app says "todo" on every line.
PLACEHOLDER = re.compile(r"lorem ipsum|<(repo name|product name|YYYY-MM-DD|short sha[^>]*)>", re.I)
NOTE = re.compile(r"\b(TODO|TBD|FIXME)\b")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# A square-bracket label that holds a bracket but is not quoted and is not a shape such as [(db)] or [[sub]].
BAD_LABEL = re.compile(r"\w\[(?![(\[/\\\"])[^\]\"]*[(){}][^\]\"]*\]")
END_AS_NODE = re.compile(r"(-->|---|-\.->|==>)\s*(\|[^|]*\|\s*)?end\b|^\s*end\s*(-->|---|-\.->|==>|\[|\(|\{)")


def split_blocks(text):
    """Return (mermaid_blocks, prose_lines).

    mermaid_blocks: list of (start_line, [lines]). prose_lines: list of
    (line_number, text) for lines outside every fenced block.
    """
    blocks, prose, fence, lang, start, buf = [], [], None, "", 0, []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if fence is None:
            opener = re.match(r"^(`{3,}|~{3,})\s*([\w+-]*)", stripped)
            if opener:
                fence, lang, start, buf = opener.group(1), opener.group(2).lower(), number, []
            else:
                prose.append((number, line))
        elif stripped.startswith(fence) and stripped.strip(fence[0]) == "":
            if lang == "mermaid":
                blocks.append((start, buf))
            fence = None
        else:
            buf.append(line)
    unclosed = start if fence is not None else None
    return blocks, prose, unclosed


def diagram_type(lines):
    for line in lines:
        text = line.strip()
        if not text or text.startswith("%%"):
            continue
        for kind in DIAGRAM_TYPES:
            if text == kind or text.startswith(kind + " ") or text.startswith(kind + ":"):
                return "flowchart" if kind == "graph" else kind.replace("stateDiagram-v2", "stateDiagram")
        return None
    return ""


def check_mermaid(start, lines):
    """Return a list of (level, line, message) for one Mermaid block."""
    out = []
    kind = diagram_type(lines)
    if kind == "":
        return [("ERROR", start, "empty Mermaid block")]
    if kind is None:
        return [("ERROR", start, "Mermaid block does not start with a known diagram type")]
    body = [(start + offset, line.strip()) for offset, line in enumerate(lines, 1)
            if line.strip() and not line.strip().startswith("%%")]
    ends = sum(1 for _, text in body if text == "end")
    if kind == "flowchart":
        opens = sum(1 for _, text in body if text.startswith("subgraph"))
        if opens != ends:
            out.append(("ERROR", start, f"flowchart has {opens} subgraph but {ends} end"))
        for number, text in body:
            if END_AS_NODE.search(text):
                out.append(("ERROR", number, "'end' used as a node id; rename it (for example 'finish')"))
            if BAD_LABEL.search(text):
                out.append(("WARN", number, "label holds brackets but is not quoted; write id[\"text (more)\"]"))
        if len(body) > 45:
            out.append(("WARN", start, f"large flowchart ({len(body)} lines); consider splitting it"))
    elif kind == "sequenceDiagram":
        opens = sum(1 for _, text in body if text.split(" ")[0] in SEQ_OPENERS)
        if opens != ends:
            out.append(("ERROR", start, f"sequence diagram has {opens} block openers but {ends} end"))
        for number, text in body:
            if "->>" in text or "-->>" in text:
                if ":" not in text:
                    out.append(("ERROR", number, "sequence message has no ': text'"))
                elif ";" in text.split(":", 1)[1]:
                    out.append(("WARN", number, "semicolon in message text may break rendering"))
    elif kind == "erDiagram":
        for number, text in body:
            if re.search(r"[|}o]{1,2}(--|\.\.)[|{o]{1,2}", text) and ":" not in text:
                out.append(("ERROR", number, "relation has no ': label'"))
    return out


def looks_like_path(code):
    """A code span that names a file or folder: has a slash or a known extension, no spaces."""
    code = re.sub(r"(:\d+(-\d+)?|\(\))$", "", code.strip())
    if not code or " " in code or code.startswith(("http", "-", "/", "@", "$", "~", "<")):
        return None
    if re.search(r"[*{}<>|=]", code) or not re.fullmatch(r"[\w.\-/\[\]()+]+", code):
        return None
    extension = code.rsplit(".", 1)[-1].lower() if "." in code.rsplit("/", 1)[-1] else ""
    if extension in ANY_EXT or code.endswith("/"):
        return code
    return None


def slug(heading):
    text = re.sub(r"[`*_~]", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def check_guide(path, repo, role, minimum):
    """Check one guide. role is 'dev' or 'user'. Returns (level, line, message) tuples."""
    out = []
    if not path.is_file():
        return [("ERROR", 0, f"file not found: {path}")]
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks, prose, unclosed = split_blocks(text)
    if unclosed:
        out.append(("ERROR", unclosed, "code fence opened here is never closed"))

    kinds = []
    for start, lines in blocks:
        kinds.append(diagram_type(lines))
        out.extend(check_mermaid(start, lines))
    if len(blocks) < minimum:
        out.append(("ERROR", 0, f"{len(blocks)} Mermaid diagrams; the standard needs at least {minimum}"))
    if "flowchart" not in kinds:
        out.append(("ERROR", 0, "no flowchart diagram (the high-level picture is required)"))
    if role == "dev" and "sequenceDiagram" not in kinds:
        out.append(("ERROR", 0, "no sequenceDiagram (each key flow needs one)"))

    headings = [(number, line) for number, line in prose if re.match(r"^#{1,6} ", line)]
    if sum(1 for _, line in headings if line.startswith("# ")) != 1:
        out.append(("WARN", 0, "expected exactly one H1 title"))
    if sum(1 for _, line in headings if line.startswith("## ")) < 6:
        out.append(("WARN", 0, "fewer than 6 sections; compare with the required sections in the standard"))
    anchors = {slug(line.lstrip("#")) for _, line in headings}

    other = "USER_GUIDE.md" if role == "dev" else "DEVELOPER_GUIDE.md"
    if other not in text:
        out.append(("WARN", 0, f"no link to the companion guide {other}"))

    for number, line in prose:
        hit = PLACEHOLDER.search(line)
        if hit:
            out.append(("ERROR", number, f"placeholder left in the text: {hit.group(0)}"))
        elif NOTE.search(line):
            out.append(("WARN", number, f"unfinished note in the text: {NOTE.search(line).group(0)}"))
        for target in LINK.findall(line):
            if re.match(r"^(https?:|mailto:|tel:)", target):
                continue
            file_part, _, anchor = target.partition("#")
            if not file_part:
                if anchor and anchor.lower() not in anchors:
                    out.append(("WARN", number, f"link to missing heading: #{anchor}"))
            elif not (path.parent / file_part).exists():
                out.append(("ERROR", number, f"link target not found: {file_part}"))
        for code in INLINE_CODE.findall(line):
            named = looks_like_path(code)
            if not named:
                continue
            extension = named.rsplit(".", 1)[-1].lower()
            # A bare name such as `Node.js` may be a product, not a file, so it is only a warning.
            level = "ERROR" if "/" in named else "WARN"
            if role == "user":
                if extension in SOURCE_EXT:
                    out.append((level, number, f"user guide names a source file: {named}"))
            elif repo and not (repo / named).exists() and not any(
                    repo.glob("**/" + glob.escape(named.strip("/")))):
                out.append((level, number, f"path not found in the repository: {named}"))
    return out


def report(name, results):
    for level, line, message in sorted(results, key=lambda item: (item[0], item[1])):
        print(f"{level} {name}:{line}: {message}" if line else f"{level} {name}: {message}")
    return sum(1 for level, _, _ in results if level == "ERROR")


def self_test():
    good = ["flowchart TD", "a[Start] --> b{Valid?}", "b -->|yes| c[\"Save (db)\"]", "subgraph s[\"Area\"]", "c --> d", "end"]
    assert check_mermaid(1, good) == [], check_mermaid(1, good)
    assert any("end" in m for _, _, m in check_mermaid(1, ["flowchart TD", "a --> end"]))
    assert any("not quoted" in m for _, _, m in check_mermaid(1, ["flowchart TD", "a[Save (db)] --> b"]))
    assert check_mermaid(1, ["flowchart TD", "a[(Database)] --> b([Done])"]) == []
    assert any("subgraph" in m for _, _, m in check_mermaid(1, ["flowchart TD", "subgraph x", "a --> b"]))
    seq = ["sequenceDiagram", "participant a", "a->>b: hi", "alt ok", "b-->>a: yes", "else no", "b-->>a: no", "end"]
    assert check_mermaid(1, seq) == [], check_mermaid(1, seq)
    assert any("openers" in m for _, _, m in check_mermaid(1, seq[:-1]))
    assert check_mermaid(1, ["pizza"])[0][2].startswith("Mermaid block does not start")
    assert check_mermaid(1, ["erDiagram", "USER ||--o{ ORDER : places"]) == []
    assert any("label" in m for _, _, m in check_mermaid(1, ["erDiagram", "USER ||--o{ ORDER"]))
    assert looks_like_path("src/app/main.ts:42") == "src/app/main.ts"
    assert looks_like_path("package.json") == "package.json"
    assert looks_like_path("src/components/") == "src/components/"
    assert looks_like_path("docs/") == "docs/"
    assert NOTE.search("see the TODO in code") and not NOTE.search("add a todo item")
    for not_a_path in ("application/json", "npm run dev", "/api/users", "createOrder()", "v1.2.3", "a/b"):
        assert looks_like_path(not_a_path) is None, not_a_path
    blocks, prose, unclosed = split_blocks("# T\n```mermaid\nflowchart TD\na-->b\n```\ntext\n```js\nx\n")
    assert len(blocks) == 1 and unclosed == 7 and [n for n, _ in prose] == [1, 6]
    assert slug(" Getting started ") == "getting-started"
    print("self-test passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, help="repository root, to check that named paths exist")
    parser.add_argument("--dev", type=Path, help="path of DEVELOPER_GUIDE.md")
    parser.add_argument("--user", type=Path, help="path of USER_GUIDE.md")
    parser.add_argument("--min-dev", type=int, default=4, help="minimum diagrams in the developer guide")
    parser.add_argument("--min-user", type=int, default=4, help="minimum diagrams in the user guide")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not (args.dev and args.user):
        parser.error("--dev and --user are required")
    if args.repo and not args.repo.is_dir():
        parser.error(f"--repo is not a folder: {args.repo}")
    errors = report(args.dev.name, check_guide(args.dev, args.repo, "dev", args.min_dev))
    errors += report(args.user.name, check_guide(args.user, args.repo, "user", args.min_user))
    print(f"{errors} error(s)" if errors else "no errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
