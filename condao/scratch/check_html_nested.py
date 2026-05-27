import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's clean the HTML to focus on tags only
# We can find all HTML tags: <div ...> or </div> or <section ...> or </section>
tag_pattern = re.compile(r'<(div|/div|section|/section)(?:\s+[^>]*)?>', re.IGNORECASE)
tags = []
for match in tag_pattern.finditer(html):
    tag_name = match.group(1).lower()
    pos = match.start()
    # Find line number
    line_no = html[:pos].count('\n') + 1
    tags.append((tag_name, line_no, pos))

stack = []
mismatches = []

for tag_name, line_no, pos in tags:
    if tag_name.startswith('/'):
        # Closing tag
        opening_name = tag_name[1:]
        if not stack:
            print(f"Error: Closing tag {tag_name} on line {line_no} has no opening tag.")
            mismatches.append((tag_name, line_no))
        else:
            top_tag, top_line, top_pos = stack.pop()
            if top_tag != opening_name:
                print(f"Error: Mismatched tag. Closing {tag_name} on line {line_no} matches {top_tag} on line {top_line}.")
                mismatches.append((tag_name, line_no))
    else:
        # Opening tag
        stack.append((tag_name, line_no, pos))

if stack:
    print("\nUnclosed tags remaining on stack:")
    for tag_name, line_no, pos in stack:
        print(f" - {tag_name} opened on line {line_no}")
else:
    print("\nNo unclosed tags!")

print(f"\nTotal tags analyzed: {len(tags)}")
