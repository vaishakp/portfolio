#!/usr/bin/env python3
"""Update Hugo publication entries from arXiv and INSPIRE.

The script is intentionally conservative:
- add new public preprints authored by the configured person;
- update existing "In preparation" entries when a public arXiv record appears;
- update journal/DOI metadata when INSPIRE has publication information;
- preserve existing hand-written summaries unless an entry was still in preparation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
import textwrap
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled in CI logs
    raise SystemExit("Missing dependency: install PyYAML before running this script.") from exc


ARXIV_API = "https://export.arxiv.org/api/query"
INSPIRE_API = "https://inspirehep.net/api/literature"
USER_AGENT = "vaishakprasad.com publication updater (mailto:vaishakprasad@psu.edu)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "publication"


def normalize_title(value: str) -> str:
    value = clean_text(value).lower()
    return re.sub(r"[^a-z0-9]+", "", value)


def normalize_arxiv_id(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()
    value = re.sub(r"^arxiv:", "", value, flags=re.I)
    value = value.rsplit("/", 1)[-1]
    value = re.sub(r"v\d+$", "", value)
    return value


def arxiv_id_from_url(value: str | None) -> str:
    if not value:
        return ""
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#]+)", value)
    if not match:
        return ""
    return normalize_arxiv_id(match.group(1).removesuffix(".pdf"))


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def query_arxiv(author: str, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": f'au:"{author}"',
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": str(max_results),
        }
    )
    root = ET.fromstring(fetch_text(f"{ARXIV_API}?{params}"))
    records = []
    for entry in root.findall("atom:entry", ATOM_NS):
        arxiv_url = clean_text(entry.findtext("atom:id", namespaces=ATOM_NS))
        arxiv_id = normalize_arxiv_id(arxiv_url)
        authors = [
            clean_text(author_el.findtext("atom:name", namespaces=ATOM_NS))
            for author_el in entry.findall("atom:author", ATOM_NS)
        ]
        authors = [name for name in authors if name]
        if author.lower() not in " ".join(authors).lower():
            continue
        category = ""
        primary = entry.find("arxiv:primary_category", ATOM_NS)
        if primary is not None:
            category = primary.attrib.get("term", "")
        doi = clean_text(entry.findtext("arxiv:doi", namespaces=ATOM_NS))
        if not doi and arxiv_id:
            doi = f"10.48550/arXiv.{arxiv_id}"
        records.append(
            {
                "source": "arxiv",
                "title": clean_text(entry.findtext("atom:title", namespaces=ATOM_NS)),
                "date": clean_text(entry.findtext("atom:published", namespaces=ATOM_NS))[:10],
                "authors": authors,
                "abstract": clean_text(entry.findtext("atom:summary", namespaces=ATOM_NS)),
                "arxiv_id": arxiv_id,
                "category": category,
                "doi": doi,
                "publication": f"arXiv ({category}:{arxiv_id})" if category else f"arXiv ({arxiv_id})",
                "journal_publication": clean_text(entry.findtext("arxiv:journal_ref", namespaces=ATOM_NS)),
            }
        )
    return records


def query_inspire(query: str, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "sort": "mostrecent", "size": str(max_results)})
    data = yaml.safe_load(fetch_text(f"{INSPIRE_API}?{params}"))
    records = []
    for hit in data.get("hits", {}).get("hits", []):
        metadata = hit.get("metadata", {})
        title_items = metadata.get("titles") or []
        title = clean_text(title_items[0].get("title") if title_items else "")
        if not title:
            continue
        authors = [clean_text(item.get("full_name")) for item in metadata.get("authors", [])]
        authors = [name for name in authors if name]
        arxiv_items = metadata.get("arxiv_eprints") or []
        arxiv_id = normalize_arxiv_id(arxiv_items[0].get("value") if arxiv_items else "")
        doi_items = metadata.get("dois") or []
        doi = clean_text(doi_items[0].get("value") if doi_items else "")
        publication = ""
        publication_info = metadata.get("publication_info") or []
        if publication_info:
            publication = format_publication_info(publication_info[0])
        abstracts = metadata.get("abstracts") or []
        abstract = clean_text(abstracts[0].get("value") if abstracts else "")
        categories = metadata.get("arxiv_eprints") or []
        category_values = categories[0].get("categories") if categories else []
        category = clean_text(category_values[0] if category_values else "")
        date = clean_text(metadata.get("preprint_date") or metadata.get("earliest_date") or "")
        records.append(
            {
                "source": "inspire",
                "title": title,
                "date": date,
                "authors": authors,
                "abstract": abstract,
                "arxiv_id": arxiv_id,
                "category": category,
                "doi": doi,
                "publication": f"arXiv ({category}:{arxiv_id})" if category and arxiv_id else "",
                "journal_publication": publication,
            }
        )
    return records


def format_publication_info(info: dict) -> str:
    journal = clean_text(info.get("journal_title"))
    volume = clean_text(str(info.get("journal_volume") or ""))
    year = clean_text(str(info.get("year") or ""))
    article = clean_text(str(info.get("artid") or info.get("page_start") or ""))
    parts = []
    if journal:
        parts.append(journal)
    if volume:
        parts.append(volume)
    if year:
        parts.append(f"({year})")
    if article:
        parts.append(article)
    return " ".join(parts)


def merge_records(records: list[dict]) -> list[dict]:
    merged: dict[str, dict] = {}
    for record in records:
        key = record.get("arxiv_id") or normalize_title(record["title"])
        if not key:
            continue
        current = merged.setdefault(key, {})
        for field, value in record.items():
            if not value:
                continue
            if field in {"journal_publication", "doi"}:
                if field not in current or current[field].startswith("10.48550/arXiv."):
                    current[field] = value
            elif field not in current or not current[field]:
                current[field] = value
    return list(merged.values())


def parse_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, front, body = text.split("---", 2)
    return yaml.safe_load(front) or {}, body.lstrip()


def write_front_matter(path: Path, front: dict, body: str) -> bool:
    front_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=90).strip()
    new_text = f"---\n{front_text}\n---\n\n{body.strip()}\n"
    old_text = path.read_text(encoding="utf-8") if path.exists() else ""
    if old_text == new_text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def load_entries(content_dir: Path) -> list[dict]:
    entries = []
    for path in sorted(content_dir.glob("*/index.md")):
        front, body = parse_front_matter(path)
        if not front.get("title"):
            continue
        entries.append({"path": path, "slug": path.parent.name, "front": front, "body": body})
    return entries


def index_entries(entries: list[dict]) -> tuple[dict, dict, dict]:
    by_arxiv = {}
    by_doi = {}
    by_title = {}
    for entry in entries:
        front = entry["front"]
        by_title[normalize_title(front.get("title", ""))] = entry
        doi = clean_text(str(front.get("doi") or ""))
        if doi:
            by_doi[doi.lower()] = entry
        for link in front.get("links") or []:
            arxiv_id = arxiv_id_from_url(link.get("url"))
            if arxiv_id:
                by_arxiv[arxiv_id] = entry
    return by_arxiv, by_doi, by_title


def find_existing(record: dict, indexes: tuple[dict, dict, dict]) -> dict | None:
    by_arxiv, by_doi, by_title = indexes
    arxiv_id = record.get("arxiv_id")
    doi = clean_text(record.get("doi", "")).lower()
    title = normalize_title(record.get("title", ""))
    return by_arxiv.get(arxiv_id) or by_doi.get(doi) or by_title.get(title)


def is_in_preparation(front: dict) -> bool:
    publication = clean_text(str(front.get("publication") or "")).lower()
    tags = [clean_text(str(tag)).lower() for tag in front.get("tags") or []]
    return publication in {"", "in preparation"} or "in preparation" in tags


def record_status(record: dict) -> str:
    return "Journal" if record.get("journal_publication") else "Preprint"


def update_links(front: dict, record: dict) -> None:
    links = list(front.get("links") or [])
    by_name = {clean_text(link.get("name")).lower(): link for link in links}

    def upsert(name: str, url: str) -> None:
        if not url:
            return
        key = name.lower()
        if key in by_name:
            by_name[key]["url"] = url
        else:
            link = {"name": name, "url": url}
            links.append(link)
            by_name[key] = link

    arxiv_id = record.get("arxiv_id", "")
    if arxiv_id:
        upsert("arXiv", f"https://arxiv.org/abs/{arxiv_id}")
        upsert("PDF", f"https://arxiv.org/pdf/{arxiv_id}.pdf")
    doi = record.get("doi", "")
    if doi:
        upsert("DOI", f"https://doi.org/{doi}")
    front["links"] = links


def apply_record(front: dict, body: str, record: dict, force_generated_body: bool = False) -> tuple[dict, str]:
    updated = dict(front)
    was_in_preparation = is_in_preparation(front)
    publication = record.get("journal_publication") or record.get("publication")

    if was_in_preparation:
        updated["title"] = record["title"]
        if record.get("date"):
            updated["date"] = record["date"]
        if record.get("authors"):
            updated["authors"] = record["authors"]
        tags = [tag for tag in updated.get("tags", []) if clean_text(str(tag)).lower() != "in preparation"]
        status_tag = "Journal" if record.get("journal_publication") else "Preprint"
        if status_tag not in tags:
            tags.insert(0, status_tag)
        updated["tags"] = tags
        if record.get("abstract"):
            updated["abstract"] = record["abstract"]
        if record.get("abstract") and not updated.get("summary"):
            updated["summary"] = summarize(record["abstract"])

    if publication and (was_in_preparation or record.get("journal_publication")):
        updated["publication"] = publication
    if record.get("doi"):
        current_doi = clean_text(str(updated.get("doi") or ""))
        if not current_doi or current_doi.startswith("10.48550/arXiv.") or record.get("journal_publication"):
            updated["doi"] = record["doi"]

    update_links(updated, record)

    if was_in_preparation or force_generated_body:
        body = generated_body(updated, record)
    return updated, body


def summarize(abstract: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", clean_text(abstract))
    return " ".join(sentences[:2])[:280].strip()


def generated_body(front: dict, record: dict) -> str:
    authors = "; ".join(front.get("authors") or record.get("authors") or [])
    venue = front.get("publication") or record.get("publication") or "Preprint"
    lines = [
        f"**Status:** {record_status(record)}",
        "",
        f"**Authors:** {authors}",
        "",
        f"**Venue:** {venue}",
        "",
    ]
    if record.get("arxiv_id"):
        arxiv_id = record["arxiv_id"]
        lines.append(f"- arXiv: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")
        lines.append("")
    lines.append(front.get("summary") or summarize(record.get("abstract", "")))
    return "\n".join(lines).strip()


def create_entry(content_dir: Path, record: dict) -> Path:
    slug = slugify(record["title"])
    path = content_dir / slug / "index.md"
    counter = 2
    while path.exists():
        path = content_dir / f"{slug}-{counter}" / "index.md"
        counter += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    tags = ["Journal" if record.get("journal_publication") else "Preprint"]
    front = {
        "title": record["title"],
        "date": record.get("date") or dt.date.today().isoformat(),
        "authors": record.get("authors") or [],
        "tags": tags,
        "summary": summarize(record.get("abstract", "")),
        "abstract": record.get("abstract", ""),
        "featured": False,
        "publication": record.get("journal_publication") or record.get("publication") or "Preprint",
    }
    if record.get("doi"):
        front["doi"] = record["doi"]
    update_links(front, record)
    write_front_matter(path, front, generated_body(front, record))
    return path


def refresh_indexes(content_dir: Path) -> bool:
    entries = load_entries(content_dir)
    dated = sorted(entries, key=lambda item: str(item["front"].get("date", "")), reverse=True)
    published = [entry for entry in dated if not is_in_preparation(entry["front"])]
    in_prep = [entry for entry in dated if is_in_preparation(entry["front"])]

    front = "---\ntitle: Publications\ndate: 2025-11-25\ntype: landing\n---\n\n"
    public_intro = (
        "This page tracks published papers and public preprints, with entries maintained from "
        "site content and automated arXiv/INSPIRE checks.\n\n"
    )
    full_intro = (
        "This page tracks published papers, public preprints, and selected in-preparation "
        "manuscripts, with public entries maintained from site content and automated "
        "arXiv/INSPIRE checks.\n\n"
    )
    published_block = "## Published / Archived\n\n" + numbered_lines(published) + "\n"
    full_block = published_block
    if in_prep:
        full_block += "\n## In preparation\n\n" + bullet_lines(in_prep) + "\n"

    changed = False
    pages = {
        "_index.md": public_intro + published_block,
        "_index_full.md": full_intro + full_block,
    }
    for name, body in pages.items():
        path = content_dir / name
        new_text = front + body
        old_text = path.read_text(encoding="utf-8") if path.exists() else ""
        if old_text != new_text:
            path.write_text(new_text, encoding="utf-8")
            changed = True
    return changed


def numbered_lines(entries: list[dict]) -> str:
    return "\n".join(f"{idx}. {entry_line(entry)}" for idx, entry in enumerate(entries, start=1))


def bullet_lines(entries: list[dict]) -> str:
    return "\n".join(f"- {entry_line(entry)}" for entry in entries)


def entry_line(entry: dict) -> str:
    front = entry["front"]
    title = front.get("title", "Untitled")
    publication = front.get("publication") or "In preparation"
    line = f"[{title}](/publications/{entry['slug']}/) - {publication}"
    arxiv_id = ""
    for link in front.get("links") or []:
        arxiv_id = arxiv_id_from_url(link.get("url"))
        if arxiv_id:
            break
    if arxiv_id:
        line += f" [arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})"
    return line


def main() -> int:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__ or ""),
    )
    parser.add_argument("--author", default="Vaishak Prasad")
    parser.add_argument("--inspire-query", default='a "Vaishak Prasad"')
    parser.add_argument("--content-dir", type=Path, default=Path("content/publications"))
    parser.add_argument("--max-results", type=int, default=75)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    entries = load_entries(args.content_dir)
    indexes = index_entries(entries)

    records = query_arxiv(args.author, args.max_results)
    time.sleep(3)  # Be polite to public APIs when this runs on a schedule.
    records.extend(query_inspire(args.inspire_query, args.max_results))
    records = merge_records(records)

    changed = False
    for record in records:
        existing = find_existing(record, indexes)
        if existing:
            front, body = apply_record(existing["front"], existing["body"], record)
            if args.dry_run:
                continue
            if write_front_matter(existing["path"], front, body):
                changed = True
        else:
            if args.dry_run:
                continue
            create_entry(args.content_dir, record)
            changed = True

    if not args.dry_run and refresh_indexes(args.content_dir):
        changed = True

    print("Publication update complete." if changed else "No publication changes found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
