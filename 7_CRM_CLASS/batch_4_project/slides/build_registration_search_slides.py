"""Build the Registration search lesson HTML from the reviewed Markdown draft.

Run from anywhere with: python slides/build_registration_search_slides.py
The HTML is also suitable for Chrome's Print to PDF.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "REGISTRATION_SEARCH_IMPLEMENTATION_DRAFT.md"
OUTPUT = HERE / "registration-search-implementation.html"


def inline_plain(text: str) -> str:
    chunks = re.split(r"(`[^`]+`|\[[^]]+\]\([^)]+\))", text)
    rendered = []
    for chunk in chunks:
        if chunk.startswith("`") and chunk.endswith("`"):
            rendered.append(f"<code>{html.escape(chunk[1:-1])}</code>")
        elif chunk.startswith("[") and "](" in chunk and chunk.endswith(")"):
            label, url = chunk[1:-1].split("](", 1)
            rendered.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>')
        else:
            safe = html.escape(chunk)
            rendered.append(safe)
    return "".join(rendered)


def inline(text: str) -> str:
    parts = re.split(r"(\*\*.+?\*\*)", text)
    return "".join(
        f"<strong>{inline_plain(part[2:-2])}</strong>"
        if part.startswith("**") and part.endswith("**")
        else inline_plain(part)
        for part in parts
    )


def markdown_body(lines: list[str]) -> str:
    out = []
    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        if not line or line == "---":
            index += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            code = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            out.append(f'<pre class="code {html.escape(language)}"><code>{html.escape(chr(10).join(code))}</code></pre>')
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]
            table = ["<table>"]
            for row_index, row in enumerate(rows):
                cell_tag = "th" if row_index == 0 else "td"
                table.append("<tr>" + "".join(f"<{cell_tag}>{inline(cell)}</{cell_tag}>" for cell in row) + "</tr>")
            table.append("</table>")
            out.append("".join(table))
            continue
        if re.match(r"\d+\. ", line):
            items = []
            while index < len(lines) and re.match(r"\d+\. ", lines[index]):
                items.append(f"<li>{inline(re.sub(r'^\d+\. ', '', lines[index]))}</li>")
                index += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append(f"<li>{inline(lines[index][2:])}</li>")
                index += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            index += 1
            continue
        if line.startswith("**Teacher explanation:**"):
            out.append(f'<div class="teacher"><span>Teacher explanation</span><p>{inline(line.removeprefix("**Teacher explanation:**").strip())}</p></div>')
            index += 1
            continue
        out.append(f"<p>{inline(line)}</p>")
        index += 1
    return "\n".join(out)


def slide(title: str, subtitle: str, content: str, number: int, kind: str = "lesson") -> str:
    return f'''<section class="slide {kind}">
  <div class="edge"></div>
  <header><div class="eyebrow">CRM · SEARCH API IMPLEMENTATION</div><h2>{html.escape(title)}</h2><div class="subtitle">{html.escape(subtitle)}</div></header>
  <div class="slide-content">{content}</div>
  <footer><span>Django REST Framework · Registration API</span><span>{number:02d}</span></footer>
</section>'''


def build() -> None:
    source = SOURCE.read_text()
    matches = list(re.finditer(r"(?m)^## Slide (\d+) — (.+)$", source))
    if len(matches) != 25:
        raise ValueError(f"Expected 25 lesson slides, found {len(matches)}")

    pages = ['''<section class="slide cover">
  <div class="edge"></div>
  <div class="slide-content">
    <div class="cover-kicker">FROM THEORY TO CODE · DJANGO REST FRAMEWORK</div>
    <h1>Registration<br>Search API</h1>
    <p class="cover-lead">A teacher-led walkthrough of the CRM code and a live Postman demonstration.</p>
    <div class="cover-topics">Name and email search <b>·</b> DOB filters <b>·</b> Ordering <b>·</b> Pagination <b>·</b> JWT</div>
  </div>
  <footer><span>Django REST Framework · Registration API</span><span>01</span></footer>
</section>''']
    for position, match in enumerate(matches):
        end = matches[position + 1].start() if position + 1 < len(matches) else source.index("## Teacher appendix A")
        body = source[match.end():end].splitlines()
        pages.append(slide(match.group(2), f"Lesson step {match.group(1)} of 25", markdown_body(body), len(pages) + 1))

    appendix = source[source.index("## Teacher appendix A"):]
    serializer_start = appendix.index("**`crm/registration/serializers.py`:**")
    view_start = appendix.index("**Registration ViewSet and pagination")
    cheat_start = appendix.index("## Teacher appendix B")
    appendix_intro = appendix[serializer_start:view_start].splitlines()
    pages.append(slide("Code reference: serializer and imports", "Teacher reference", markdown_body(appendix_intro), len(pages) + 1, "reference"))

    view_fragment = appendix[view_start:cheat_start]
    code_match = re.search(r"```python\n(.*?)\n```", view_fragment, re.S)
    if not code_match:
        raise ValueError("Cannot find ViewSet code in appendix")
    code = code_match.group(1).splitlines()
    split_at = next(i for i, line in enumerate(code) if line.strip() == "def get_queryset(self):")
    for title, portion in [
        ("Code reference: ViewSet setup", code[:split_at]),
        ("Code reference: exact email and DOB filters", code[split_at:]),
    ]:
        pages.append(slide(title, "Teacher reference · matches the project", markdown_body(["```python", *portion, "```"]), len(pages) + 1, "reference"))

    cheat = appendix[cheat_start:appendix.index("## Teacher references")]
    rows = [line for line in cheat.splitlines() if line.startswith("|")]
    headers = rows[:2]
    data = rows[2:]
    for title, part in [
        ("Postman request cheat sheet · 1", data[:4]),
        ("Postman request cheat sheet · 2", data[4:]),
    ]:
        prefix = ["Every Registration GET uses Bearer Token `{{access_token}}`. Send login first."]
        pages.append(slide(title, "Teacher reference · exact request URLs", markdown_body(prefix + headers + part), len(pages) + 1, "reference"))

    reference_lines = appendix[appendix.index("## Teacher references"):].splitlines()[1:]
    reference_lines = [line for line in reference_lines if not line.startswith("**This Markdown is the editable")]
    pages.append(slide("Sources and course note", "Teacher reference", markdown_body(reference_lines), len(pages) + 1, "reference"))

    css = r'''
@page { size: 13.333in 7.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: #d9e3e6; color: #1c2f37; font-family: "Liberation Sans", Arial, sans-serif; }
.slide { position: relative; width: 13.333in; height: 7.5in; padding: .43in .63in .43in .72in; overflow: hidden; page-break-after: always; background: #f8faf8; }
.slide:last-child { page-break-after: auto; }
.cover { background: #172f39; color: #f5f8f5; }
.cover .edge { background: #e56b45; }
.cover .slide-content { margin: 1.22in .30in 0 .18in; max-height: 5in; }
.cover-kicker { font-size: 18px; letter-spacing: .12em; color: #68ced0; font-weight: bold; }
.cover h1 { font-size: 72px; line-height: 1.07; margin: .24in 0; }
.cover-lead { font-size: 27px; max-width: 9.6in; line-height: 1.35; }
.cover-topics { margin-top: .42in; font-size: 18px; color: #d7e6e5; }
.cover-topics b { color: #ee7a55; padding: 0 .10in; }
.cover footer { border-top-color: #56727a; color: #b7cecf; }
.edge { position: absolute; left: 0; top: 0; height: 100%; width: .16in; background: #e56b45; }
header { border-bottom: 2px solid #c9d7d9; padding-bottom: .13in; margin-bottom: .17in; }
.eyebrow { color: #087c82; font-size: 14px; font-weight: bold; letter-spacing: .12em; }
h2 { margin: .05in 0 .04in; font-size: 36px; line-height: 1.08; color: #172f39; }
.subtitle { color: #687d82; font-size: 16px; }
.slide-content { max-height: 5.62in; overflow: hidden; font-size: 19px; line-height: 1.31; }
.slide-content p { margin: .10in 0; overflow-wrap: anywhere; }
.slide-content strong { color: #0b696e; }
.slide-content p:first-child { margin-top: .04in; }
.slide-content p:has(strong:first-child) { color: #263d45; }
.teacher { background: #eaf2f1; border-left: 6px solid #0c7c80; padding: .12in .18in; margin: .18in 0 .08in; }
.teacher span { display: block; font-size: 14px; font-weight: bold; letter-spacing: .08em; text-transform: uppercase; color: #0a6c72; }
.teacher p { margin: .06in 0 0; }
code, pre { font-family: "DejaVu Sans Mono", monospace; }
p code, td code { font-size: .84em; background: #e7eceb; padding: 1px 4px; border-radius: 3px; overflow-wrap: anywhere; }
.code { background: #172b34; color: #f0f7f4; font-size: 16px; line-height: 1.31; padding: .14in .2in; border-radius: 7px; white-space: pre-wrap; overflow-wrap: anywhere; margin: .12in 0; }
.code code { font-size: inherit; }
table { border-collapse: collapse; width: 100%; margin: .10in 0 .14in; background: white; }
td, th { text-align: left; border: 1px solid #c9d8d7; padding: .09in .11in; font-size: 17px; line-height: 1.22; vertical-align: top; overflow-wrap: anywhere; }
th { background: #137b80; color: white; }
td code { font-size: .79em; }
ol, ul { padding-left: .34in; margin: .10in 0; }
li { margin: .08in 0; }
footer { position: absolute; bottom: .20in; left: .72in; right: .61in; display: flex; justify-content: space-between; border-top: 1px solid #c9d7d9; padding-top: .08in; color: #718389; font-size: 12px; }
.reference .slide-content { font-size: 17px; }
.reference .code { font-size: 14px; }
.reference table td, .reference table th { font-size: 15px; }
.reference a { color: #0a777b; }
.dense-1 .slide-content { font-size: 17px; line-height: 1.24; }
.dense-1 .code { font-size: 14px; line-height: 1.2; padding: .11in .16in; }
.dense-1 td, .dense-1 th { font-size: 15px; padding: .07in .09in; }
.dense-1 .teacher { margin-top: .10in; padding: .08in .13in; }
.dense-2 .slide-content { font-size: 15px; line-height: 1.17; }
.dense-2 .code { font-size: 12px; line-height: 1.15; padding: .08in .12in; }
.dense-2 td, .dense-2 th { font-size: 13px; padding: .05in .07in; }
.dense-2 .teacher { margin-top: .07in; padding: .06in .10in; }
.dense-2 .slide-content p { margin: .06in 0; }
.dense-3 .slide-content { font-size: 13px; line-height: 1.12; }
.dense-3 .code { font-size: 11px; line-height: 1.11; padding: .06in .09in; }
.dense-3 td, .dense-3 th { font-size: 12px; padding: .04in .06in; }
.dense-3 .teacher { margin-top: .05in; padding: .05in .08in; }
.dense-3 .slide-content p { margin: .04in 0; }
@media screen { .slide { margin: 24px auto; box-shadow: 0 8px 25px #18303c31; } }
@media print { body { background: transparent; } }
'''
    js = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slide').forEach(slide => {
    const content = slide.querySelector('.slide-content');
    for (const level of ['dense-1', 'dense-2', 'dense-3']) {
      if (content.scrollHeight <= content.clientHeight + 1) break;
      slide.classList.add(level);
    }
    if (content.scrollHeight > content.clientHeight + 1) slide.dataset.overflow = 'true';
  });
});
</script>'''
    document = "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Registration Search API · Implementation</title><style>" + css + "</style></head><body>" + "\n".join(pages) + js + "</body></html>"
    OUTPUT.write_text(document)
    print(f"Wrote {OUTPUT} ({len(pages)} slides)")


if __name__ == "__main__":
    build()
