import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tab3_match = re.search(r'<section id="tab3".*?</section>', html, re.DOTALL)
if not tab3_match:
    print("No tab3 section found!")
    sys.exit(1)
    
tab3_html = tab3_match.group(0)

# Let's search for h3 or h4 tags or something that looks like titles
# In tab3 there are hotels like Six Senses, Poulo Condor, etc.
titles = re.findall(r'<h3 class="[^"]+">(.*?)</h3>', tab3_html)
print(f"Titles found in tab3: {len(titles)}")
for t in titles:
    print(t)
    
# Let's search for other headings
headings = re.findall(r'<h[2-5][^>]*>(.*?)</h[2-5]>', tab3_html)
print(f"\nAll headings in tab3: {len(headings)}")
for h in headings:
    print(h)
