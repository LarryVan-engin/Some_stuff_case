import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's read full extracted data
with open('scratch/full_extracted_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Let's locate the zones
# 1. Destinations container
dest_start_tag = '<div class="space-y-12 max-w-5xl mx-auto" id="destinations-container">'
dest_start_idx = html.find(dest_start_tag)
if dest_start_idx == -1:
    print("Could not find destinations start tag!")
    sys.exit(1)

# Find </section> after it
dest_end_idx = html.find('</section>', dest_start_idx)
# The destinations-container div ends right before </section> (usually a </div>\s*)
# Let's search backward from </section> to find the closing </div>
close_div_match = re.search(r'</div>\s*$', html[dest_start_idx:dest_end_idx].rstrip())
if not close_div_match:
    print("Could not find destinations close div!")
    sys.exit(1)

dest_end_tag_idx = dest_start_idx + html[dest_start_idx:dest_end_idx].rfind('</div>')
dest_block = html[dest_start_idx + len(dest_start_tag) : dest_end_tag_idx]

print(f"Destinations block starts at {dest_start_idx}, ends at {dest_end_tag_idx}")
print("First 100 chars of dest block:\n", dest_block[:100])
print("Last 100 chars of dest block:\n", dest_block[-100:])

# 2. Hotels list container
hotel_start_tag = '<div class="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">'
hotel_start_idx = html.find(hotel_start_tag)
if hotel_start_idx == -1:
    print("Could not find hotels start tag!")
    sys.exit(1)

# We want to find the matching </div> or simply search backward from </section> of tab3
tab3_section_end = html.find('</section>', hotel_start_idx)
hotel_end_tag_idx = hotel_start_idx + html[hotel_start_idx:tab3_section_end].rfind('</div>')
# Wait, let's verify if there is an outer div that needs to be preserved
# The container itself is <div class="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">...</div>
# Inside there are hotel cards, then a closing </div>. Let's find the closing </div> of the container.
# It should be the last </div> before the closing </section> of tab3.
# Let's search backward from tab3_section_end
hotel_end_tag_idx = hotel_start_idx + html[hotel_start_idx:tab3_section_end].rfind('</div>')
# Wait! Let's find the exact close tag of the hotel container by tracking div nesting
# Let's write a parser to find the matching close tag
content = html[hotel_start_idx + len(hotel_start_tag):]
depth = 1
idx = 0
for idx, char in enumerate(content):
    if content[idx:idx+4] == '<div':
        depth += 1
    elif content[idx:idx+6] == '</div':
        depth -= 1
        if depth == 0:
            break
            
hotel_end_tag_idx = hotel_start_idx + len(hotel_start_tag) + idx
hotel_block = html[hotel_start_idx + len(hotel_start_tag) : hotel_end_tag_idx]

print(f"\nHotels block starts at {hotel_start_idx}, ends at {hotel_end_tag_idx}")
print("First 100 chars of hotel block:\n", hotel_block[:100])
print("Last 100 chars of hotel block:\n", hotel_block[-100:])

# 3. Food container
food_start_tag = 'id="food-container">'
food_start_idx = html.find(food_start_tag)
if food_start_idx == -1:
    print("Could not find food start tag!")
    sys.exit(1)
    
food_start_idx_full = html.rfind('<div', 0, food_start_idx)
food_start_tag_full = html[food_start_idx_full : food_start_idx + len(food_start_tag)]

# Find matching close tag
content_food = html[food_start_idx_full + len(food_start_tag_full):]
depth = 1
idx = 0
for idx, char in enumerate(content_food):
    if content_food[idx:idx+4] == '<div':
        depth += 1
    elif content_food[idx:idx+6] == '</div':
        depth -= 1
        if depth == 0:
            break
            
food_end_tag_idx = food_start_idx_full + len(food_start_tag_full) + idx
food_block = html[food_start_idx_full + len(food_start_tag_full) : food_end_tag_idx]

print(f"\nFood block starts at {food_start_idx_full}, ends at {food_end_tag_idx}")
print("First 100 chars of food block:\n", food_block[:100])
print("Last 100 chars of food block:\n", food_block[-100:])
print("Size of food block:", len(food_block))
print("Food start tag full:", food_start_tag_full)
