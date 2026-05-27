import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tab4_start = html.find('<section id="tab4"')
tab5_start = html.find('<section id="tab5"')
tab4_html = html[tab4_start:tab5_start]

# Let's find all blocks matching <!-- Card: ... -->
# and parse each block
blocks = re.split(r'<!-- Card:\s*([^>]+)\s*-->', tab4_html)

foods = []
for i in range(1, len(blocks), 2):
    title = blocks[i].strip()
    content = blocks[i+1]
    
    # data-category
    cat_match = re.search(r'data-category="([^"]+)"', content)
    category = cat_match.group(1) if cat_match else "restaurant"
    
    # img
    img_match = re.search(r'src="([^"]+)"', content)
    img_url = img_match.group(1) if img_match else ""
    
    # h4 or h3 title (sometimes it's h4 as we saw)
    name_match = re.search(r'<h4[^>]*>(.*?)</h4>', content, re.DOTALL)
    if not name_match:
        name_match = re.search(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    name = name_match.group(1).strip() if name_match else title
    name = re.sub(r'<[^>]+>', '', name)
    
    # address
    addr_match = re.search(r'fa-location-dot.*?</i>\s*(.*?)\s*</p>', content, re.DOTALL)
    address = addr_match.group(1).strip() if addr_match else ""
    address = re.sub(r'<[^>]+>', '', address)
    
    # description
    # usually text-xs text-gray-500
    desc_match = re.search(r'<p class="text-xs text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""
    # let's keep strong tags but strip other things if needed. Let's just remove all tags or keep strong
    desc = re.sub(r'<a[^>]*>.*?</a>', '', desc) # remove any links
    desc = re.sub(r'<br\s*/?>', ' ', desc)
    # keep strong tags as they are useful, but let's see. Let's strip other html tags
    desc = re.sub(r'<(?!strong|/strong)[^>]+>', '', desc)
    
    # mapsUrl
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
    # linkUrl (review link if any, e.g. for Cơm niêu, let's see if there is any other link)
    links = re.findall(r'href="([^"]+)"', content)
    link_url = ""
    for l in links:
        if 'google.com/maps' not in l:
            link_url = l
            break
            
    food_id = f"default_food_{i//2 + 1}"
    foods.append({
        "id": food_id,
        "name": name,
        "category": category,
        "address": address,
        "mapsUrl": maps_url,
        "linkUrl": link_url,
        "desc": desc,
        "imgUrl": img_url
    })

print(f"Extracted {len(foods)} foods.")
for f in foods[:3]:
    print(f)
    print("-" * 50)
