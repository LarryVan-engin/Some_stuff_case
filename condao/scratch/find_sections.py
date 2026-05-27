import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for all id=... tags to see the layout of the page
ids = re.findall(r'id="([^"]+)"', html)
print("All IDs in index.html:")
print(ids)

# Let's search for the start and end of section elements (tabs)
sections = re.findall(r'<section id="([^"]+)"[^>]*>', html)
print("\nAll sections in index.html:")
for sec in sections:
    match = re.search(r'<section id="' + sec + r'"[^>]*>', html)
    print(f"Section {sec} starts at char {match.start()}")
