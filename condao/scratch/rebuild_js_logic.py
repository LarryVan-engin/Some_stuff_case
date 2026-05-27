import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index_migrated.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# NEW JS RENDERING LOGIC DEFINITIONS
# ============================================================

new_renderAdminDestCardsInTab1 = """function renderAdminDestCardsInTab1() {
    const container = document.getElementById('destinations-container');
    if(!container) return;
    const items = loadData(KEYS.adminDests);
    if(!items.length) { container.innerHTML = '<div class="text-center text-gray-400 py-12">Chưa có địa điểm nào.</div>'; return; }
    container.innerHTML = items.map((d, idx) => renderDestCard(d, idx)).join('');
    // Re-attach IntersectionObserver for all cards
    document.querySelectorAll('#destinations-container .destination-card').forEach(el => observer && observer.observe(el));
}"""

new_renderDestCard = """function renderDestCard(d, idx) {
    const catLabel = DEST_CATEGORY_LABELS[d.category] || d.category;
    const highlights = (d.highlights||[]).map(h=>`<li>${h}</li>`).join('');
    const img1HTML = d.img1 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img1}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    const img2HTML = d.img2 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img2}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    const cardWrapper = d.linkUrl ? `onclick="window.open('${d.linkUrl}','_blank')"` : `onclick="toggleDestDetail(this)"`;
    const slideClass = idx % 2 === 0 ? 'slide-left' : 'slide-right';
    
    // Check if it's admin custom or default
    const badgeHTML = !d.isDefault ? `
        <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm ml-2">Mới</span>
    ` : '';
    
    // Display tags if they exist
    const tagsHTML = d.tags && d.tags.length ? `
        <div class="flex flex-wrap gap-2 mb-3">
            ${d.tags.map(t=>`<span class="bg-teal-50 text-teal-700 border border-teal-100 px-3 py-1 rounded-full text-xs font-semibold">#${t}</span>`).join('')}
        </div>
    ` : '';

    return `
    <div class="destination-card p-4 md:p-6 ${slideClass}" ${cardWrapper} data-category="${d.category}">
        <div class="flex flex-col md:flex-row gap-4 items-start">
            ${d.img1?`<div class="dest-img-container w-full md:w-56 shrink-0"><img src="${d.img1}" class="dest-img" alt="${d.name}"></div>`:''}
            <div class="flex-grow">
                <div class="flex flex-wrap items-center gap-2 mb-1">
                    <h3 class="text-lg font-extrabold text-gray-800">${d.name}</h3>
                    ${badgeHTML}
                    ${d.rating?`<span class="bg-amber-50 text-amber-700 border border-amber-100 text-xs font-bold px-2 py-0.5 rounded-full">⭐ ${d.rating}/5</span>`:''}
                    <span class="bg-teal-50 text-teal-700 border border-teal-100 text-xs font-bold px-2 py-0.5 rounded-full">${catLabel}</span>
                </div>
                ${tagsHTML}
                <p class="text-gray-500 text-sm leading-relaxed mb-2">${d.descShort||''}</p>
                ${d.mapsUrl?`<a href="${d.mapsUrl}" target="_blank" onclick="event.stopPropagation()" class="text-teal-600 hover:text-teal-800 text-xs font-semibold flex items-center gap-1 w-fit">
                    <i class="fa-solid fa-map-location-dot"></i> Xem trên Google Maps
                </a>`:''}
                ${!d.linkUrl?`<div class="text-xs text-gray-400 mt-2 flex items-center gap-1"><i class="fa-solid fa-chevron-down text-[10px]"></i> Nhấn để xem chi tiết</div>`:''}
            </div>
        </div>
        ${!d.linkUrl?`
        <div class="detail-panel">
            <div class="border-t border-gray-100 mt-4 pt-4 grid grid-cols-1 lg:grid-cols-12 gap-6 text-gray-600">
                <div class="lg:col-span-7 space-y-4">
                    ${d.descLong?`<p class="text-gray-600 leading-relaxed text-sm">${d.descLong}</p>`:''}
                    ${highlights?`<div class="bg-amber-50/60 border border-amber-100 p-4 rounded-xl">
                        <h5 class="font-bold text-amber-800 mb-2 flex items-center gap-2 text-sm"><i class="fa-solid fa-star text-amber-500"></i> Trải nghiệm nổi bật</h5>
                        <ul class="list-disc pl-5 text-amber-900/80 text-xs space-y-1">${highlights}</ul>
                    </div>`:''}
                    ${d.bestTime?`<div class="bg-teal-50/60 border border-teal-100 p-4 rounded-xl">
                        <h5 class="font-bold text-teal-800 mb-1 flex items-center gap-2 text-sm"><i class="fa-solid fa-clock text-teal-600"></i> Thời điểm lý tưởng</h5>
                        <p class="text-teal-900/80 text-xs">${d.bestTime}</p>
                    </div>`:''}
                </div>
                <div class="lg:col-span-5 space-y-3">
                    ${d.img1||d.img2?`<h4 class="font-bold text-gray-800 text-lg mb-2 flex items-center gap-2"><i class="fa-solid fa-images text-teal-600"></i> Hình ảnh</h4>
                    <div class="grid ${d.img1&&d.img2?'grid-cols-2':'grid-cols-1'} gap-3">${img1HTML}${img2HTML}</div>`:''}
                </div>
            </div>
        </div>`:''}
    </div>`;
}"""

