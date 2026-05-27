import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate function renderDestCard
start_str = "function renderDestCard(d, idx) {"
idx = html.find(start_str)
if idx == -1:
    print("Could not find function renderDestCard in index.html!")
    sys.exit(1)

# Find the end of the function by brace tracking
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

old_func_block = content[:idx_close + 1]

# Our new, beautiful symmetrical layout that matches the original design exactly
new_func_block = """function renderDestCard(d, idx) {
    const catLabel = DEST_CATEGORY_LABELS[d.category] || d.category;
    const highlights = (d.highlights||[]).map(h=>`<li>${h}</li>`).join('');
    
    const img1HTML = d.img1 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img1}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    const img2HTML = d.img2 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img2}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    
    // For alternating orders like the original layout
    const imgOrderClass = idx % 2 === 0 ? 'md:order-1' : 'md:order-2';
    const infoOrderClass = idx % 2 === 0 ? 'md:order-2' : 'md:order-1';
    const slideClass = idx % 2 === 0 ? 'slide-left' : 'slide-right';
    
    const cardWrapper = d.linkUrl ? `onclick="window.open('${d.linkUrl}','_blank')"` : `onclick="if(!event.target.closest('.detail-panel')) toggleDetail(this)"`;
    
    // Show a premium star badge for admin-added destinations
    const badgeHTML = !d.isDefault ? `
        <span class="bg-teal-600 text-white text-[10px] font-bold px-2.5 py-0.5 rounded-full shadow-sm">
            <i class="fa-solid fa-star text-[9px] mr-0.5"></i> Mới
        </span>
    ` : '';
    
    // Premium tag-list under title
    const tagsHTML = d.tags && d.tags.length ? `
        <div class="flex flex-wrap gap-2 mb-3">
            ${d.tags.map(t => `<span class="bg-teal-50 text-teal-700 border border-teal-100 px-3 py-1 rounded-full text-xs font-semibold">#${t}</span>`).join('')}
        </div>
    ` : '';

    return `
    <div class="destination-card p-6 md:p-8 ${slideClass}" ${cardWrapper} data-category="${d.category}">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 md:gap-8 items-center">
            
            <!-- Image (alternating order) -->
            <div class="md:col-span-5 ${imgOrderClass}">
                ${d.img1 ? `
                <div class="dest-img-container shadow-md">
                    <img src="${d.img1}" alt="${d.name}" class="dest-img">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
                </div>` : `
                <div class="dest-img-container shadow-md bg-teal-50/50 flex items-center justify-center text-5xl text-teal-600">
                    🌴
                </div>`}
            </div>
            
            <!-- Info (alternating order) -->
            <div class="md:col-span-7 ${infoOrderClass} flex flex-col justify-between h-full">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-3">
                        ${d.rating ? `<span class="bg-amber-50 text-amber-700 border border-amber-100 px-3 py-1 rounded-full text-xs font-semibold">⭐ ${d.rating}/5</span>` : ''}
                        <span class="bg-teal-50 text-teal-700 border border-teal-100 px-3 py-1 rounded-full text-xs font-semibold">${catLabel}</span>
                        ${badgeHTML}
                    </div>
                    ${tagsHTML}
                    <h3 class="text-2xl md:text-3xl font-extrabold text-gray-800 hover:text-teal-700 transition-colors mb-4">${d.name}</h3>
                    <p class="text-gray-500 text-sm md:text-base leading-relaxed mb-6">${d.descShort||''}</p>
                </div>
                
                <div class="flex items-center justify-between gap-4">
                    <div class="flex items-center gap-4">
                        <span class="text-teal-600 font-bold text-sm flex items-center gap-2 hover:translate-x-1 transition-all toggle-text">
                            Khám phá chi tiết <i class="fa-solid fa-arrow-right-long ml-2"></i>
                        </span>
                        ${d.mapsUrl ? `
                        <a href="${d.mapsUrl}" target="_blank" class="px-3 py-1 rounded-full border border-gray-200 hover:border-teal-200 hover:bg-teal-50 text-gray-500 hover:text-teal-700 transition-colors flex items-center gap-1.5 text-xs font-bold" onclick="event.stopPropagation()">
                            <i class="fa-solid fa-map-location-dot text-teal-600"></i> Bản đồ
                        </a>` : ''}
                    </div>
                    <button class="w-10 h-10 rounded-full bg-teal-50 hover:bg-teal-100 text-teal-700 flex items-center justify-center transition-colors shadow-sm focus:outline-none">
                        <i class="fa-solid fa-chevron-down toggle-arrow"></i>
                    </button>
                </div>
            </div>
            
        </div>
        
        <!-- Collapsible Detail Panel (smooth CSS accordion) -->
        ${!d.linkUrl ? `
        <div class="detail-panel">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 text-gray-600">
                <div class="lg:col-span-7 space-y-4">
                    <h4 class="font-bold text-gray-800 text-lg mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-circle-info text-teal-600"></i> Giới thiệu chi tiết
                    </h4>
                    ${d.descLong ? `<p class="text-gray-600 leading-relaxed text-sm md:text-base">${d.descLong}</p>` : ''}
                    ${highlights ? `
                    <div class="bg-amber-50/60 border border-amber-100 p-4 rounded-xl">
                        <h5 class="font-bold text-amber-800 mb-1 flex items-center gap-2 text-sm md:text-base">
                            <i class="fa-solid fa-star text-amber-500"></i> Trải nghiệm nổi bật
                        </h5>
                        <ul class="list-disc pl-5 text-amber-900/80 text-xs md:text-sm space-y-1">${highlights}</ul>
                    </div>` : ''}
                    ${d.bestTime ? `
                    <div class="bg-teal-50/60 border border-teal-100 p-4 rounded-xl">
                        <h5 class="font-bold text-teal-800 mb-1 flex items-center gap-2 text-sm md:text-base">
                            <i class="fa-solid fa-clock text-teal-600"></i> Thời điểm lý tưởng
                        </h5>
                        <p class="text-teal-900/80 text-xs md:text-sm">${d.bestTime}</p>
                    </div>` : ''}
                </div>
                
                <div class="lg:col-span-5 space-y-3">
                    ${d.img1 || d.img2 ? `
                    <h4 class="font-bold text-gray-800 text-lg mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-images text-teal-600"></i> Hình ảnh thực tế
                    </h4>
                    <div class="grid ${d.img1 && d.img2 ? 'grid-cols-2' : 'grid-cols-1'} gap-3">
                        ${img1HTML}
                        ${img2HTML}
                    </div>` : ''}
                </div>
            </div>
        </div>` : ''}
    </div>`;
}"""

# Replace in html
html_updated = html.replace(old_func_block, new_func_block)

# Let's save it
with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'w', encoding='utf-8') as f:
    f.write(html_updated)

print("SUCCESS: Symmetric alternating card layout implemented!")
