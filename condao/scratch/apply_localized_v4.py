# -*- coding: utf-8 -*-
import os

def replace_in_file(filepath, replacements):
    print(f"Applying replacements in {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.")
        return False
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    replaced_count = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            replaced_count += 1
        else:
            # Silence print error or format as ascii safe
            pass
            
    print(f"  Replaced {replaced_count} out of {len(replacements)} items.")
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated {filepath}!")
        return True
    else:
        print(f"No changes made to {filepath}.")
        return False

# 1. Update index.html
index_replacements = [
    (
        "let trips = JSON.parse(localStorage.getItem('PORTFOLIO_TRIPS')) || DEFAULT_TRIPS;",
        """const PORTFOLIO_VERSION = '2.1';
        if (localStorage.getItem('PORTFOLIO_VERSION') !== PORTFOLIO_VERSION) {
            localStorage.setItem('PORTFOLIO_TRIPS', JSON.stringify(DEFAULT_TRIPS));
            localStorage.setItem('PORTFOLIO_VERSION', PORTFOLIO_VERSION);
        }
        let trips = JSON.parse(localStorage.getItem('PORTFOLIO_TRIPS')) || DEFAULT_TRIPS;"""
    )
]
replace_in_file("index.html", index_replacements)

# 2. Update dalat.html
dalat_replacements = [
    (
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.</p>',
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Xứ sở ngàn hoa rực rỡ, thành phố sương mù lãng mạn nơi núi rừng Tây Nguyên.</p>'
    ),
    (
        '<p class="text-gray-500 mt-2">Chạm vào thiên nhiên và lịch sử qua từng danh thắng Đà Lạt.</p>',
        '<p class="text-gray-500 mt-2">Chạm vào mây ngàn và thông xanh qua từng danh thắng Đà Lạt.</p>'
    ),
    (
        '<i class="fa-solid fa-landmark text-teal-600"></i> Lịch Sử & Tham Quan',
        '<i class="fa-solid fa-mountain-sun text-teal-600"></i> Check-in & Thiên Nhiên'
    ),
    (
        '<i class="fa-solid fa-gopuran text-teal-600"></i> Điểm Đến Tâm Linh',
        '<i class="fa-solid fa-seedling text-teal-600"></i> Café & Trải Nghiệm'
    ),
    (
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Tàu Cao Tốc 4N3Đ</h2>',
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Khám Phá Đà Lạt 4N3Đ</h2>'
    ),
    (
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình vượt sóng đại dương kết hợp trọn vẹn khám phá lịch sử, tâm linh, sinh thái biển đảo & ẩm thực đặc sắc.</p>',
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình lãng mạn giữa ngàn hoa kết hợp săn mây rừng thông, check-in đồi chè thơ mộng & thưởng thức ẩm thực đặc trưng phố núi.</p>'
    ),
    (
        '<option value="history">🏛 Di Tích Lịch Sử</option>',
        '<option value="nature">🌲 Thiên Nhiên & Check-in</option>'
    ),
    (
        '<option value="spiritual">🙏 Tâm Linh & Văn Hóa</option>',
        '<option value="cafe">☕ Trải Nghiệm & Café</option>'
    ),
    (
        "placeholder=\"Ví dụ: Bãi Đầm Trầu\"",
        "placeholder=\"Ví dụ: Thung lũng Tình Yêu\""
    ),
    (
        "Trang web cá nhân ghi lại hành trình khám phá Đà Lạt — viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.",
        "Trang web cá nhân ghi lại hành trình khám phá Đà Lạt — thành phố ngàn hoa rực rỡ, xứ sở sương mù và rừng thông lãng mạn."
    ),
    (
        "history: '🏛 Di Tích Lịch Sử',",
        "nature: '🌲 Thiên Nhiên & Check-in',"
    ),
    (
        "spiritual: '🙏 Tâm Linh & Văn Hóa',",
        "cafe: '☕ Trải Nghiệm & Café',"
    ),
    (
        "if (localStorage.getItem('dalat_db_initialized') !== 'yes')",
        "if (localStorage.getItem('dalat_db_initialized_v4') !== 'yes')"
    ),
    (
        "localStorage.setItem('dalat_db_initialized', 'yes');",
        "localStorage.setItem('dalat_db_initialized_v4', 'yes');"
    ),
    (
        "const mergedDests = [...existingDests.filter(d => !d.isDefault), ...DEFAULT_DESTINATIONS];",
        "const mergedDests = [...existingDests.filter(d => !d.isDefault && (!d.id || !d.id.includes('condao'))), ...DEFAULT_DESTINATIONS];"
    ),
    (
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault), ...DEFAULT_HOTELS];",
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault && (!h.id || !h.id.includes('condao'))), ...DEFAULT_HOTELS];"
    ),
    (
        "const mergedFood = [...existingFood.filter(f => !f.isDefault), ...DEFAULT_FOOD];",
        "const mergedFood = [...existingFood.filter(f => !f.isDefault && (!f.id || !f.id.includes('condao'))), ...DEFAULT_FOOD];"
    )
]
replace_in_file("dalat.html", dalat_replacements)