new_renderAdminHotelsInTab3 = """function renderAdminHotelsInTab3() {
    const hotelScrollDiv = document.getElementById('hotels-container');
    if(!hotelScrollDiv) return;
    const items = loadData(KEYS.adminHotels);
    if(!items.length){
        hotelScrollDiv.innerHTML = '<div class="text-center text-gray-400 py-12">Chưa có khách sạn nào.</div>';
        return;
    }
    hotelScrollDiv.innerHTML = items.map(h=>{
        const badgeHTML = !h.isDefault ? `
            <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-sm ml-2">Mới</span>
        ` : '';
        return `
        <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl flex flex-col sm:flex-row gap-4 transition-all duration-300 shadow-sm hover:shadow-md group ${h.linkUrl?'cursor-pointer':''}"
            ${h.linkUrl?`onclick="window.open('${h.linkUrl}','_blank')"`:''}>
            <div class="w-full sm:w-32 h-24 rounded-lg overflow-hidden shrink-0 shadow-sm relative">
                <img src="${h.imgUrl||'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400'}" alt="${h.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'">
                <span class="absolute top-1 left-1 bg-amber-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm">${h.stars} ★</span>
            </div>
            <div class="flex-grow flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start gap-2">
                        <div class="flex items-center gap-2">
                            <h4 class="font-bold text-gray-800 group-hover:text-teal-700 transition-colors text-sm sm:text-base">${h.name}</h4>
                            ${badgeHTML}
                        </div>
                        ${h.price?`<span class="bg-teal-50 text-teal-700 border border-teal-100 text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 whitespace-nowrap">${h.price}</span>`:''}
                    </div>
                    ${h.address?`<p class="text-[11px] text-gray-400 mt-0.5 flex items-center gap-1"><i class="fa-solid fa-location-dot"></i> ${h.address}</p>`:''}
                    ${h.desc?`<p class="text-xs text-gray-500 mt-2 leading-relaxed">${h.desc}</p>`:''}
                    <div class="flex gap-2 mt-2">
                        ${h.mapsUrl?`<a href="${h.mapsUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-teal-600 hover:underline flex items-center gap-1"><i class="fa-solid fa-map-location-dot"></i> Maps</a>`:''}
                        ${h.linkUrl?`<a href="${h.linkUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-green-600 hover:underline flex items-center gap-1"><i class="fa-solid fa-calendar-check"></i> Đặt phòng</a>`:''}
                    </div>
                </div>
            </div>
        </div>
    `}).join('');
}"""

new_renderAdminFoodInTab4 = """function renderAdminFoodInTab4() {
    const foodContainer = document.getElementById('food-container');
    if(!foodContainer) return;
    const items = loadData(KEYS.adminFood);
    if(!items.length){
        foodContainer.innerHTML = '<div class="text-center text-gray-400 py-12">Chưa có món ăn nào.</div>';
        return;
    }
    foodContainer.innerHTML = items.map(f=>{
        const badgeHTML = !f.isDefault ? `
            <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm ml-2">Mới</span>
        ` : '';
        return `
        <div class="food-card bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden group transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${f.linkUrl?'cursor-pointer':''}"
            data-category="${f.category}" ${f.linkUrl?`onclick="window.open('${f.linkUrl}','_blank')"`:''}> 
            <div class="relative overflow-hidden aspect-video">
                <img src="${f.imgUrl||'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600'}" alt="${f.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600'">
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <span class="absolute top-3 left-3 bg-white/90 backdrop-blur-sm text-gray-700 text-xs font-bold px-2.5 py-1 rounded-full">${FOOD_CAT_ICONS[f.category]||'🍴'} ${f.category}</span>
            </div>
            <div class="p-4">
                <div class="flex items-center">
                    <h3 class="font-extrabold text-gray-800 text-base group-hover:text-teal-700 transition-colors mb-1">${f.name}</h3>
                    ${badgeHTML}
                </div>
                ${f.address?`<p class="text-xs text-gray-400 flex items-center gap-1 mb-2"><i class="fa-solid fa-location-dot text-teal-500"></i> ${f.address}</p>`:''}
                ${f.desc?`<p class="text-xs text-gray-600 leading-relaxed mb-3">${f.desc}</p>`:''}
                <div class="flex items-center gap-2">
                    ${f.mapsUrl?`<a href="${f.mapsUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-teal-600 hover:text-teal-800 font-semibold flex items-center gap-1 transition-colors"><i class="fa-solid fa-map-location-dot"></i> Maps</a>`:''}
                    ${f.linkUrl?`<a href="${f.linkUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1 transition-colors ml-auto"><i class="fa-solid fa-star"></i> Review</a>`:''}
                </div>
            </div>
        </div>
    `}).join('');
}"""

