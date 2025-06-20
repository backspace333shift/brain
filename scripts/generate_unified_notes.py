import os
import markdown
import json

notes_dir = "notes"
output_dir = "output"
output_html_path = os.path.join(output_dir, "notes.html")
sitemap_path = os.path.join(output_dir, "sitemap.xml")
txt_index_path = os.path.join(output_dir, "index.txt")
json_index_path = os.path.join(output_dir, "brain-index.json")

GITHUB_PAGES_BASE = "https://backspace333shift.github.io/brain"
SINGLE_PAGE_NAME = "notes.html"
RENDERED_URL = f"{GITHUB_PAGES_BASE}/{SINGLE_PAGE_NAME}"

os.makedirs(output_dir, exist_ok=True)

all_notes_html = [
    "<!DOCTYPE html>",
    "<html lang='en'>",
    "<head>",
    "  <meta charset='UTF-8'>",
    "  <meta name='robots' content='index, follow'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    "  <title>Unified Notes</title>",
    "  <style>body{font-family:sans-serif;max-width:800px;margin:auto;padding:2rem;} h1,h2{border-bottom:1px solid #ccc;} pre{background:#f0f0f0;padding:1em;}</style>",
    "</head><body>",
    "<h1>📚 Unified Notes</h1>"
]

json_objects = []
found_files = 0

for root, _, files in os.walk(notes_dir):
    for file in sorted(files):
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            relative_md_path = os.path.relpath(full_path, notes_dir)
            note_title = relative_md_path.replace(".md", "").replace("\\", "/")

            with open(full_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

            anchor_id = note_title.replace("/", "_").replace(" ", "_")
            all_notes_html.append(f"<hr><h2 id='{anchor_id}'>{note_title}</h2>")
            all_notes_html.append(html_content)

            json_objects.append({
                "title": note_title,
                "anchor": anchor_id,
                "path": relative_md_path
            })

            found_files += 1

all_notes_html.append("</body></html>")

if found_files:
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_notes_html))

    # Write sitemap pointing to the single page
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <url><loc>{RENDERED_URL}</loc></url>",
        "</urlset>"
    ]
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_lines))

    # Write plaintext index file
    with open(txt_index_path, 'w', encoding='utf-8') as f:
        f.write(RENDERED_URL)

    # Write JSON index
    with open(json_index_path, 'w', encoding='utf-8') as f:
        json.dump(json_objects, f, indent=2)

    print(f"\n✅ Success. Compiled {found_files} Markdown files into:")
    print(f"- Unified HTML: {output_html_path}")
    print(f"- Sitemap: {sitemap_path}")
    print(f"- Text Index: {txt_index_path}")
    print(f"- JSON Index: {json_index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