# 3. Update vinhhy.html
vinhhy_replacements = [
    (
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.</p>',
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Tuyệt tác vịnh biển hoang sơ, thiên đường nắng gió giữa rặng san hô cổ nghìn năm.</p>'
    ),
    (
        '<p class="text-gray-500 mt-2">Chạm vào thiên nhiên và lịch sử qua từng danh thắng Vĩnh Hy.</p>',
        '<p class="text-gray-500 mt-2">Chạm vào nắng gió và rạn san hô qua từng danh thắng Vĩnh Hy.</p>'
    ),
    (
        '<i class="fa-solid fa-landmark text-teal-600"></i> Lịch Sử & Tham Quan',
        '<i class="fa-solid fa-anchor text-teal-600"></i> Vịnh Biển & Trải Nghiệm'
    ),
    (
        '<i class="fa-solid fa-gopuran text-teal-600"></i> Điểm Đến Tâm Linh',
        '<i class="fa-solid fa-compass text-teal-600"></i> Khám Phá Hoang Sơ'
    ),
    (
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Tàu Cao Tốc 4N3Đ</h2>',
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Khám Phá Vịnh Vĩnh Hy 4N3Đ</h2>'
    ),
    (
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình vượt sóng đại dương kết hợp trọn vẹn khám phá lịch sử, tâm linh, sinh thái biển đảo & ẩm thực đặc sắc.</p>',
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình lướt sóng ngắm rạn san hô cổ kết hợp chinh phục cung đèo Núi Chúa hùng vĩ, sinh thái biển đảo & tiệc tôm hùm Bình Hưng.</p>'
    ),
    (
        '<option value="history">🏛 Di Tích Lịch Sử</option>',
        '<option value="bay">⚓ Vịnh Biển & Trải Nghiệm</option>'
    ),
    (
        '<option value="spiritual">🙏 Tâm Linh & Văn Hóa</option>',
        '<option value="nature">🧭 Khám Phá Hoang Sơ</option>'
    ),
    (
        "placeholder=\"Ví dụ: Bãi Đầm Trầu\"",
        "placeholder=\"Ví dụ: Hang Rái Vĩnh Hy\""
    ),
    (
        "Trang web cá nhân ghi lại hành trình khám phá Vĩnh Hy — viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.",
        "Trang web cá nhân ghi lại hành trình khám phá Vĩnh Hy — tuyệt tác vịnh biển hoang sơ, rạn san hô cổ và rặng núi Chúa hùng vĩ."
    ),
    (
        "history: '🏛 Di Tích Lịch Sử',",
        "bay: '⚓ Vịnh Biển & Trải Nghiệm',"
    ),
    (
        "spiritual: '🙏 Tâm Linh & Văn Hóa',",
        "nature: '🧭 Khám Phá Hoang Sơ',"
    ),
    (
        "if (localStorage.getItem('vinhhy_db_initialized') !== 'yes')",
        "if (localStorage.getItem('vinhhy_db_initialized_v4') !== 'yes')"
    ),
    (
        "localStorage.setItem('vinhhy_db_initialized', 'yes');",
        "localStorage.setItem('vinhhy_db_initialized_v4', 'yes');"
    ),
    (
        "const mergedDests = [...existingDests.filter(d => !d.isDefault), ...DEFAULT_DESTINATIONS];",
        "const mergedDests = [...existingDests.filter(d => !d.isDefault && (!d.id || !d.id.includes('condao'))), ...DEFAULT_DESTINATIONS];"
    ),
    (
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault), ...DEFAULT_HOTELS];",
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault && (!h.id || !h.id.includes('condao'))), ...DEFAULT_HOTELS];"
    ),
    (
        "const mergedFood = [...existingFood.filter(f => !f.isDefault), ...DEFAULT_FOOD];",
        "const mergedFood = [...existingFood.filter(f => !f.isDefault && (!f.id || !f.id.includes('condao'))), ...DEFAULT_FOOD];"
    )
]
replace_in_file("vinhhy.html", vinhhy_replacements)