new_initAdminItems = """(function initAdminItems() {
    // Initialize defaults in localStorage if not done
    if (localStorage.getItem('condao_db_initialized') !== 'yes') {
        const existingDests = JSON.parse(localStorage.getItem(KEYS.adminDests)) || [];
        const existingHotels = JSON.parse(localStorage.getItem(KEYS.adminHotels)) || [];
        const existingFood = JSON.parse(localStorage.getItem(KEYS.adminFood)) || [];
        
        const mergedDests = [...existingDests.filter(d => !d.isDefault), ...DEFAULT_DESTINATIONS];
        const mergedHotels = [...existingHotels.filter(h => !h.isDefault), ...DEFAULT_HOTELS];
        const mergedFood = [...existingFood.filter(f => !f.isDefault), ...DEFAULT_FOOD];
        
        localStorage.setItem(KEYS.adminDests, JSON.stringify(mergedDests));
        localStorage.setItem(KEYS.adminHotels, JSON.stringify(mergedHotels));
        localStorage.setItem(KEYS.adminFood, JSON.stringify(mergedFood));
        
        localStorage.setItem('condao_db_initialized', 'yes');
    }

    // Init memories password if not set
    if(!localStorage.getItem(KEYS.memPass)) {
        localStorage.setItem(KEYS.memPass, simpleHash(DEFAULT_MEM_PASSWORD));
    }
    // Check if memories session already unlocked
    if(sessionStorage.getItem('memoriesUnlocked')==='yes') {
        document.getElementById('mem-gate').classList.add('hidden');
        document.getElementById('mem-content').classList.remove('hidden');
        renderMemoryAlbums();
    }
    // Render all content (default + admin) into tabs
    renderAdminDestCardsInTab1();
    renderAdminHotelsInTab3();
    renderAdminFoodInTab4();
})();"""

# ============================================================
# REPLACE JS FUNCTIONS IN TEXT
# ============================================================

# We can use regex to find the start of a function and matching closing bracket, 
# but a simpler way is string replacement since the function signatures are unique!

# 1. replace renderAdminDestCardsInTab1
idx = html.find('function renderAdminDestCardsInTab1()')
end_idx = html.find('}', idx)
# wait, there's nested braces in renderAdminDestCardsInTab1, let's find the closing brace exactly
content = html[idx:]
depth = 0
idx_close = 0
for idx_close, char in enumerate(content):
    if char == '{':
        depth += 1
    elif char == '}':
        depth -= 1
        if depth == 0:
            break
            
html_replace_1 = html[:idx] + new_renderAdminDestCardsInTab1 + html[idx + idx_close + 1:]

# 2. replace renderDestCard
html = html_replace_1
idx = html.find('function renderDestCard(d)')
content = html[idx:]
depth = 0
idx_close = 0
for idx_close, char in enumerate(content):
    if char == '{':
        depth += 1
    elif char == '}':
        depth -= 1
        if depth == 0:
            break
            
html_replace_2 = html[:idx] + new_renderDestCard + html[idx + idx_close + 1:]

# 3. replace renderAdminHotelsInTab3
html = html_replace_2
idx = html.find('function renderAdminHotelsInTab3()')
content = html[idx:]
depth = 0
idx_close = 0
for idx_close, char in enumerate(content):
    if char == '{':
        depth += 1
    elif char == '}':
        depth -= 1
        if depth == 0:
            break
            
html_replace_3 = html[:idx] + new_renderAdminHotelsInTab3 + html[idx + idx_close + 1:]

# 4. replace renderAdminFoodInTab4
html = html_replace_3
idx = html.find('function renderAdminFoodInTab4()')
content = html[idx:]
depth = 0
idx_close = 0
for idx_close, char in enumerate(content):
    if char == '{':
        depth += 1
    elif char == '}':
        depth -= 1
        if depth == 0:
            break
            
html_replace_4 = html[:idx] + new_renderAdminFoodInTab4 + html[idx + idx_close + 1:]

# 5. replace initAdminItems
html = html_replace_4
idx = html.find('(function initAdminItems()')
content = html[idx:]
depth = 0
idx_close = 0
for idx_close, char in enumerate(content):
    if char == '(':
        depth += 1
    elif char == ')':
        depth -= 1
        if depth == 0:
            break
# Note it ends with )(); or similar
# Let's see: (function initAdminItems() { ... })();
# So the closing is nested: let's track braces
idx_brace = content.find('{')
depth_brace = 1
idx_close_brace = idx_brace
for idx_close_brace, char in enumerate(content[idx_brace+1:], idx_brace+1):
    if char == '{':
        depth_brace += 1
    elif char == '}':
        depth_brace -= 1
        if depth_brace == 0:
            break

# The block ends after the closing brace, followed by empty space, and )();
# So it ends at idx_close_brace + 5 or 6 (i.e. '})();')
end_of_block = html.find('})();', idx + idx_close_brace) + 5

html_final = html[:idx] + new_initAdminItems + html[end_of_block:]

# Write final file
with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)
print("Finished rewriting index.html with perfect unified dynamic rendering and CRUD support!")
