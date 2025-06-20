import os
import markdown
from urllib.parse import quote

notes_dir = "notes"
output_dir = "output"
sitemap_path = os.path.join(output_dir, "sitemap.xml")

print(f"\n[INFO] Scanning directory: {os.path.abspath(notes_dir)}")

if not os.path.exists(notes_dir):
    print("[ERROR] 'notes/' directory does not exist.")
    exit(1)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"[INFO] Created output directory: {output_dir}")

# Base URLs
GITHUB_PAGES_BASE = "https://backspace333shift.github.io/brain/output"
RAW_BASE = "https://raw.githubusercontent.com/backspace333shift/brain/main/output"

index_lines = ["<html><body><h1>Notes Index</h1><ul>"]
sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
found_files = []

# Recursively walk through markdown files
for root, _, files in os.walk(notes_dir):
    for file in files:
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            relative_md_path = os.path.relpath(full_path, notes_dir)
            relative_html_path = relative_md_path.replace(".md", ".html")
            output_path = os.path.join(output_dir, relative_html_path)

            print(f"[PROCESSING] {relative_md_path}")
            with open(full_path, 'r', encoding='utf-8') as f:
                text = f.read()

            html = markdown.markdown(text)

            title = relative_md_path.replace(".md", "")
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="index, follow">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body>
{html}
</body>
</html>"""

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_html)

            encoded_path = quote(relative_html_path.replace(os.sep, "/"))
            rendered_url = f"{GITHUB_PAGES_BASE}/{encoded_path}"
            raw_url = f"{RAW_BASE}/{encoded_path}"
            display_name = title

            index_lines.append(f'<li><a href="{rendered_url}">{display_name}</a> [<a href="{raw_url}">raw</a>]</li>')
            sitemap_lines.append(f"<url><loc>{rendered_url}</loc></url>")
            found_files.append(relative_md_path)

# Finalize outputs
if found_files:
    index_lines.append("</ul></body></html>")
    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))

    sitemap_lines.append("</urlset>")
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_lines))

    print(f"\n✅ Done. Generated HTML and sitemap for {len(found_files)} notes.")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
