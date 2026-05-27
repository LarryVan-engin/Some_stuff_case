import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all blocks matching:
# <div class="destination-card ...> ... </div>
# We can find all occurrences of class="destination-card"
# and grab until the next matching close div (since they have a specific structure)

# A more robust regex is to parse destinations in tab1
tab1_match = re.search(r'<section id="tab1".*?</section>', html, re.DOTALL)
if not tab1_match:
    print("No tab1 section found!")
    sys.exit(1)
    
tab1_html = tab1_match.group(0)

# Let's find all cards
cards = re.findall(r'<div class="destination-card\s+[^"]+"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>', tab1_html, re.DOTALL)
print(f"Regex found {len(cards)} cards")

# Wait, let's write a script to look at the card titles first using basic search
titles = re.findall(r'<h3 class="[^"]+">(.*?)</h3>', tab1_html)
print(f"Titles found: {len(titles)}")
for t in titles:
    print(t)
