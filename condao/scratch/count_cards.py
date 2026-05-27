import re

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all divs with destination-card class
dest_cards = re.findall(r'<div class="destination-card[^>]*>', html)
print('Destination cards:', len(dest_cards))

# Let's look at the containers
# 1. Destinations container
# 2. Hotels container
# 3. Food container
containers = ['destinations-container', 'hotels-container', 'food-container']
for c in containers:
    match = re.search(r'id="' + c + r'"', html)
    if match:
        print(f'Found container {c}')
    else:
        print(f'NOT found container {c}')
