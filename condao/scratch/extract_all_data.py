import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. PARSE DESTINATIONS (TAB 1)
# ============================================================
tab1_start = html.find('<section id="tab1"')
tab2_start = html.find('<section id="tab2"')
tab1_html = html[tab1_start:tab2_start]

# We will split tab1_html by comments like <!-- X. Name -->
# Note that the first comment might be <!-- 1. Vịnh Đầm Tre -->
blocks = re.split(r'<!-- \d+\.\s+([^>]+) -->', tab1_html)
destinations = []
for i in range(1, len(blocks), 2):
    title = blocks[i].strip()
    content = blocks[i+1]
    
    # Extract data-category
    cat_match = re.search(r'data-category="([^"]+)"', content)
    category = cat_match.group(1) if cat_match else "beach"
    
    # Extract rating (if any)
    rating_match = re.search(r'⭐\s*([\d\.]+)/5', content)
    rating = rating_match.group(1) if rating_match else ""
    
    # Extract images
    images = re.findall(r'src="([^"]+)"', content)
    images = [img for img in images if not img.endswith('.js') and not 'font-awesome' in img]
    img1 = images[0] if len(images) > 0 else ""
    img2 = images[1] if len(images) > 1 else ""
    
    # Extract tags (e.g. #Mùa_rong_mơ)
    tags = re.findall(r'#([a-zA-Z0-9_\u00C0-\u1EF9]+)', content)
    
    # Extract short desc (usually in paragraph right under h3)
    desc_p = re.search(r'<p class="text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc_short = desc_p.group(1).strip() if desc_p else ""
    desc_short = re.sub(r'<[^>]+>', '', desc_short)
    
    # Extract long desc (inside detail-panel)
    desc_long_match = re.search(r'Giới thiệu chi tiết.*?</h4>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    desc_long = desc_long_match.group(1).strip() if desc_long_match else ""
    desc_long = re.sub(r'<[^>]+>', '', desc_long)
    
    # Extract highlights
    highlights = []
    ul_match = re.search(r'<ul[^>]*>(.*?)</ul>', content, re.DOTALL)
    if ul_match:
        li_matches = re.findall(r'<li[^>]*>(.*?)</li>', ul_match.group(1), re.DOTALL)
        highlights = [re.sub(r'<[^>]+>', '', li).strip() for li in li_matches]
        
    # Extract best time
    best_time_match = re.search(r'Thời điểm lý tưởng.*?</h5>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    best_time = best_time_match.group(1).strip() if best_time_match else ""
    best_time = re.sub(r'<[^>]+>', '', best_time)
    
    # Extract mapsUrl
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
    # Extract linkUrl
    links = re.findall(r'href="([^"]+)"', content)
    link_url = ""
    for l in links:
        if 'google.com/maps' not in l and not l.startswith('#') and 'javascript:' not in l:
            link_url = l
            break
            
    dest_id = f"default_dest_{i//2 + 1}"
    
    destinations.append({
        "id": dest_id,
        "name": title,
        "category": category,
        "rating": rating,
        "img1": img1,
        "img2": img2,
        "tags": tags,
        "descShort": desc_short,
        "descLong": desc_long,
        "highlights": highlights,
        "bestTime": best_time,
        "mapsUrl": maps_url,
        "linkUrl": link_url,
        "isDefault": True
    })

print(f"Extracted {len(destinations)} destinations.")

# ============================================================
# 2. PARSE HOTELS (TAB 3)
# ============================================================
tab3_start = html.find('<section id="tab3"')
tab4_start = html.find('<section id="tab4"')
tab3_html = html[tab3_start:tab4_start]

hblocks = re.split(r'<!-- \d+\.\s+([^>]+) -->', tab3_html)
hotels = []
for i in range(1, len(hblocks), 2):
    title = hblocks[i].strip()
    content = hblocks[i+1]
    
    stars_match = re.search(r'(\d)\s*★', content)
    stars = stars_match.group(1) if stars_match else "3"
    
    price_match = re.search(r'fa-money-bill-wave.*?</i>\s*(.*?)\s*</span>', content, re.DOTALL)
    price = price_match.group(1).strip() if price_match else ""
    price = re.sub(r'<[^>]+>', '', price)
    
    addr_match = re.search(r'fa-location-dot.*?</i>\s*(.*?)\s*</span>', content, re.DOTALL)
    address = addr_match.group(1).strip() if addr_match else ""
    address = re.sub(r'<[^>]+>', '', address)
    
    desc_match = re.search(r'<p class="text-xs text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""
    desc = re.sub(r'<[^>]+>', '', desc)
    
    img_match = re.search(r'src="([^"]+)"', content)
    img_url = img_match.group(1) if img_match else ""
    
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
    links = re.findall(r'href="([^"]+)"', content)
    booking_url = ""
    for l in links:
        if 'google.com/maps' not in l:
            booking_url = l
            break
            
    hotel_id = f"default_hotel_{i//2 + 1}"
    
    hotels.append({
        "id": hotel_id,
        "name": title,
        "stars": stars,
        "price": price,
        "address": address,
        "desc": desc,
        "imgUrl": img_url,
        "mapsUrl": maps_url,
        "linkUrl": booking_url,
        "isDefault": True
    })

print(f"Extracted {len(hotels)} hotels.")

# ============================================================
# 3. PARSE FOODS (TAB 4)
# ============================================================
tab4_start = html.find('<section id="tab4"')
tab5_start = html.find('<section id="tab5"')
tab4_html = html[tab4_start:tab5_start]

# Split tab4 by comments like <!-- Card: ... -->
blocks = re.split(r'<!-- Card:\s*([^>]+)\s*-->', tab4_html)

foods = []
for i in range(1, len(blocks), 2):
    title = blocks[i].strip()
    content = blocks[i+1]
    
    cat_match = re.search(r'data-category="([^"]+)"', content)
    category = cat_match.group(1) if cat_match else "restaurant"
    
    img_match = re.search(r'src="([^"]+)"', content)
    img_url = img_match.group(1) if img_match else ""
    
    name_match = re.search(r'<h4[^>]*>(.*?)</h4>', content, re.DOTALL)
    if not name_match:
        name_match = re.search(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    name = name_match.group(1).strip() if name_match else title
    name = re.sub(r'<[^>]+>', '', name)
    
    addr_match = re.search(r'fa-location-dot.*?</i>\s*(.*?)\s*</p>', content, re.DOTALL)
    address = addr_match.group(1).strip() if addr_match else ""
    address = re.sub(r'<[^>]+>', '', address)
    
    desc_match = re.search(r'<p class="text-xs text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""
    desc = re.sub(r'<a[^>]*>.*?</a>', '', desc)
    desc = re.sub(r'<br\s*/?>', ' ', desc)
    desc = re.sub(r'<(?!strong|/strong)[^>]+>', '', desc)
    
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
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
        "imgUrl": img_url,
        "isDefault": True
    })

print(f"Extracted {len(foods)} foods.")

# Write all to standard JSON
db = {
    "destinations": destinations,
    "hotels": hotels,
    "foods": foods
}

with open('scratch/full_extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Saved all extracted data to scratch/full_extracted_data.json")
