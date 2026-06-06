from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "summition"


BASE_CSS = """
body {
  font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", Arial, sans-serif;
  color: #1f2933;
  margin: 36px 44px;
  line-height: 1.6;
  font-size: 13.5px;
}
h1, h2, h3 {
  color: #102a43;
  margin-top: 1.2em;
  margin-bottom: 0.45em;
}
h1 { font-size: 24px; border-bottom: 2px solid #d9e2ec; padding-bottom: 8px; }
h2 { font-size: 19px; }
h3 { font-size: 16px; }
p { margin: 0.45em 0; }
ul, ol { margin: 0.35em 0 0.7em 1.4em; }
li { margin: 0.2em 0; }
hr { border: 0; border-top: 1px solid #bcccdc; margin: 1.4em 0; }
code {
  background: #f0f4f8;
  border-radius: 4px;
  padding: 1px 4px;
  font-family: Consolas, monospace;
}
.page-break { page-break-before: always; }
"""


def apply_inline(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def markdown_to_html(markdown_text: str, title: str) -> str:
    lines = markdown_text.splitlines()
    parts: list[str] = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'>",
        f"<title>{html.escape(title)}</title>",
        f"<style>{BASE_CSS}</style>",
        "</head><body>",
    ]

    paragraph: list[str] = []
    in_ul = False
    in_ol = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(x.strip() for x in paragraph).strip()
            if joined:
                parts.append(f"<p>{apply_inline(joined)}</p>")
            paragraph = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            parts.append("</ul>")
            in_ul = False
        if in_ol:
            parts.append("</ol>")
            in_ol = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        if stripped == "---":
            flush_paragraph()
            close_lists()
            parts.append("<hr>")
            continue

        heading_match = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            close_lists()
            level = len(heading_match.group(1))
            text = apply_inline(heading_match.group(2))
            parts.append(f"<h{level}>{text}</h{level}>")
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            if not in_ol:
                parts.append("<ol>")
                in_ol = True
            parts.append(f"<li>{apply_inline(ordered_match.group(1))}</li>")
            continue

        unordered_match = re.match(r"^-\s+(.*)$", stripped)
        if unordered_match:
            flush_paragraph()
            if in_ol:
                parts.append("</ol>")
                in_ol = False
            if not in_ul:
                parts.append("<ul>")
                in_ul = True
            parts.append(f"<li>{apply_inline(unordered_match.group(1))}</li>")
            continue

        close_lists()
        paragraph.append(stripped)

    flush_paragraph()
    close_lists()
    parts.append("</body></html>")
    return "\n".join(parts)


def write_html(markdown_path: Path, html_path: Path, title: str) -> None:
    content = markdown_path.read_text(encoding="utf-8")
    html_doc = markdown_to_html(content, title)
    html_path.write_text(html_doc, encoding="utf-8")


def write_svg_wrapper(svg_name: str, html_path: Path, title: str) -> None:
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 0;
      background: #ffffff;
      font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", Arial, sans-serif;
    }}
    .wrap {{
      width: 100%;
      padding: 16px;
      box-sizing: border-box;
    }}
    img {{
      width: 100%;
      height: auto;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <img src="{html.escape(svg_name)}" alt="{html.escape(title)}">
  </div>
</body>
</html>
"""
    html_path.write_text(html_doc, encoding="utf-8")


def main() -> None:
    write_html(
        SUBMISSION / "part1_part3_preview.md",
        SUBMISSION / "part1_part3_preview.html",
        "AI Harness 作業預覽",
    )
    write_svg_wrapper(
        "02_infographic.svg",
        SUBMISSION / "02_infographic.html",
        "Code Operations Agent Infographic",
    )


if __name__ == "__main__":
    main()
