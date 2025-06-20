import os
import markdown
import json

notes_dir = "notes"
output_dir = "output"
json_index_path = os.path.join(output_dir, "brain-index.json")

os.makedirs(output_dir, exist_ok=True)

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

            json_objects.append({
                "title": note_title,
                "path": relative_md_path,
                "markdown": md_content,
                "html": html_content
            })

            found_files += 1

if found_files:
    with open(json_index_path, 'w', encoding='utf-8') as f:
        json.dump(json_objects, f, indent=2, ensure_ascii=False)

    print(f"\n✅ JSON-only index generated with {found_files} notes.")
    print(f"- JSON Output: {json_index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
