from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def validate_required_files(errors: list[str]) -> None:
    required = [
        "README.md",
        "QUICKSTART.md",
        "OVERVIEW.md",
        "index.html",
        "portal.css",
        "docs/PLAN_TEMPLATE.md",
        "docs/EXECUTIVE_SUMMARY_TEMPLATE.md",
        "docs/RESOURCE_MATRIX_TEMPLATE.md",
        "docs/ONBOARDING_CHECKLIST.md",
        "projects/INDEX.md",
        "infra/README.md",
        "assets/csa-roadmap-template-banner.svg",
        "assets/csa-roadmap-template-social-preview.svg",
    ]
    for relative_path in required:
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing required file: {relative_path}")


def validate_weeks(errors: list[str]) -> None:
    for week in range(1, 11):
        week_dir = ROOT / f"week-{week:02d}"
        if not week_dir.exists():
            errors.append(f"Missing week folder: {week_dir.name}")
            continue
        for file_name in ("STATUS.md", "WEEK_ASSIGNMENT.md"):
            file_path = week_dir / file_name
            if not file_path.exists():
                errors.append(f"Missing week file: {week_dir.name}/{file_name}")


def validate_markdown_headings(errors: list[str]) -> None:
    for markdown_file in ROOT.rglob("*.md"):
        lines = [line.strip() for line in markdown_file.read_text(encoding="utf-8").splitlines()]
        content_lines = lines
        if content_lines and content_lines[0] == "---":
            try:
                frontmatter_end = content_lines.index("---", 1)
                content_lines = content_lines[frontmatter_end + 1 :]
            except ValueError:
                pass
        first_content = next((line for line in content_lines if line), "")
        if not first_content.startswith("#"):
            errors.append(f"Markdown file missing top heading: {markdown_file.relative_to(ROOT)}")


def validate_index_links(errors: list[str]) -> None:
    index_path = ROOT / "index.html"
    parser = LinkCollector()
    parser.feed(index_path.read_text(encoding="utf-8"))
    for link in parser.links:
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (index_path.parent / link).resolve()
        if not target.exists():
            errors.append(f"Broken local link in index.html: {link}")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    validate_weeks(errors)
    validate_markdown_headings(errors)
    validate_index_links(errors)

    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())