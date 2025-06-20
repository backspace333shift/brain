import os
import markdown

notes_dir = "notes"
output_dir = "output"
txt_index_path = os.path.join(output_dir, "brain-index.txt")
html_index_path = os.path.join(output_dir, "index.html")  # Will be plaintext inside <pre>

os.makedirs(output_dir, exist_ok=True)

txt_sections = []
found_files = 0

for root, _, files in os.walk(notes_dir):
    for file in sorted(files):
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            relative_md_path = os.path.relpath(full_path, notes_dir)
            note_title = relative_md_path.replace(".md", "").replace("\\", "/")

            with open(full_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            txt_sections.append(f"""---\n# {note_title}\nPath: {relative_md_path}\n\n{md_content.strip()}\n""")
            found_files += 1

if found_files:
    full_txt = "\n".join(txt_sections)

    # Write TXT version
    with open(txt_index_path, 'w', encoding='utf-8') as f:
        f.write(full_txt)

    # Write plaintext-wrapped HTML version for GitHub Pages
    with open(html_index_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Brain Notes (Plaintext)</title>
</head>
<body>
<pre>
{full_txt}
</pre>
</body>
</html>""")

    print(f"\n✅ TXT-based index generated with {found_files} notes.")
    print(f"- TXT Output: {txt_index_path}")
    print(f"- HTML Output (plaintext container): {html_index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