# 4. Update vungtau.html
vungtau_replacements = [
    (
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.</p>',
        '<p class="text-lg md:text-2xl text-gray-200 max-w-2xl font-light opacity-0 animate-fade-in-up delay-200 leading-relaxed">Thành phố biển năng động, thiên đường ẩm thực và những cung đường biển rực rỡ nắng vàng.</p>'
    ),
    (
        '<p class="text-gray-500 mt-2">Chạm vào thiên nhiên và lịch sử qua từng danh thắng Vũng Tàu.</p>',
        '<p class="text-gray-500 mt-2">Chạm vào sóng vỗ và ẩm thực phố biển qua từng danh thắng Vũng Tàu.</p>'
    ),
    (
        '<i class="fa-solid fa-landmark text-teal-600"></i> Lịch Sử & Tham Quan',
        '<i class="fa-solid fa-umbrella-beach text-teal-600"></i> Bãi Biển & Check-in'
    ),
    (
        '<i class="fa-solid fa-gopuran text-teal-600"></i> Điểm Đến Tâm Linh',
        '<i class="fa-solid fa-utensils text-teal-600"></i> Ẩm Thực & Trải Nghiệm'
    ),
    (
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Tàu Cao Tốc 4N3Đ</h2>',
        '<h2 class="text-3xl md:text-4xl font-extrabold text-teal-700">Lịch Trình Chi Tiết Khám Phá Vũng Tàu 4N3Đ</h2>'
    ),
    (
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình vượt sóng đại dương kết hợp trọn vẹn khám phá lịch sử, tâm linh, sinh thái biển đảo & ẩm thực đặc sắc.</p>',
        '<p class="text-gray-500 mt-3 text-sm md:text-base">Hành trình lướt sóng tàu cánh ngầm ngắm biển ngập tràn nắng gió kết hợp chinh phục ngọn hải đăng cổ kính, ẩm thực đặc trưng & trải nghiệm nghỉ dưỡng.</p>'
    ),
    (
        '<option value="history">🏛 Di Tích Lịch Sử</option>',
        '<option value="beach">🏖 Bãi Biển & Check-in</option>'
    ),
    (
        '<option value="spiritual">🙏 Tâm Linh & Văn Hóa</option>',
        '<option value="food">🍽 Ẩm Thực & Trải Nghiệm</option>'
    ),
    (
        "placeholder=\"Ví dụ: Bãi Đầm Trầu\"",
        "placeholder=\"Ví dụ: Mũi Nghinh Phong\""
    ),
    (
        "Trang web cá nhân ghi lại hành trình khám phá Vũng Tàu — viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.",
        "Trang web cá nhân ghi lại hành trình khám phá Vũng Tàu — thành phố biển rực rỡ, năng động và thiên đường ẩm thực ngập tràn nắng gió."
    ),
    (
        "history: '🏛 Di Tích Lịch Sử',",
        "beach: '🏖 Bãi Biển & Check-in',"
    ),
    (
        "spiritual: '🙏 Tâm Linh & Văn Hóa',",
        "food: '🍽 Ẩm Thực & Trải Nghiệm',"
    ),
    (
        "if (localStorage.getItem('vungtau_db_initialized') !== 'yes')",
        "if (localStorage.getItem('vungtau_db_initialized_v4') !== 'yes')"
    ),
    (
        "localStorage.setItem('vungtau_db_initialized', 'yes');",
        "localStorage.setItem('vungtau_db_initialized_v4', 'yes');"
    ),
    (
        "const mergedDests = [...existingDests.filter(d => !d.isDefault), ...DEFAULT_DESTINATIONS];",
        "const mergedDests = [...existingDests.filter(d => !d.isDefault && (!d.id || !d.id.includes('condao'))), ...DEFAULT_DESTINATIONS];"
    ),
    (
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault), ...DEFAULT_HOTELS];",
        "const mergedHotels = [...existingHotels.filter(h => !h.isDefault && (!h.id || !h.id.includes('condao'))), ...DEFAULT_HOTELS];"
    ),
    (
        "const mergedFood = [...existingFood.filter(f => !f.isDefault), ...DEFAULT_FOOD];",
        "const mergedFood = [...existingFood.filter(f => !f.isDefault && (!f.id || !f.id.includes('condao'))), ...DEFAULT_FOOD];"
    ),
    (
        "Trải nghiệm đi tàu cao tốc Greenlines từ Bạch Đằng ra Vũng Tàu",
        "Trải nghiệm đi tàu cánh ngầm Greenlines từ Bạch Đằng ra Vũng Tàu"
    )
]
replace_in_file("vungtau.html", vungtau_replacements)

print("All replacements done!")
