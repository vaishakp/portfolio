#!/usr/bin/env python3
"""Generate the one-page CV (content/cv/_index.md) and the homepage talk list
(data/cv_talks.json) from the LaTeX CV.

The CV (moderncv, github.com/vaishakp/vaishak_cv_v2) is the source. This script
reads the section files in the order main.tex lists them and writes them as one
Markdown page, with a contents line at the top and fixed anchors for the
sections the site menu links to (#publications, #talks, #conferences, ...).
The talks of sections/talks.tex are also written, newest first, to a data file
that the homepage's cv-talks block (layouts/_partials/hbx/blocks/) shows.

Edit the CV, then rerun:

    python scripts/cv_to_site.py --cv ~/Documents/cv

Left out: the referees (sections/references.tex), the contact details
(personal.tex), papers in EXCLUDED_ARXIV, and, unless asked for, the
"In preparation" papers and the "Pending" grant applications.

Only the subset of LaTeX the CV uses is converted: \\cvitem, \\cventry,
\\section, \\subsection, \\httplink, \\textbf, \\emph, \\texttt, \\normalfont,
itemize/enumerate, accents and a few symbols. Anything else is left as text and
reported, so a new macro in the CV shows up as a warning rather than silently
disappearing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GENERATED_NOTE = (
    "<!-- Generated from the CV by scripts/cv_to_site.py. "
    "Edit the CV and rerun the script; changes made here are overwritten. -->"
)
OWNER = "Vaishak Prasad"
# Papers in the CV that are not listed on the site (also excluded from the weekly
# arXiv/INSPIRE job in .github/workflows/update-publications.yml).
EXCLUDED_ARXIV = {"2610.19688"}  # ICTS-TIFR simulation catalog
SKIPPED_FILES = {"references"}
# Fixed anchors for the sections the menu links to; other sections get a slug.
ANCHORS = {
    "Positions held": "positions",
    "Ph.D. Thesis": "thesis",
    "Publications": "publications",
    "Fellowships, Grants, and Awards": "awards",
    "Invited Talks and Seminars": "talks",
    "Contributed Talks and Posters": "contributed-talks",
    "Projects Guided, Mentoring and Teaching": "teaching",
    "Academic Service": "service",
    "Science outreach activities": "outreach",
    "Computing skills and interests": "skills",
    "Codes developed": "codes",
    "Conferences and Schools": "conferences",
}
# Short names for the contents line at the top of the page.
CONTENTS = [
    ("Positions", "positions"),
    ("Education", "thesis"),
    ("Research", "research-interests"),
    ("Publications", "publications"),
    ("Awards", "awards"),
    ("Talks", "talks"),
    ("Teaching", "teaching"),
    ("Service", "service"),
    ("Outreach", "outreach"),
    ("Skills & codes", "skills"),
    ("Conferences", "conferences"),
]

ACCENTS = {
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "E": "É"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"},
    '"': {"a": "ä", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"},
    "~": {"n": "ñ", "a": "ã", "o": "õ"},
}
SYMBOLS = {"l": "ł", "L": "Ł", "o": "ø", "ss": "ß"}
IGNORED = {"small", "footnotesize", "normalsize", "newline", "noindent", "centering"}

unknown_macros: set[str] = set()


def read_group(text: str, pos: int, open_ch: str = "{", close_ch: str = "}") -> tuple[str, int]:
    """Return the contents of the balanced group starting at text[pos] and the index after it."""
    if text[pos] != open_ch:
        raise ValueError(f"expected {open_ch!r} at {pos}: {text[pos:pos + 40]!r}")
    depth = 0
    for i in range(pos, len(text)):
        ch = text[i]
        if ch == open_ch and text[i - 1] != "\\":
            depth += 1
        elif ch == close_ch and text[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return text[pos + 1 : i], i + 1
    raise ValueError(f"unbalanced group at {pos}")


def skip_space(text: str, pos: int) -> int:
    while pos < len(text) and text[pos] in " \t\n":
        pos += 1
    return pos


def read_args(text: str, pos: int, n: int) -> tuple[list[str], int]:
    args = []
    for _ in range(n):
        pos = skip_space(text, pos)
        arg, pos = read_group(text, pos)
        args.append(arg)
    return args, pos


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def latex_to_md(text: str) -> str:
    """Convert one CV field to Markdown (inline; lists become <br>-separated lines)."""
    out = []
    pos = 0
    while pos < len(text):
        ch = text[pos]
        if ch == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", text[pos:])
            name = m.group(1)
            pos += m.end()
            if name in ACCENTS:
                pos = skip_space(text, pos)
                if text[pos] == "{":
                    letter, pos = read_group(text, pos)
                else:
                    letter, pos = text[pos], pos + 1
                letter = letter.replace("\\", "")
                out.append(ACCENTS[name].get(letter, letter))
            elif name in SYMBOLS:
                if pos < len(text) and text[pos] == "{":
                    _, pos = read_group(text, pos)
                out.append(SYMBOLS[name])
            elif name == "httplink":
                pos = skip_space(text, pos)
                label, pos = read_group(text, pos, "[", "]")
                (url,), pos = read_args(text, pos, 1)
                pos2 = skip_space(text, pos)
                suffix = ""
                if pos2 < len(text) and text[pos2] == "{":
                    suffix, pos = read_group(text, pos2)
                suffix = latex_to_md(suffix)
                label = latex_to_md(label).rstrip(".")
                out.append(f"[{label}]({url})" + (f" {suffix}" if suffix else ""))
            elif name in ("textbf", "emph", "texttt", "normalfont", "textsc", "textit"):
                pos = skip_space(text, pos)
                if pos < len(text) and text[pos] == "{":
                    (inner,), pos = read_args(text, pos, 1)
                    inner = latex_to_md(inner)
                    wrap = {"textbf": "**", "emph": "*", "textit": "*", "texttt": "`"}.get(name, "")
                    out.append(f"{wrap}{inner}{wrap}")
            elif name in ("begin", "end"):
                (_env,), pos = read_args(text, pos, 1)
            elif name == "item":
                out.append("<br>• ")
            elif name in ("&", "%", "$", "#", "_"):
                out.append(name)
            elif name == "quad":
                out.append(" — ")
            elif name in (",", " "):
                out.append(" ")
            elif name in IGNORED:
                out.append(" ")
            else:
                unknown_macros.add(name)
                out.append(name)
        elif ch in "{}":
            pos += 1
        elif ch == "~":
            out.append(" ")
            pos += 1
        else:
            out.append(ch)
            pos += 1
    md = "".join(out)
    md = md.replace("---", "—").replace("--", "–").replace("``", "“").replace("''", "”")
    md = re.sub(r"\s*<br>\s*", "<br>", md)
    return re.sub(r"\s+", " ", md).strip()


def parse_blocks(tex: str) -> list[tuple[str, object]]:
    """Return ("section", title), ("subsection", title), ("cvitem", [date, body]) and
    ("cventry", [six fields]) in document order."""
    tex = strip_comments(tex)
    blocks: list[tuple[str, object]] = []
    pattern = re.compile(r"\\(section|subsection|cvitem|cventry)\b|\\begin\{center\}")
    pos = 0
    while True:
        m = pattern.search(tex, pos)
        if not m:
            break
        if m.group(0).startswith("\\begin{center}"):
            end = tex.index("\\end{center}", m.end())
            blocks.append(("subsection", latex_to_md(tex[m.end() : end]).strip("*")))
            pos = end + len("\\end{center}")
            continue
        kind = m.group(1)
        nargs = {"section": 1, "subsection": 1, "cvitem": 2, "cventry": 6}[kind]
        args, pos = read_args(tex, m.end(), nargs)
        blocks.append((kind, args[0] if nargs == 1 else args))
    return blocks


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def bold_owner(text: str) -> str:
    text = text.replace(f"**{OWNER}**", OWNER)
    return text.replace(OWNER, f"**{OWNER}**")


def item_line(fields: list[str]) -> str:
    when, body = (latex_to_md(f) for f in fields)
    return f"- **{when}** — {body}" if when else f"- {body}"


def entry_line(fields: list[str]) -> str:
    """A generic \\cventry{date}{title}{employer}{city}{grade}{description}."""
    when, *rest = (latex_to_md(f) for f in fields)
    *main, description = rest
    main = [part.rstrip(".") for part in main if part]
    text = ". ".join(main)
    if description:
        text = f"{text}<br>{description}".replace("<br><br>", "<br>") if text else description
    return f"- **{when}** — {text}" if when else f"- {text}"


def publication_line(fields: list[str]) -> str:
    _num, lead, others, title_date, links, note = (latex_to_md(f) for f in fields)
    authors = lead if not others else (f"{lead} {others}" if others.startswith("and ") else f"{lead}, {others}")
    authors = bold_owner(authors)
    m = re.match(r'"(.*?)\.?"\s*,?\s*(.*)$', title_date)
    title, status = (m.group(1), m.group(2).rstrip(".")) if m else (title_date.strip('".'), "")
    end = "" if title.endswith(("?", "!")) else "."
    parts = [f"{authors}. **{title}**{end}"]
    if links:
        parts.append(links.rstrip(".") + ".")
    if status:
        parts.append(f"{status}.")
    line = " ".join(parts)
    if note:
        line += f'<br><span class="pub-note">{note.rstrip(".")}.</span>'
    return line


def section_files(cv: Path) -> list[Path]:
    """The section files in the order main.tex inputs them."""
    main = strip_comments((cv / "main.tex").read_text(encoding="utf-8"))
    names = re.findall(r"\\input\{sections/([^}]+)\}", main)
    return [cv / "sections" / f"{name.removesuffix('.tex')}.tex" for name in names if name not in SKIPPED_FILES]


def cv_page(cv: Path, date: str, include_in_prep: bool, include_pending: bool) -> str:
    lines = [
        f"---\ntitle: Curriculum Vitae\ndate: {date}\ntype: page\n---\n",
        GENERATED_NOTE,
        "",
        '<p class="cv-contents">'
        + " · ".join(f'<a href="#{anchor}">{name}</a>' for name, anchor in CONTENTS)
        + ' · <a href="/uploads/resume.pdf"><strong>PDF</strong></a></p>',
        "",
    ]
    for path in section_files(cv):
        section = subsection = ""
        for kind, value in parse_blocks(path.read_text(encoding="utf-8")):
            if kind == "section":
                section, subsection = latex_to_md(value), ""
                lines.append(f"\n## {section} {{#{ANCHORS.get(section, slug(section))}}}\n")
                continue
            if kind == "subsection":
                subsection = latex_to_md(value)
                if skipped(subsection, include_in_prep, include_pending):
                    continue
                heading = "Journal articles and preprints" if subsection.lower().startswith("published") else subsection
                lines.append(f"\n### {heading}\n")
                continue
            if skipped(subsection, include_in_prep, include_pending):
                continue
            if section == "Publications" and kind == "cventry":
                if any(arxiv_id in value[4] for arxiv_id in EXCLUDED_ARXIV):
                    continue
                lines.append(f"1. {publication_line(value)}")
            elif kind == "cvitem":
                lines.append(item_line(value))
            else:
                lines.append(entry_line(value))
    return "\n".join(lines) + "\n"


MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def date_key(when: str) -> str:
    """Sort key "YYYY-MM" for CV dates such as "Aug 2026", "Jun-Jul 2025" or "2018"."""
    year = re.findall(r"(?:19|20)\d\d", when)
    month = re.match(r"\s*([A-Za-z]{3})", when)
    m = MONTHS.get(month.group(1).lower(), 0) if month else 0
    return f"{year[-1] if year else '0000'}-{m:02d}"


def talks_data(cv: Path) -> list[dict]:
    """The talks of sections/talks.tex, newest first (stable within a month)."""
    talks = []
    section = subsection = ""
    for kind, value in parse_blocks((cv / "sections" / "talks.tex").read_text(encoding="utf-8")):
        if kind == "section":
            section, subsection = latex_to_md(value), ""
        elif kind == "subsection":
            subsection = latex_to_md(value)
        elif kind == "cvitem":
            when, body = (latex_to_md(f) for f in value)
            talks.append({
                "date": when,
                "sort": date_key(when),
                "invited": section.lower().startswith("invited"),
                "group": subsection or section,
                "text": body,
            })
    return sorted(talks, key=lambda t: t["sort"], reverse=True)


def write_if_changed(path: Path, text: str, check: bool) -> bool:
    """Write text to path unless it is already there; True if it was out of date."""
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old == text:
        print(f"{path} is up to date.")
        return False
    if check:
        print(f"{path} is out of date.")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"updated {path}")
    return True


def skipped(subsection: str, include_in_prep: bool, include_pending: bool) -> bool:
    name = subsection.lower()
    return (name.startswith("in preparation") and not include_in_prep) or (
        name == "pending" and not include_pending
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__
    )
    parser.add_argument("--cv", type=Path, default=Path.home() / "Documents" / "cv",
                        help="CV checkout containing main.tex and sections/*.tex")
    parser.add_argument("--out", type=Path, default=Path("content/cv/_index.md"))
    parser.add_argument("--date", default="2026-10-31", help="front-matter date of the page")
    parser.add_argument("--include-in-prep", action="store_true",
                        help="also list the CV's 'In preparation' papers")
    parser.add_argument("--include-pending", action="store_true",
                        help="also list the CV's 'Pending' grant applications")
    parser.add_argument("--talks-data", type=Path, default=Path("data/cv_talks.json"))
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if an output is out of date, without writing it")
    args = parser.parse_args()

    page = cv_page(args.cv, args.date, args.include_in_prep, args.include_pending)
    talks = json.dumps(talks_data(args.cv), indent=1, ensure_ascii=False) + "\n"
    if unknown_macros:
        print("warning: LaTeX macros left unconverted: " + ", ".join(sorted(unknown_macros)),
              file=sys.stderr)
    stale = [write_if_changed(args.out, page, args.check),
             write_if_changed(args.talks_data, talks, args.check)]
    return 1 if args.check and any(stale) else 0


if __name__ == "__main__":
    sys.exit(main())
