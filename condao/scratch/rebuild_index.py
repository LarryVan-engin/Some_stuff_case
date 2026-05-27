import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load the extracted JSON
with open('scratch/full_extracted_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 2. Read the current index.html
with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make a backup first
with open(r'd:\VSCode\Some_stuff_case\condao\index.html.bak', 'w', encoding='utf-8') as f:
    f.write(html)
print("Backup created at index.html.bak")

# ============================================================
# REPLACE HTML BLOCKS WITH DYNAMIC CONTAINERS
# ============================================================

# --- TAB 1 DESTINATIONS ---
dest_start_tag = '<div class="space-y-12 max-w-5xl mx-auto" id="destinations-container">'
dest_start_idx = html.find(dest_start_tag)
if dest_start_idx == -1:
    print("Could not find destinations container!")
    sys.exit(1)

# Find </section> of tab1
dest_section_end = html.find('</section>', dest_start_idx)
# Find the last </div> before it
dest_end_tag_idx = dest_start_idx + html[dest_start_idx:dest_section_end].rfind('</div>')

# Replace the block
dest_placeholder = '\n                <!-- RENDERED DYNAMICALLY BY JAVASCRIPT -->\n            '
html = html[:dest_start_idx + len(dest_start_tag)] + dest_placeholder + html[dest_end_tag_idx:]
print("Tab 1 HTML replaced with dynamic placeholder.")

# --- TAB 3 HOTELS ---
hotel_start_tag = '<!-- Scrollable list of hotels -->\n                    <div class="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">'
hotel_start_idx = html.find(hotel_start_tag)
if hotel_start_idx == -1:
    print("Could not find hotel start tag!")
    sys.exit(1)

# Find the next </div>\n                </div>\n\n            </div>\n        </section>
hotel_end_pattern = '</div>\n                </div>\n\n            </div>\n        </section>'
hotel_end_idx = html.find(hotel_end_pattern, hotel_start_idx)
if hotel_end_idx == -1:
    # try slightly different whitespace
    hotel_end_idx = html.find('</div>\n                </div>\n\n            </div>\n        </section>', hotel_start_idx)

# We want to replace inside <div class="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar" id="hotels-container">
hotel_placeholder_container = '<!-- Scrollable list of hotels -->\n                    <div class="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar" id="hotels-container">\n                        <!-- RENDERED DYNAMICALLY BY JAVASCRIPT -->\n                    '
html = html[:hotel_start_idx] + hotel_placeholder_container + html[hotel_end_idx:]
print("Tab 3 HTML replaced with dynamic placeholder.")

# --- TAB 4 FOOD ---
food_start_tag = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto" id="food-container">'
food_start_idx = html.find(food_start_tag)
if food_start_idx == -1:
    print("Could not find food container start tag!")
    sys.exit(1)

# Find the next </section>
food_section_end = html.find('</section>', food_start_idx)
food_end_tag_idx = food_start_idx + html[food_start_idx:food_section_end].rfind('</div>')

food_placeholder = '\n                <!-- RENDERED DYNAMICALLY BY JAVASCRIPT -->\n            '
html = html[:food_start_idx + len(food_start_tag)] + food_placeholder + html[food_end_tag_idx:]
print("Tab 4 HTML replaced with dynamic placeholder.")

# ============================================================
# INJECT DATA DEFINITIONS AND HELPER FUNCTIONS IN JS
# ============================================================

# Format data lists to JS
js_data = f"""
// ============================================================
// DEFAULT CONTENT DATABASE (MIGRATED TO LOCALSTORAGE)
// ============================================================
const DEFAULT_DESTINATIONS = {json.dumps(db['destinations'], ensure_ascii=False, indent=4)};

const DEFAULT_HOTELS = {json.dumps(db['hotels'], ensure_ascii=False, indent=4)};

const DEFAULT_FOOD = {json.dumps(db['foods'], ensure_ascii=False, indent=4)};
"""

# Let's inject this right inside `<script>` before `const KEYS = {`
script_tag = '<script>'
script_idx = html.find(script_tag)
if script_idx == -1:
    print("Could not find script tag!")
    sys.exit(1)

# We will inject right after `<script>`
html = html[:script_idx + len(script_tag)] + js_data + html[script_idx + len(script_tag):]
print("Inserted DEFAULT content databases into JS.")

# Save temporary result
with open(r'd:\VSCode\Some_stuff_case\condao\index_migrated.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved temporary result to index_migrated.html")
