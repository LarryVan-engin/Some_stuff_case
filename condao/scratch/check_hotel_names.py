import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('pristine_tab3_segment.html', 'r', encoding='utf-8') as f:
    pristine = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

t3_start = html.find('id="tab3"')
t4_start = html.find('id="tab4"')
curr_tab3 = html[t3_start:t4_start]

def extract_headings(text):
    # Find h4 tags
    return re.findall(r'<h4[^>]*>(.*?)</h4>', text)

print("Headings in pristine tab3:")
for h in extract_headings(pristine):
    print(" -", h.strip())

print("\nHeadings in current tab3:")
for h in extract_headings(curr_tab3):
    print(" -", h.strip())
