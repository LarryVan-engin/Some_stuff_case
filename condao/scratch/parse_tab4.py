import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tab4_match = re.search(r'<section id="tab4".*?</section>', html, re.DOTALL)
if not tab4_match:
    print("No tab4 section found!")
    sys.exit(1)
    
tab4_html = tab4_match.group(0)

# Let's search for h3 or h4 tags or something that looks like titles
headings = re.findall(r'<h[2-5][^>]*>(.*?)</h[2-5]>', tab4_html)
print(f"All headings in tab4: {len(headings)}")
for h in headings:
    print(h)
