import os
import markdown

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
GITHUB_PAGES_BASE = "https://backspace333shift.github.io/brain/output"
RAW_BASE = "https://raw.githubusercontent.com/backspace333shift/brain/main/output"

index_lines = ["<html><body><h1>Notes Index</h1><ul>"]

found_files = []

# Recursively walk through all markdown files
for root, _, files in os.walk(notes_dir):
    for file in files:
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            relative_md_path = os.path.relpath(full_path, notes_dir)
            relative_html_path = relative_md_path.replace(".md", ".html")
            output_path = os.path.join(output_dir, relative_html_path)

            print(f"[PROCESSING] {relative_md_path}")

            # Read markdown content
            with open(full_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Convert to HTML
            html = markdown.markdown(text)

            # Ensure output subdir exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            # Encode for URL
            ENCODED_PATH = relative_html_path.replace(os.sep, "%20")

            # Construct URLs
            rendered_url = f"{GITHUB_PAGES_BASE}/{ENCODED_PATH}"
            raw_url = f"{RAW_BASE}/{ENCODED_PATH}"
            display_name = relative_md_path.replace(".md", "")

            # Add both links to index
            index_lines.append(
                f'<li><a href="{rendered_url}">{display_name}</a> [<a href="{raw_url}">raw</a>]</li>'
            )

            found_files.append(relative_md_path)

if found_files:
    index_lines.append("</ul></body></html>")
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
    print(f"\n✅ Done. Generated HTML for {len(found_files)} notes.")
    print(f"[INFO] Index file written to: {index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
