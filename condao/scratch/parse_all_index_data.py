import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. PARSE DESTINATIONS (TAB 1)
# ============================================================
# Let's find each card in destinations-container.
# In tab1:
# <!-- 1. Vịnh Đầm Tre -->
# <div class="destination-card ... " data-category="...">
# We can find all destination cards in tab1 using regex
# Since the comments list each item like "<!-- 1. Vịnh Đầm Tre -->", we can use them as delimiters!

# Let's find all the comments in tab1 that start with "<!-- X. Name -->"
items_raw = re.split(r'<!-- \d+\.\s+([^>]+) -->', html)
# This will alternate between text and title!
# We want to search only within tab1
tab1_start = html.find('<section id="tab1"')
tab2_start = html.find('<section id="tab2"')
tab1_html = html[tab1_start:tab2_start]

# Split tab1_html by comments like <!-- 1. Vịnh Đầm Tre -->
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
    # We can find any src in content, except fontawesome or other icons
    # e.g., src="./media__..." or src="https://..."
    images = re.findall(r'src="([^"]+)"', content)
    # Filter out tailwind or other scripts (should only be images in the card)
    images = [img for img in images if not img.endswith('.js') and not 'font-awesome' in img]
    img1 = images[0] if len(images) > 0 else ""
    img2 = images[1] if len(images) > 1 else ""
    
    # Extract tags (e.g. #Mùa_rong_mơ)
    tags = re.findall(r'#([a-zA-Z0-9_\u00C0-\u1EF9]+)', content)
    
    # Extract short desc (usually in paragraph right under h3)
    # <p class="text-gray-500 ... mb-6">\s*(.*?)\s*</p>
    desc_p = re.search(r'<p class="text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc_short = desc_p.group(1).strip() if desc_p else ""
    # remove html tags if any
    desc_short = re.sub(r'<[^>]+>', '', desc_short)
    
    # Extract long desc (inside detail-panel)
    # <h4.*?>\s*<i class="fa-solid fa-circle-info.*?></i>\s*Giới thiệu chi tiết\s*</h4>\s*<p class=".*?">\s*(.*?)\s*</p>
    desc_long_match = re.search(r'Giới thiệu chi tiết.*?</h4>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    desc_long = desc_long_match.group(1).strip() if desc_long_match else ""
    desc_long = re.sub(r'<[^>]+>', '', desc_long)
    
    # Extract highlights
    # <ul class="list-disc ...">(.*?)</ul>
    highlights = []
    ul_match = re.search(r'<ul[^>]*>(.*?)</ul>', content, re.DOTALL)
    if ul_match:
        li_matches = re.findall(r'<li[^>]*>(.*?)</li>', ul_match.group(1), re.DOTALL)
        highlights = [re.sub(r'<[^>]+>', '', li).strip() for li in li_matches]
        
    # Extract best time
    # <h5 class=".*?">.*?Thời điểm lý tưởng</h5>\s*<p[^>]*>(.*?)</p>
    best_time_match = re.search(r'Thời điểm lý tưởng.*?</h5>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
    best_time = best_time_match.group(1).strip() if best_time_match else ""
    best_time = re.sub(r'<[^>]+>', '', best_time)
    
    # Extract mapsUrl
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
    # Extract linkUrl
    # If it is a direct link (for the 2 food items at the end, let's see if they have external links)
    link_url = "" # default
    
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
        "linkUrl": link_url
    })

print(f"Extracted {len(destinations)} destinations.")

# ============================================================
# 2. PARSE HOTELS (TAB 3)
# ============================================================
# In tab3:
# <!-- 1. Six Senses Côn Đảo -->
# <div class="... flex-col sm:flex-row gap-4 ...">
# Let's split by comments like <!-- 1. Six Senses Côn Đảo -->
tab3_start = html.find('<section id="tab3"')
tab4_start = html.find('<section id="tab4"')
tab3_html = html[tab3_start:tab4_start]

hblocks = re.split(r'<!-- \d+\.\s+([^>]+) -->', tab3_html)
hotels = []
for i in range(1, len(hblocks), 2):
    title = hblocks[i].strip()
    content = hblocks[i+1]
    
    # Stars (e.g. 5 ★ or 4 ★ or 3 ★)
    stars_match = re.search(r'(\d)\s*★', content)
    stars = stars_match.group(1) if stars_match else "3"
    
    # Price range (e.g. Từ 15.000.000đ/đêm)
    price_match = re.search(r'fa-money-bill-wave.*?</i>\s*(.*?)\s*</span>', content, re.DOTALL)
    price = price_match.group(1).strip() if price_match else ""
    price = re.sub(r'<[^>]+>', '', price)
    
    # Address
    addr_match = re.search(r'fa-location-dot.*?</i>\s*(.*?)\s*</span>', content, re.DOTALL)
    address = addr_match.group(1).strip() if addr_match else ""
    address = re.sub(r'<[^>]+>', '', address)
    
    # Description
    desc_match = re.search(r'<p class="text-xs text-gray-500[^>]*>(.*?)</p>', content, re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""
    desc = re.sub(r'<[^>]+>', '', desc)
    
    # Image
    img_match = re.search(r'src="([^"]+)"', content)
    img_url = img_match.group(1) if img_match else ""
    
    # Maps URL
    maps_match = re.search(r'href="(https://www.google.com/maps/[^"]+)"', content)
    maps_url = maps_match.group(1) if maps_match else ""
    
    # Booking URL / Link
    # Find any booking link that is NOT google maps
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
        "linkUrl": booking_url
    })

print(f"Extracted {len(hotels)} hotels.")

# ============================================================
# 3. PARSE FOODS (TAB 4)
# ============================================================
# In tab4, let's find the cards.
# Wait, let's look at the structure of tab4 cards.
# Let's inspect food cards using python first to write the parser correctly.
print("Finished basic analysis of tab3 and tab1.")
with open('scratch/extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump({"destinations": destinations, "hotels": hotels}, f, ensure_ascii=False, indent=2)
