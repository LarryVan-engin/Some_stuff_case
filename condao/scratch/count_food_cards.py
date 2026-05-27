import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/tab4_content.html', 'r', encoding='utf-8') as f:
    tab4_html = f.read()

# Let's find all divs with class="food-card"
# and split them
cards = re.split(r'<!-- Card:\s*([^-]+)\s*-->', tab4_html)
print(f"Split tab4 by comments: found {len(cards)} segments")

# Let's see if we can find all cards with class="food-card"
div_cards = re.findall(r'<div class="[^"]*food-card[^"]*"[^>]*>', tab4_html)
print(f"Found {len(div_cards)} food-cards by class")
