import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all destination cards inside tab1
tab1 = soup.find('section', id='tab1')
dest_cards = tab1.find_all('div', class_='destination-card')

print(f"Found {len(dest_cards)} destination cards in tab1:")
for i, card in enumerate(dest_cards, 1):
    h3 = card.find('h3')
    name = h3.text.strip() if h3 else "Unknown"
    category = card.get('data-category', 'beach')
    
    # rating
    rating_span = card.find('span', class_='bg-amber-50')
    rating = rating_span.text.replace('⭐', '').replace('/5', '').strip() if rating_span else ""
    if not rating:
        # check text content of other spans
        spans = card.find_all('span')
        for s in spans:
            if '⭐' in s.text:
                rating = s.text.replace('⭐', '').replace('/5', '').strip()
                break
                
    print(f"{i}. Name: {name} | Category: {category} | Rating: {rating}")
