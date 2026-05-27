import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's check for duplicate IDs
id_pattern = re.compile(r'id=["\']([^"\']+)["\']')
ids = id_pattern.findall(html)
seen_ids = set()
duplicates = set()
for ident in ids:
    if ident in seen_ids:
        duplicates.add(ident)
    seen_ids.add(ident)

print("Duplicate IDs in HTML:", duplicates)

# Let's get the tab3 content and check if it contains any 'destination-card' or 'destinations-container'
tab3_start = html.find('id="tab3"')
tab4_start = html.find('id="tab4"')
tab3_content = html[tab3_start:tab4_start]

print("\nDoes tab3 contain 'destination-card'?")
print('destination-card' in tab3_content)

print("\nDoes tab3 contain 'destinations-container'?")
print('destinations-container' in tab3_content)

print("\nDoes tab3 contain 'gợi ý lưu trú' or similar?")
print('lưu trú' in tab3_content.lower() or 'six senses' in tab3_content.lower())
