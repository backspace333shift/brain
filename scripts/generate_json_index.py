import os
import markdown
import json

notes_dir = "notes"
output_dir = "output"
html_index_path = os.path.join(output_dir, "index.html")
txt_index_path = os.path.join(output_dir, "brain-index.txt")

os.makedirs(output_dir, exist_ok=True)

json_objects = []
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
                html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

            # JSON object
            json_objects.append({
                "title": note_title,
                "path": relative_md_path,
                "markdown": md_content,
                "html": html_content
            })

            # TXT section
            txt_sections.append(f"""---\n# {note_title}\nPath: {relative_md_path}\n\n{md_content.strip()}\n""")

            found_files += 1

if found_files:
    # Write TXT index
    with open(txt_index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(txt_sections))

    # Write HTML with embedded JSON
    json_data_inline = json.dumps(json_objects, indent=2, ensure_ascii=False)

    with open(html_index_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Brain Index</title>
  <style>
    body {{
      font-family: system-ui, sans-serif;
      padding: 2em;
    }}
    pre {{
      background: #f0f0f0;
      padding: 1em;
      border-radius: 8px;
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <h1>🧠 Brain Index</h1>
  <p>This is an embedded JSON view of all Markdown notes.</p>
  <pre id="viewer">Loading...</pre>

  <script id="brain-data" type="application/json">
{json_data_inline}
  </script>

  <script>
    const raw = document.getElementById('brain-data').textContent;
    const data = JSON.parse(raw);
    document.getElementById('viewer').textContent = JSON.stringify(data, null, 2);
  </script>
</body>
</html>""")

    print(f"\n✅ HTML + TXT index generated with {found_files} notes.")
    print(f"- HTML Output: {html_index_path}")
    print(f"- TXT Output: {txt_index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
