import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find each occurrence of 'destination-card' and print its surrounding text or which section it falls into.
# Sections are:
# tab1: from html.find('id="tab1"') to html.find('id="tab2"')
# tab2: from html.find('id="tab2"') to html.find('id="tab3"')
# tab3: from html.find('id="tab3"') to html.find('id="tab4"')
# tab4: from html.find('id="tab4"') to html.find('</main>')

tab1_idx = html.find('id="tab1"')
tab2_idx = html.find('id="tab2"')
tab3_idx = html.find('id="tab3"')
tab4_idx = html.find('id="tab4"')
main_end_idx = html.find('</main>')

indices = [
    ('tab1', tab1_idx),
    ('tab2', tab2_idx),
    ('tab3', tab3_idx),
    ('tab4', tab4_idx),
    ('end', main_end_idx)
]
indices.sort(key=lambda x: x[1])

import re
matches = [m.start() for m in re.finditer('destination-card', html)]

for m in matches:
    # Find which section it's in
    sect_name = 'unknown'
    for i in range(len(indices) - 1):
        if indices[i][1] <= m < indices[i+1][1]:
            sect_name = indices[i][0]
            break
    print(f"Match at index {m} is in section: {sect_name}")
