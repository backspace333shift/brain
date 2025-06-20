import os
import re
import yaml

notes_dir = "notes"
output_dir = "output"
md_index_path = os.path.join(output_dir, "brain-index.md")
html_index_path = os.path.join(output_dir, "index.html")

os.makedirs(output_dir, exist_ok=True)

toc_entries = []
md_sections = []
found_files = 0


def slugify(text):
    return re.sub(r'[^a-z0-9\-]', '', re.sub(r'\s+', '-', text.lower()))


def extract_yaml_frontmatter(text):
    if text.startswith('---'):
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
        if match:
            frontmatter = yaml.safe_load(match.group(1))
            content = match.group(2)
            return frontmatter, content.strip()
    return None, text.strip()


def extract_headings(content, note_slug):
    headings = []
    for line in content.splitlines():
        if line.startswith("#"):
            level = len(re.match(r'^#+', line).group())
            title = line.lstrip("#").strip()
            slug = slugify(f"{note_slug}-{title}")
            headings.append((level, title, f"#{slug}"))
    return headings


for root, _, files in os.walk(notes_dir):
    for file in sorted(files):
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            relative_md_path = os.path.relpath(full_path, notes_dir)
            note_slug = relative_md_path.replace(".md", "").replace("\\", "/")

            with open(full_path, 'r', encoding='utf-8') as f:
                raw = f.read()

            metadata, body = extract_yaml_frontmatter(raw)
            headings = extract_headings(body, note_slug)

            # Add to ToC
            for level, title, anchor in headings:
                indent = "  " * (level - 1)
                toc_entries.append(f"{indent}- [{title}]({anchor})")

            # Build section
            header_anchor = f"<!-- anchor: {slugify(note_slug)} -->"
            metadata_block = f"<!-- meta: {metadata} -->" if metadata else ""
            path_comment = f"<!-- path: {relative_md_path} -->"

            section = f"""{header_anchor}
# {note_slug}
{metadata_block}
{path_comment}

{body}

"""
            md_sections.append(section)
            found_files += 1

# Final build
if found_files:
    full_md = f"# 🧠 Brain Index\n\n## Table of Contents\n\n" + "\n".join(toc_entries) + "\n\n---\n\n" + "\n".join(md_sections)

    # Write Markdown output
    with open(md_index_path, 'w', encoding='utf-8') as f:
        f.write(full_md)

    # Optional HTML plaintext wrapper
    with open(html_index_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Brain Notes (Markdown Index)</title>
</head>
<body>
<pre>
{full_md}
</pre>
</body>
</html>""")

    print(f"\n✅ Generated unified Markdown index with {found_files} notes.")
    print(f"- Markdown output: {md_index_path}")
    print(f"- HTML plaintext view: {html_index_path}")
else:
    print("[WARNING] No Markdown (.md) files found in the notes directory.")
