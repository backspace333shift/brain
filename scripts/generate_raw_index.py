import os
import markdown
import urllib.parse

notes_dir = "notes"
output_dir = "output"

print(f"\n[INFO] Scanning directory: {os.path.abspath(notes_dir)}")

if not os.path.exists(notes_dir):
    print("[ERROR] 'notes/' directory does not exist.")
    exit(1)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"[INFO] Created output directory: {output_dir}")

# Base URLs
GITHUB_PAGES_BASE = "https://backspace333shift.github.io/brain"
RAW_BASE = "https://raw.githubusercontent.com/backspace333shift/brain/main/output"

index_lines = ["<html><body><h1>Notes Index</h1><ul>"]
found_files = []

for root, _, files in os.walk(notes_dir):
    for file in files:
        if file.endswith(".md"):
            md_full_path = os.path.join(root, file)
            rel_md_path = os.path.relpath(md_full_path, notes_dir)

            # Sanitize file name
            rel_html_path = rel_md_path.replace(" ", "_").replace(".md", ".html")
            output_path = os.path.join(output_dir, rel_html_path)

            print(f"[PROCESSING] {rel_md_path} → {rel_html_path}")

            # Read markdown content
            with open(md_full_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Convert to HTML
            html = markdown.markdown(text)

            # Ensure output subdirectory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            # Encode for URL
            url_safe_path = urllib.parse.quote(rel_html_path.replace(os.sep, "/"))

            # Construct URLs
            rendered_url = f"{GITHUB_PAGES_BASE}/{url_safe_path}"
            raw_url = f"{RAW_BASE}/{url_safe_path}"
            display_name = rel_md_path.replace(".md", "").replace(" ", "_")

            # Add to index
            index_lines.append(
                f'<li><a href="{rendered_url}">{display_name}</a> [<a href="{raw_url}">raw</a>]</li>'
            )

            found_files.append(rel_md_path)

index_lines.append("</ul></body></html>")

if found_files:
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
    print(f"\n✅ Done. Converted {len(found_files)} notes to HTML.")
    print(f"[INFO] Index file written to: {index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
