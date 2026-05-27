# -*- coding: utf-8 -*-
import os
import re

def process_index():
    path = r"d:\VSCode\Some_stuff_case\condao\index.html"
    print(f"Processing index.html...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Shrink homepage glass card to show more background
    target = """                    <div class="relative z-10 w-full max-w-3xl px-6" data-tilt data-tilt-max="10" data-tilt-speed="400" data-tilt-perspective="1000" data-tilt-glare="true" data-tilt-max-glare="0.2">
                        <div class="glass-card p-10 md:p-16 rounded-3xl text-center flex flex-col items-center shadow-2xl">
                            <div class="tilt-inner fade-in-up">
                                <span class="text-sm md:text-base uppercase tracking-[0.3em] text-white/70 mb-4 block font-semibold">Điểm đến</span>
                                <h2 class="text-4xl md:text-6xl font-serif font-bold mb-6 text-white leading-tight">${trip.title}</h2>
                                <div class="w-24 h-1 bg-white/50 mx-auto mb-8 rounded-full"></div>
                                <p class="text-base md:text-lg font-light text-white/90 leading-relaxed mb-10 max-w-xl mx-auto">${trip.desc}</p>
                                <a href="${trip.link}" class="inline-block relative overflow-hidden group bg-white/10 backdrop-blur-md border border-white/40 hover:bg-white hover:text-black hover:border-white transition-all duration-300 px-10 py-4 rounded-full text-sm font-semibold tracking-widest uppercase shadow-[0_0_15px_rgba(255,255,255,0.05)] hover:shadow-[0_0_30px_rgba(255,255,255,0.4)] hover:scale-105">
                                    Khám Phá Hành Trình
                                </a>
                            </div>
                        </div>
                    </div>"""

    replacement = """                    <div class="relative z-10 w-full max-w-xl px-6" data-tilt data-tilt-max="10" data-tilt-speed="400" data-tilt-perspective="1000" data-tilt-glare="true" data-tilt-max-glare="0.2">
                        <div class="glass-card p-6 md:p-8 rounded-2xl text-center flex flex-col items-center shadow-2xl">
                            <div class="tilt-inner fade-in-up">
                                <span class="text-xs md:text-sm uppercase tracking-[0.3em] text-white/70 mb-3 block font-semibold">Điểm đến</span>
                                <h2 class="text-3xl md:text-4xl font-serif font-bold mb-4 text-white leading-tight">${trip.title}</h2>
                                <div class="w-16 h-0.5 bg-white/40 mx-auto mb-5 rounded-full"></div>
                                <p class="text-sm md:text-base font-light text-white/80 leading-relaxed mb-6 max-w-lg mx-auto">${trip.desc}</p>
                                <a href="${trip.link}" class="inline-block relative overflow-hidden group bg-white/10 backdrop-blur-md border border-white/40 hover:bg-white hover:text-black hover:border-white transition-all duration-300 px-8 py-3 rounded-full text-xs font-semibold tracking-widest uppercase shadow-[0_0_15px_rgba(255,255,255,0.05)] hover:shadow-[0_0_30px_rgba(255,255,255,0.4)] hover:scale-105">
                                    Khám Phá Hành Trình
                                </a>
                            </div>
                        </div>
                    </div>"""

    content = content.replace(target, replacement)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success index.html!")

def process_condao():
    path = r"d:\VSCode\Some_stuff_case\condao\condao.html"
    print(f"Processing condao.html...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add boat options to planner dropdown
    dropdown_target = """                                <select id="planner-dest-select" class="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 text-gray-700 shadow-inner font-semibold">
                                    <option value="Vịnh Đầm Tre">1. Vịnh Đầm Tre (#Mùa_rong_mơ)</option>
                                    <option value="Bãi Đầm Trầu">2. Bãi Đầm Trầu (#Bãi_tắm_đẹp)</option>
                                    <option value="Bãi Nhát">3. Bãi Nhát (#Phong_cảnh_hữu_tình)</option>
                                    <option value="Bãi Suối Nóng">4. Bãi Suối Nóng (#Hoang_sơ_hiếm_có)</option>
                                    <option value="Bãi Đá Cuội">5. Bãi Đá Cuội (#Khu_Bến_Đầm)</option>
                                    <option value="Hòn Bảy Cạnh">6. Hòn Bảy Cạnh (#Bảo_tồn_rùa)</option>
                                    <option value="Hòn Cau & Miếu Cô Vân">7. Hòn Cau & Miếu Cô Vân (#Hòn_Cau)</option>
                                    <option value="Bãi Đất Thắm">8. Bãi Đất Thắm (#Private_Beach)</option>
                                    <option value="Hòn Tài, Hòn Trác">9. Hòn Tài, Hòn Trác (#Hòn_đảo_ẩn_giấu)</option>
                                    <option value="Bảo tàng Côn Đảo">10. Bảo tàng Côn Đảo (#Lưu_giữ_hiện_vật)</option>
                                    <option value="Nhà tù Côn Đảo (Trại Phú Hải, Phú Sơn)">11. Nhà tù Côn Đảo (Trại Phú Hải, Phú Sơn) (#Di_tích_quốc_gia)</option>
                                    <option value="Dinh Chúa Đảo">12. Dinh Chúa Đảo (#Kiến_trúc_Pháp_cổ)</option>
                                    <option value="Trung Tâm Bảo Tồn Di Tích Quốc Gia">13. Trung Tâm Bảo Tồn Di Tích Quốc Gia (#Đường_Nguyễn_Huệ)</option>
                                    <option value="Cầu tàu 914">14. Cầu tàu 914 (#Chứng_nhân_lịch_sử)</option>
                                    <option value="Mũi Cá Mập">15. Mũi Cá Mập (#Tọa_độ_lý_tưởng)</option>
                                    <option value="Nghĩa trang Hàng Dương">16. Nghĩa trang Hàng Dương (#Tâm_linh_thiêng_liêng)</option>
                                    <option value="Miếu Cậu (Thiếu Gia Miếu)">17. Miếu Cậu (Thiếu Gia Miếu) (#Hoàng_tử_Cải)</option>
                                    <option value="Miếu Năm Cô (Miếu Ngũ Hành)">18. Miếu Năm Cô (Miếu Ngũ Hành) (#Thờ_Ngũ_Hành)</option>
                                    <option value="Chùa Núi Một (Vân Sơn Tự)">19. Chùa Núi Một (Vân Sơn Tự) (#Tựa_sơn_hướng_thủy)</option>
                                    <option value="Cua mặt trăng">20. Cua mặt trăng (#Đặc_sản_quý_hiếm)</option>
                                    <option value="Mứt hạt bàng">21. Mứt hạt bàng (#Quà_tặng_Côn_Đảo)</option>
                                </select>"""

    dropdown_replacement = """                                <select id="planner-dest-select" class="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 text-gray-700 shadow-inner font-semibold">
                                    <option value="Vịnh Đầm Tre">1. Vịnh Đầm Tre (#Mùa_rong_mơ)</option>
                                    <option value="Bãi Đầm Trầu">2. Bãi Đầm Trầu (#Bãi_tắm_đẹp)</option>
                                    <option value="Bãi Nhát">3. Bãi Nhát (#Phong_cảnh_hữu_tình)</option>
                                    <option value="Bãi Suối Nóng">4. Bãi Suối Nóng (#Hoang_sơ_hiếm_có)</option>
                                    <option value="Bãi Đá Cuội">5. Bãi Đá Cuội (#Khu_Bến_Đầm)</option>
                                    <option value="Hòn Bảy Cạnh">6. Hòn Bảy Cạnh (#Bảo_tồn_rùa)</option>
                                    <option value="Hòn Cau & Miếu Cô Vân">7. Hòn Cau & Miếu Cô Vân (#Hòn_Cau)</option>
                                    <option value="Bãi Đất Thắm">8. Bãi Đất Thắm (#Private_Beach)</option>
                                    <option value="Hòn Tài, Hòn Trác">9. Hòn Tài, Hòn Trác (#Hòn_đảo_ẩn_giấu)</option>
                                    <option value="Bảo tàng Côn Đảo">10. Bảo tàng Côn Đảo (#Lưu_giữ_hiện_vật)</option>
                                    <option value="Nhà tù Côn Đảo (Trại Phú Hải, Phú Sơn)">11. Nhà tù Côn Đảo (Trại Phú Hải, Phú Sơn) (#Di_tích_quốc_gia)</option>
                                    <option value="Dinh Chúa Đảo">12. Dinh Chúa Đảo (#Kiến_trúc_Pháp_cổ)</option>
                                    <option value="Trung Tâm Bảo Tồn Di Tích Quốc Gia">13. Trung Tâm Bảo Tồn Di Tích Quốc Gia (#Đường_Nguyễn_Huệ)</option>
                                    <option value="Cầu tàu 914">14. Cầu tàu 914 (#Chứng_nhân_lịch_sử)</option>
                                    <option value="Mũi Cá Mập">15. Mũi Cá Mập (#Tọa_độ_lý_tưởng)</option>
                                    <option value="Nghĩa trang Hàng Dương">16. Nghĩa trang Hàng Dương (#Tâm_linh_thiêng_liêng)</option>
                                    <option value="Miếu Cậu (Thiếu Gia Miếu)">17. Miếu Cậu (Thiếu Gia Miếu) (#Hoàng_tử_Cải)</option>
                                    <option value="Miếu Năm Cô (Miếu Ngũ Hành)">18. Miếu Năm Cô (Miếu Ngũ Hành) (#Thờ_Ngũ_Hành)</option>
                                    <option value="Chùa Núi Một (Vân Sơn Tự)">19. Chùa Núi Một (Vân Sơn Tự) (#Tựa_sơn_hướng_thủy)</option>
                                    <option value="Cua mặt trăng">20. Cua mặt trăng (#Đặc_sản_quý_hiếm)</option>
                                    <option value="Mứt hạt bàng">21. Mứt hạt bàng (#Quà_tặng_Côn_Đảo)</option>
                                    <option value="Tàu cao tốc từ Cảng Cầu Đá Vũng Tàu">22. Tàu từ bến cảng Vũng Tàu (#Di_chuyển_ra_đảo)</option>
                                    <option value="Tàu cao tốc từ Cảng Trần Đề">23. Tàu từ bến cảng Trần Đề (#Di_chuyển_ra_đảo)</option>
                                    <option value="Tàu cao tốc về Vũng Tàu (Cảng Bến Đầm)">24. Lên tàu về đất liền - Vũng Tàu (#Quay_về_đất_liền)</option>
                                    <option value="Tàu cao tốc về Trần Đề (Cảng Bến Đầm)">25. Lên tàu về đất liền - Trần Đề (#Quay_về_đất_liền)</option>
                                </select>"""
    
    content = content.replace(dropdown_target, dropdown_replacement)

    # 2. Add suggested time buttons
    time_target = """                                <div class="flex flex-wrap gap-2">
                                    <button type="button" onclick="fillSuggestedTime('07:30 - 08:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">07:30 - 08:30 (Ăn sáng)</button>
                                    <button type="button" onclick="fillSuggestedTime('08:30 - 11:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">08:30 - 11:30 (Tham quan sáng)</button>
                                    <button type="button" onclick="fillSuggestedTime('11:30 - 13:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">11:30 - 13:30 (Trưa/Bè nổi)</button>
                                    <button type="button" onclick="fillSuggestedTime('14:30 - 17:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">14:30 - 17:30 (Chiều mát/Tắm biển)</button>
                                    <button type="button" onclick="fillSuggestedTime('18:30 - 21:00')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">18:30 - 21:00 (Ăn tối)</button>
                                    <button type="button" onclick="fillSuggestedTime('21:30 - 23:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">21:30 - 23:30 (Viếng đêm linh thiêng)</button>
                                </div>"""

    time_replacement = """                                <div class="flex flex-wrap gap-2">
                                    <button type="button" onclick="fillSuggestedTime('07:30 - 08:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">07:30 - 08:30 (Ăn sáng)</button>
                                    <button type="button" onclick="fillSuggestedTime('08:00 - 12:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">08:00 - 12:30 (Đi Tàu ra đảo)</button>
                                    <button type="button" onclick="fillSuggestedTime('08:30 - 11:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">08:30 - 11:30 (Tham quan sáng)</button>
                                    <button type="button" onclick="fillSuggestedTime('11:30 - 13:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">11:30 - 13:30 (Trưa/Bè nổi)</button>
                                    <button type="button" onclick="fillSuggestedTime('13:00 - 17:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">13:00 - 17:30 (Lên Tàu về đất liền)</button>
                                    <button type="button" onclick="fillSuggestedTime('14:30 - 17:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">14:30 - 17:30 (Chiều mát/Tắm biển)</button>
                                    <button type="button" onclick="fillSuggestedTime('18:30 - 21:00')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">18:30 - 21:00 (Ăn tối)</button>
                                    <button type="button" onclick="fillSuggestedTime('21:30 - 23:30')" class="bg-white hover:bg-teal-50 text-gray-600 hover:text-teal-700 border border-gray-200 hover:border-teal-200 text-xs font-semibold px-3 py-1.5 rounded-full transition-all shadow-sm">21:30 - 23:30 (Viếng đêm linh thiêng)</button>
                                </div>"""

    content = content.replace(time_target, time_replacement)

    # 3. Add boat items into destMeta
    destmeta_target = """const destMeta = {
    "Vịnh Đầm Tre": { icon: "fa-water", badge: "#Mùa_rong_mơ", color: "bg-teal-50 text-teal-700 border-teal-100" },"""

    destmeta_replacement = """const destMeta = {
    "Tàu cao tốc từ Cảng Cầu Đá Vũng Tàu": { icon: "fa-ship", badge: "#Vũng_Tàu_Ra_Đảo", color: "bg-blue-50 text-blue-700 border-blue-100" },
    "Tàu cao tốc từ Cảng Trần Đề": { icon: "fa-ship", badge: "#Trần_Đề_Ra_Đảo", color: "bg-blue-50 text-blue-700 border-blue-100" },
    "Tàu cao tốc về Vũng Tàu (Cảng Bến Đầm)": { icon: "fa-ship", badge: "#Về_Vũng_Tàu", color: "bg-cyan-50 text-cyan-700 border-cyan-100" },
    "Tàu cao tốc về Trần Đề (Cảng Bến Đầm)": { icon: "fa-ship", badge: "#Về_Trần_Đề", color: "bg-cyan-50 text-cyan-700 border-cyan-100" },
    "Vịnh Đầm Tre": { icon: "fa-water", badge: "#Mùa_rong_mơ", color: "bg-teal-50 text-teal-700 border-teal-100" },"""

    content = content.replace(destmeta_target, destmeta_replacement)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success condao.html!")

# Duplicate destMeta Con Dao block that was in dalat, vungtau, vinhhy and throws SyntaxError
CONDAO_DESTMETA_BLOCK = """// Destination metadata for beautiful visual presentation in the scheduler
const destMeta = {
    "Vịnh Đầm Tre": { icon: "fa-water", badge: "#Mùa_rong_mơ", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bãi Đầm Trầu": { icon: "fa-umbrella-beach", badge: "#Bãi_tắm_đẹp", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bãi Nhát": { icon: "fa-umbrella-beach", badge: "#Phong_cảnh_hữu_tình", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bãi Suối Nóng": { icon: "fa-umbrella-beach", badge: "#Hoang_sơ_hiếm_có", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bãi Đá Cuội": { icon: "fa-umbrella-beach", badge: "#Khu_Bến_Đầm", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Hòn Bảy Cạnh": { icon: "fa-water", badge: "#Bảo_tồn_rùa", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Hòn Cau & Miếu Cô Vân": { icon: "fa-person-surfing", badge: "#Hòn_Cau", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bãi Đất Thắm": { icon: "fa-shoe-prints", badge: "#Private_Beach", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Hòn Tài, Hòn Trác": { icon: "fa-ship", badge: "#Hòn_đảo_ẩn_giấu", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Bảo tàng Côn Đảo": { icon: "fa-landmark", badge: "#Lưu_giữ_hiện_vật", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Nhà tù Côn Đảo (Trại Phú Hải, Phú Sơn)": { icon: "fa-building", badge: "#Di_tích_quốc_gia", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Dinh Chúa Đảo": { icon: "fa-landmark", badge: "#Kiến_trúc_Pháp_cổ", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Trung Tâm Bảo Tồn Di Tích Quốc Gia": { icon: "fa-landmark", badge: "#Đường_Nguyễn_Huệ", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Cầu tàu 914": { icon: "fa-landmark", badge: "#Chứng_nhân_lịch_sử", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Mũi Cá Mập": { icon: "fa-mountain-sun", badge: "#Tọa_độ_lý_tưởng", color: "bg-gray-100 text-gray-700 border-gray-200" },
    "Nghĩa trang Hàng Dương": { icon: "fa-place-of-worship", badge: "#Tâm_linh_thiêng_liêng", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Miếu Cậu (Thiếu Gia Miếu)": { icon: "fa-gopuran", badge: "#Hoàng_tử_Cải", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Miếu Năm Cô (Miếu Ngũ Hành)": { icon: "fa-scroll", badge: "#Thờ_Ngũ_Hành", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Chùa Núi Một (Vân Sơn Tự)": { icon: "fa-gopuran", badge: "#Tựa_sơn_hướng_thủy", color: "bg-teal-50 text-teal-700 border-teal-100" },
    "Cua mặt trăng": { icon: "fa-shrimp", badge: "#Đặc_sản_quý_hiếm", color: "bg-orange-50 text-orange-700 border-orange-100" },
    "Mứt hạt bàng": { icon: "fa-cookie", badge: "#Quà_tặng_Côn_Đảo", color: "bg-orange-50 text-orange-700 border-orange-100" }
};"""

dalat_preset_timeline = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-hotel"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Lên Thành Phố Sương Mù & Nhịp Sống Đêm</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 11:30</div>
                                <div>Di chuyển lên <strong>Đà Lạt</strong> bằng xe khách giường nằm cao cấp từ TP.HCM qua những đồi dốc quanh co ngắm cảnh núi non rừng thông.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Ăn trưa nhẹ nhàng tại quán bánh căn giòn nóng hổi trung tâm thành phố.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">13:30 - 14:30</div>
                                <div>Về nhận phòng tại <strong>Hotel Colline</strong> ngay cạnh chợ Đà Lạt, sắp xếp đồ đạc và nghỉ ngơi sau hành trình dài.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Dạo mát quanh <strong>Hồ Xuân Hương</strong>, chụp ảnh check-in nụ hoa Atiso khổng lồ tại Quảng trường Lâm Viên.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 20:00</div>
                                <div>Thưởng thức món đặc sản <strong>Lẩu Gà Lá É Tao Ngộ</strong> nóng hổi, vị ngọt thanh của gà đồi quyện cùng lá é the mát cực kỳ hợp với khí lạnh Đà Lạt.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">20:30 - 22:30</div>
                                <div>Khám phá <strong>Chợ Đêm Đà Lạt</strong>, thưởng thức khoai nướng, sữa đậu nành nóng và bánh tráng nướng lừng danh.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-mountain"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Săn Mây Langbiang & Chiều Hoàng Hôn Tuyền Lâm</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">05:00 - 08:30</div>
                                <div>Dậy sớm đón bình minh, đi xe Jeep băng qua rừng thông lên đỉnh <strong>Langbiang</strong> huyền thoại để săn mây bồng bềnh và ngắm toàn cảnh hồ Đan Kia dưới làn sương.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 10:00</div>
                                <div>Dùng bữa sáng bánh mì xíu mại chén thơm ngon cùng ly cà phê phin đậm đà.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:30</div>
                                <div>Ăn trưa cơm lam thịt nướng ống tre đặc sản Tây Nguyên tại quán ăn bản địa.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Đến <strong>Hồ Tuyền Lâm</strong>, chèo SUP đón hoàng hôn tuyệt đẹp buông xuống thung lũng thông xanh phẳng lặng như gương.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Dùng bữa tối nướng ngói thơm lừng lộng gió lạnh Đà Lạt.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-camera"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Di Sản Cổ Kính & Bản Tình Ca Quán Cà Phê</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:30</div>
                                <div>Ghé thăm <strong>Ga Đà Lạt</strong> cổ kính phong cách Pháp, trải nghiệm chụp ảnh check-in đầu máy xe lửa hơi nước xưa.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">11:00 - 12:30</div>
                                <div>Viếng thăm <strong>Chùa Linh Phước</strong> (chùa Ve Chai) với kiến trúc khảm sành sứ rực rỡ ấn tượng.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">13:00 - 14:30</div>
                                <div>Ăn trưa cơm niêu thuần Việt ấm cúng tại quán cơm niêu Như Ngọc.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Chill nhẹ nhàng thư giãn tại các quán cà phê ngắm cảnh thung lũng đồi thông lộng gió lãng mạn.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Ăn tối lẩu bò Ba Toa nức tiếng, súp lẩu béo ngậy thơm ngon ngọt thịt.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-basket-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Hương Vị Đà Lạt & Lưu Luyến Trở Về</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 08:30</div>
                                <div>Ăn sáng bún riêu, dùng trà nóng ngắm sương mù nhẹ trôi ven đồi.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 11:00</div>
                                <div>Ghé <strong>Chợ Đà Lạt</strong> mua hồng sấy, mứt dâu tây dâu tằm, trà atiso và bông hoa tươi về làm quà tặng ý nghĩa.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">11:30 - 12:30</div>
                                <div>Trở lại <strong>Hotel Colline</strong> check-out trả phòng, dùng bữa trưa nhẹ và sắp xếp hành lý lên xe khách, tạm biệt thành phố ngàn hoa thơ mộng.</div>
                            </li>
                        </ul>
                    </div>"""

dalat_template = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "dl1", time: "13:30 - 14:30", dest: "Đỉnh Langbiang", note: "Xe trung chuyển đón về khách sạn nhận phòng" },
                { id: "dl2", time: "15:00 - 17:30", dest: "Hồ Tuyền Lâm", note: "Dạo quanh Hồ Xuân Hương và ngắm hoàng hôn Đà Lạt" },
                { id: "dl3", time: "18:30 - 20:00", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Thưởng thức nồi lẩu gà lá é ấm nồng đặc trưng" },
                { id: "dl4", time: "20:30 - 22:30", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Dạo tham quan Chợ đêm Đà Lạt lộng gió" }
            ],
            day2: [
                { id: "dl5", time: "05:00 - 08:30", dest: "Đỉnh Langbiang", note: "Đi xe Jeep lên đỉnh Langbiang săn mây buổi sáng sớm" },
                { id: "dl6", time: "15:00 - 17:30", dest: "Hồ Tuyền Lâm", note: "Chèo SUP ngắm hoàng hôn lãng mạn trên mặt hồ phẳng lặng" }
            ],
            day3: [
                { id: "dl7", time: "08:30 - 11:30", dest: "Hồ Tuyền Lâm", note: "Ghé thăm Thiền Viện Trúc Lâm và đi cáp treo đồi Robin" },
                { id: "dl8", time: "15:00 - 17:00", dest: "Đỉnh Langbiang", note: "Ghé các quán cà phê ngắm cảnh sương mù thung lũng thông reo" }
            ],
            day4: [
                { id: "dl9", time: "09:00 - 11:00", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Đi chợ Đà Lạt mua đặc sản mứt hồng sấy dẻo và hoa tươi" },
                { id: "dl10", time: "12:00 - 12:30", dest: "Hotel Colline", note: "Check-out trả phòng khách sạn, kết thúc chuyến đi" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

dalat_tab3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-plane-departure mr-2"></i> Kênh Di Chuyển Lên Lâm Đồng</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-2"><i class="fa-solid fa-plane text-teal-600 mr-2"></i> Bằng Máy Bay</h4>
                        <p class="text-gray-600 text-sm mb-2">Sân bay Liên Khương cách trung tâm Đà Lạt khoảng 30km, kết nối trực tiếp với các hãng hàng không lớn.</p>
                        <ul class="list-disc pl-5 text-gray-600 text-sm space-y-1">
                            <li><strong>Từ TP.HCM / Hà Nội / Đà Nẵng:</strong> Vé bay từ 900.000đ - 2.500.000đ/lượt.</li>
                            <li><strong>Xe Bus Sân Bay về phố:</strong> Khoảng 40.000 VNĐ/lượt hoặc đi taxi trọn gói khoảng 250.000 VNĐ.</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-3"><i class="fa-solid fa-bus text-teal-600 mr-2"></i> Bằng Xe Khách Limousine</h4>
                        <p class="text-gray-600 text-sm mb-4">Các dòng xe limousine giường nằm chất lượng cao đem lại hành trình thoải mái xuyên suốt ngày đêm:</p>

                        <div class="space-y-4">
                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-bus text-teal-600"></i> Hãng xe Thành Bưởi & Phương Trang</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 6 - 7 tiếng</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Tần suất chạy liên tục mỗi 30 - 60 phút từ TP.HCM, dòng xe phòng nằm cabin Vip sang trọng riêng tư.</p>
                                <div class="bg-white p-3 rounded-lg border border-gray-100 text-sm">
                                    <p class="font-semibold text-teal-700 mb-1 border-b pb-1">Bảng giá tham khảo:</p>
                                    <ul class="space-y-1.5 text-gray-600 mt-2">
                                        <li class="flex justify-between"><span>Giường nằm tiêu chuẩn:</span> <span class="font-bold text-gray-800">270.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Phòng nằm VIP Cabin:</span> <span class="font-bold text-gray-800">380.000 - 450.000 VNĐ</span></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="mt-4 bg-amber-50/80 border border-amber-100 p-4 rounded-xl flex gap-3 shadow-xs">
                                <div class="text-amber-500 text-lg shrink-0 mt-0.5"><i class="fa-solid fa-lightbulb"></i></div>
                                <div>
                                    <h6 class="font-bold text-amber-800 text-sm">Lưu ý khi đi Đà Lạt</h6>
                                    <p class="text-amber-900/80 text-xs mt-1 leading-relaxed">Nên chuẩn bị sẵn áo khoác ấm vì nhiệt độ ban đêm có thể giảm rất sâu (khoảng 14 - 16 độ C). Lên lịch đặt vé trước 1 - 2 tuần cho cuối tuần cao điểm.</p>
                                </div>
                            </div>
                        </div>
                    </div>"""

vungtau_preset_timeline = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-hotel"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Hải Trình Vượt Biển & Chinh Phục Núi Nhỏ</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:00</div>
                                <div>Trải nghiệm di chuyển bằng <strong>Tàu cánh ngầm Greenlines DP</strong> xuất phát từ Bến Bạch Đằng lướt sóng ra Vũng Tàu thơ mộng.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">10:30 - 11:30</div>
                                <div>Thưởng thức bữa trưa đặc sản <strong>Bánh Khọt Gốc Vú Sữa</strong> giòn rụm với tôm to cuộn rau sống chấm nước mắm tuyệt hảo.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Nhận phòng khách sạn 5 sao mang phong cách Phục Hưng <strong>The Imperial Hotel Vũng Tàu</strong> ngay sát Bãi Sau để nghỉ ngơi.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Tắm bơi lội mát rượi tại Bãi Sau hoặc bể bơi vô cực khách sạn đón sóng vỗ rì rào.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:00 - 19:30</div>
                                <div>Chinh phục 800+ bậc thang lên núi Nhỏ viếng <strong>Tượng Chúa Dang Tay</strong> ngắm biển trời lộng gió lúc chiều muộn yên bình.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-lightbulb"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Dinh Thự Cổ Kính & Hoàng Hôn Ngọn Hải Đăng</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:30</div>
                                <div>Ghé tham quan khu dinh thự cổ thời Pháp <strong>Bạch Dinh</strong>, chụp hình cây hoa sứ trắng trăm năm tuổi view vịnh Bãi Trước.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Lượn xe máy theo cung đường dốc núi rợp bóng hoa giấy lên <strong>Ngọn Hải Đăng Vũng Tàu</strong> ngắm hoàng hôn, ăn sữa chua Yaourt Cô Tiên nổi tiếng dưới chân núi.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Thưởng thức hải sản tươi sống ngắm sóng vỗ tuyệt đẹp tại nhà hàng Gành Hào.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-umbrella-beach"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Khu Vui Chơi Hồ Mây & Check-in Cổng Trời Nghinh Phong</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:30 - 12:00</div>
                                <div>Đi cáp treo lên đỉnh núi Tương Kỳ vui chơi trọn gói tại khu du lịch sinh thái <strong>Hồ Mây Park</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Khám phá <strong>Mũi Nghinh Phong</strong> lộng gió đón sóng vỗ, check-in cổng trời và ngắm nhìn đảo nhỏ Hòn Bà cô độc nổi trên biển.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-basket-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Tắm Biển Sáng & Thưởng Thức Quà Chiều</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 09:30</div>
                                <div>Dùng bữa sáng nhẹ, thỏa sức tắm mát đón bình minh Bãi Sau.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">10:00 - 11:30</div>
                                <div>Ghé sạp hàng mua bánh bông lan trứng muối Gốc Cột Điện lừng danh làm quà lưu niệm.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Trả phòng khách sạn <strong>The Imperial</strong>, chuẩn bị hành lý đón xe limousine hoặc tàu cao tốc về đất liền, khép lại kỳ nghỉ lãng mạn.</div>
                            </li>
                        </ul>
                    </div>"""

vungtau_template = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "vt1", time: "08:00 - 10:00", dest: "Tượng Chúa Dang Tay", note: "Di chuyển bằng tàu cao tốc Greenlines DP đến Vũng Tàu" },
                { id: "vt2", time: "10:30 - 11:30", dest: "Bánh Khọt Gốc Vú Sữa", note: "Ăn trưa đặc sản bánh khọt nổi tiếng nóng hổi" },
                { id: "vt3", time: "12:00 - 13:00", dest: "The Imperial Hotel Vũng Tàu", note: "Check-in khách sạn, nhận phòng và sắp xếp hành lý" },
                { id: "vt4", time: "15:00 - 17:30", dest: "Tượng Chúa Dang Tay", note: "Chinh phục Tượng Chúa Kitô Vua đón gió lộng ngắm toàn cảnh" }
            ],
            day2: [
                { id: "vt5", time: "08:30 - 11:00", dest: "Ngọn Hải Đăng Vũng Tàu", note: "Khám phá Bạch Dinh phong cách Pháp cổ kính" },
                { id: "vt6", time: "15:30 - 17:30", dest: "Ngọn Hải Đăng Vũng Tàu", note: "Ngắm hoàng hôn rực rỡ và ăn sữa chua Yaourt Cô Tiên" }
            ],
            day3: [
                { id: "vt7", time: "08:30 - 11:30", dest: "Tượng Chúa Dang Tay", note: "Vui chơi khu sinh thái Hồ Mây Park" },
                { id: "vt8", time: "15:00 - 17:30", dest: "Tượng Chúa Dang Tay", note: "Khám phá Mũi Nghinh Phong chụp ảnh đón sóng biển rì rào" }
            ],
            day4: [
                { id: "vt9", time: "09:00 - 10:30", dest: "Bánh Khọt Gốc Vú Sữa", note: "Mua bánh bông lan trứng muối Gốc Cột Điện làm quà lưu niệm" },
                { id: "vt10", time: "12:00 - 12:30", dest: "The Imperial Hotel Vũng Tàu", note: "Làm thủ tục trả phòng khách sạn kết thúc chuyến đi" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

vungtau_tab3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-plane-departure mr-2"></i> Kênh Di Chuyển Ra Vũng Tàu</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-2"><i class="fa-solid fa-ferry text-teal-600 mr-2"></i> Bằng Tàu Cao Tốc (Tàu Cánh Ngầm)</h4>
                        <p class="text-gray-600 text-sm mb-2">Rất nhanh gọn và thoáng đãng từ TP.HCM (Bến Bạch Đằng) sang Cảng Cầu Đá Vũng Tàu.</p>
                        <ul class="list-disc pl-5 text-gray-600 text-sm space-y-1">
                            <li><strong>Hãng tàu Greenlines DP:</strong> Thời gian di chuyển khoảng 2 tiếng lướt sóng êm ái.</li>
                            <li><strong>Bảng giá vé tham khảo:</strong> Khoảng 280.000đ (thứ 2 - thứ 5) và 320.000đ (thứ 6 - chủ nhật).</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-3"><i class="fa-solid fa-car-side text-teal-600 mr-2"></i> Bằng Xe Limousine / Ô tô</h4>
                        <p class="text-gray-600 text-sm mb-4">Các hãng xe limousine đưa đón tận nơi chạy liên tục với tần suất 15 phút/chuyến:</p>

                        <div class="space-y-4">
                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-car text-teal-600"></i> Hãng xe Hoa Mai / Toàn Thắng / Anh Quốc</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 2 tiếng qua cao tốc</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Xe limousine 9 chỗ ghế mát-xa rộng rãi, đưa đón khách tận nhà hoặc các điểm hẹn trung tâm.</p>
                                <div class="bg-white p-3 rounded-lg border border-gray-100 text-sm">
                                    <p class="font-semibold text-teal-700 mb-1 border-b pb-1">Bảng giá tham khảo:</p>
                                    <ul class="space-y-1.5 text-gray-600 mt-2">
                                        <li class="flex justify-between"><span>Vé ghế thường Limousine:</span> <span class="font-bold text-gray-800">170.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Vé ghế VIP mát-xa:</span> <span class="font-bold text-gray-800">200.000 VNĐ</span></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="mt-4 bg-amber-50/80 border border-amber-100 p-4 rounded-xl flex gap-3 shadow-xs">
                                <div class="text-amber-500 text-lg shrink-0 mt-0.5"><i class="fa-solid fa-lightbulb"></i></div>
                                <div>
                                    <h6 class="font-bold text-amber-800 text-sm">Lưu ý khi du lịch Vũng Tàu</h6>
                                    <p class="text-amber-900/80 text-xs mt-1 leading-relaxed">Vũng Tàu thường rất đông vào cuối tuần, khiến giá dịch vụ phòng và hải sản có thể tăng nhẹ. Nên ưu tiên đặt trước và di chuyển sớm để tránh kẹt xe.</p>
                                </div>
                            </div>
                        </div>
                    </div>"""

vinhhy_preset_timeline = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-hotel"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Vượt Cung Đường Vịnh Biển & Thưởng Ngoạn Vịnh Vĩnh Hy</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 11:00</div>
                                <div>Đón xe dịch vụ từ Sân bay Cam Ranh chạy men theo cung đường đèo ven biển Bình Tiên ngắm đại dương bao la để tới Vĩnh Hy.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Nhận phòng nghỉ ngơi tại <strong>Amanoi Resort</strong> hoặc các khu resort/homestay rợp bóng cây xanh sát vịnh.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">14:00 - 17:30</div>
                                <div>Đi tàu đáy kính tham quan Vịnh <strong>Vĩnh Hy</strong>, thỏa thích bơi lội, lặn biển ngắm rạn san hô sinh động.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Dùng bữa tối hải sản phong phú tươi ngon trên bè nổi cảng Vĩnh Hy lộng gió biển.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-sun"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Săn Bình Minh Hang Rái & Hải Sản Đảo Bình Hưng</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">05:00 - 08:30</div>
                                <div>Dậy sớm đón bình minh tuyệt đỉnh trên thềm san hô cổ hóa thạch Hang Rái, chiêm ngưỡng hiện tượng thác nước trên biển kỳ thú.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:30 - 15:00</div>
                                <div>Đi tàu sang <strong>Đảo Bình Hưng</strong>, thuê xe điện dạo quanh ngắm cảnh, thưởng thức bữa trưa **Tôm hùm Bình Hưng** trứ danh nức tiếng.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Về đất liền, ăn tối thư thái và nhâm nhi cafe đón gió tối trong lành.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-person-hiking"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Trekking Rừng Quốc Gia Núi Chúa & Bãi Nước Ngọt</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 11:30</div>
                                <div>Trekking nhẹ nhàng xuyên qua rừng khô hạn Núi Chúa, vãn cảnh dòng <strong>Suối Lồ Ồ</strong> trong vắt mát lạnh, ngắm cầu treo gỗ dân dã.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">14:00 - 17:30</div>
                                <div>Tắm bơi bãi hoang sơ Bãi Nước Ngọt với dòng suối mát chảy trực tiếp ra vịnh cát trắng mịn màng thơ mộng.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-basket-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Chợ Hải Sản Vịnh Biển & Trở Về</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 09:30</div>
                                <div>Dạo chợ hải sản buổi sáng sớm để chọn mua khô mực, nước mắm nhĩ, hành tỏi Phan Rang làm quà.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Làm thủ tục check-out trả phòng tại <strong>Amanoi</strong>, thu xếp hành lý dịch vụ xe tiễn ra Sân bay Cam Ranh đón chuyến bay về.</div>
                            </li>
                        </ul>
                    </div>"""

vinhhy_template = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "vh1", time: "11:00 - 12:30", dest: "Amanoi Resort", note: "Di chuyển bằng xe taxi về vịnh Vĩnh Hy tuyệt đẹp" },
                { id: "vh2", time: "13:00 - 14:00", dest: "Amanoi Resort", note: "Check-in resort cao cấp ẩn mình bên đồi thông" },
                { id: "vh3", time: "15:00 - 17:30", dest: "Đảo Bình Hưng", note: "Đi cano khám phá rạn san hô vịnh Vĩnh Hy màu sắc" }
            ],
            day2: [
                { id: "vh4", time: "05:00 - 08:00", dest: "Hang Rái", note: "Đón bình minh tuyệt đỉnh trên đá san hô cổ Hang Rái" },
                { id: "vh5", time: "09:30 - 15:00", dest: "Đảo Bình Hưng", note: "Ăn tôm hùm tại bè nổi đảo Bình Hưng, đi xe điện dạo quanh" }
            ],
            day3: [
                { id: "vh6", time: "08:30 - 11:30", dest: "Hang Rái", note: "Trekking nhẹ nhàng ngắm dòng Suối Lồ Ồ" },
                { id: "vh7", time: "14:30 - 17:00", dest: "Đảo Bình Hưng", note: "Thư giãn tắm bơi tự do bãi cát trắng ngần" }
            ],
            day4: [
                { id: "vh8", time: "09:00 - 10:30", dest: "Tôm hùm Bình Hưng", note: "Mua khô mực nước mắm tỏi Phan Rang làm quà" },
                { id: "vh9", time: "12:00 - 12:30", dest: "Amanoi Resort", note: "Trả phòng khách sạn, tiễn khách ra sân bay Cam Ranh" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

vinhhy_tab3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-plane-departure mr-2"></i> Kênh Di Chuyển Đến Vịnh Vĩnh Hy</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-2"><i class="fa-solid fa-plane text-teal-600 mr-2"></i> Bằng Máy Bay (Đến Cam Ranh)</h4>
                        <p class="text-gray-600 text-sm mb-2">Đến Sân bay Cam Ranh (Khánh Hòa) là hành trình nhanh nhất, sau đó đi xe dịch vụ ven biển vào Vịnh.</p>
                        <ul class="list-disc pl-5 text-gray-600 text-sm space-y-1">
                            <li><strong>Quãng đường:</strong> Sân bay Cam Ranh - Vĩnh Hy khoảng 60km, đi qua cung đèo vịnh biển tuyệt tác Ninh Thuận.</li>
                            <li><strong>Phương tiện trung chuyển:</strong> Giá taxi trọn gói dao động từ 600.000đ - 700.000đ/lượt.</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-3"><i class="fa-solid fa-train text-teal-600 mr-2"></i> Bằng Tàu Hỏa / Xe Khách (Đến Phan Rang)</h4>
                        <p class="text-gray-600 text-sm mb-4">Lựa chọn tàu hỏa ngắm cảnh hoặc xe giường nằm đến TP Phan Rang Tháp Chàm rồi di chuyển vào vịnh:</p>

                        <div class="space-y-4">
                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-train text-teal-600"></i> Ga Tháp Chàm hoặc Bến xe Phan Rang</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 40km vào vịnh</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Có thể di chuyển bằng xe bus công cộng Phan Rang - Vĩnh Hy (~20.000đ) hoặc bắt taxi vào vịnh khoảng 350.000đ.</p>
                            </div>

                            <div class="mt-4 bg-amber-50/80 border border-amber-100 p-4 rounded-xl flex gap-3 shadow-xs">
                                <div class="text-amber-500 text-lg shrink-0 mt-0.5"><i class="fa-solid fa-lightbulb"></i></div>
                                <div>
                                    <h6 class="font-bold text-amber-800 text-sm">Lưu ý khi đi Vĩnh Hy</h6>
                                    <p class="text-amber-900/80 text-xs mt-1 leading-relaxed">Đoạn đường ven biển rất nhiều cua dốc uốn lượn, nếu tự đi bằng xe máy cần hết sức cẩn thận. Thời điểm biển đẹp nhất là từ tháng 3 đến tháng 9 âm lịch.</p>
                                </div>
                            </div>
                        </div>
                    </div>"""

def process_subpage(filename, prefix, name_vietnamese):
    path = rf"d:\VSCode\Some_stuff_case\condao\{filename}"
    print(f"Processing subpage: {filename}...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Decouple KEYS keys
    content = content.replace("condao_admin_destinations", f"{prefix}_admin_destinations")
    content = content.replace("condao_admin_hotels", f"{prefix}_admin_hotels")
    content = content.replace("condao_admin_food", f"{prefix}_admin_food")
    content = content.replace("condao_memories", f"{prefix}_memories")
    content = content.replace("condao_memory_pass", f"{prefix}_memory_pass")
    content = content.replace("condao_github_token", f"{prefix}_github_token")
    content = content.replace("condao_github_config", f"{prefix}_github_config")
    
    # 2. Decouple custom plan and initialize check keys
    content = content.replace("condao_db_initialized", f"{prefix}_db_initialized")
    content = content.replace("condao_custom_plan", f"{prefix}_custom_plan")

    # 3. Remove duplicate Con Dao destMeta block
    content = content.replace(CONDAO_DESTMETA_BLOCK, "")

    # 4. Inject populatePlannerDestinations in DOMContentLoaded
    dom_target = """  loadPlanFromStorage();
  renderCustomTimeline();"""
    dom_replacement = """  populatePlannerDestinations();
  loadPlanFromStorage();
  renderCustomTimeline();"""
    content = content.replace(dom_target, dom_replacement)

    # 5. Inject populatePlannerDestinations() function
    func_target = """function loadPlanFromStorage() {"""
    func_replacement = """function populatePlannerDestinations() {
    const destSelect = document.getElementById('planner-dest-select');
    if (!destSelect) return;
    destSelect.innerHTML = "";
    const adminDests = loadData(KEYS.adminDests);
    const allDests = [...adminDests, ...DEFAULT_DESTINATIONS];
    const seen = new Set();
    allDests.forEach((d, idx) => {
        if (!seen.has(d.name)) {
            seen.add(d.name);
            const opt = document.createElement('option');
            opt.value = d.name;
            opt.textContent = `${idx + 1}. ${d.name} (${d.tags && d.tags.length ? '#' + d.tags[0] : '#Điểm_đến'})`;
            destSelect.appendChild(opt);
        }
    });
}

function loadPlanFromStorage() {"""
    content = content.replace(func_target, func_replacement)

    # 6. Global String replacements to clear "Côn Đảo" leftovers
    content = content.replace("Khám Phá Côn Đảo", f"Khám Phá {name_vietnamese}")
    content = content.replace("danh thắng Côn Đảo", f"danh thắng {name_vietnamese}")
    content = content.replace("địa điểm đẹp nhất Côn Đảo", f"địa điểm đẹp nhất {name_vietnamese}")
    content = content.replace("Cẩm Nang Ẩm Thực & Cà Phê Côn Đảo", f"Cẩm Nang Ẩm Thực & Cà Phê {name_vietnamese}")
    content = content.replace("Quán Ngon Côn Đảo", f"Quán Ngon {name_vietnamese}")
    content = content.replace("chuyến hành trình Côn Đảo", f"chuyến hành trình {name_vietnamese}")
    content = content.replace("Admin Dashboard — Côn Đảo", f"Admin Dashboard — {name_vietnamese}")
    content = content.replace("hành trình khám phá Côn Đảo", f"hành trình khám phá {name_vietnamese}")
    content = content.replace("for Côn Đảo", f"for {name_vietnamese}")
    content = content.replace("LỊCH TRÌNH DU LỊCH CÔN ĐẢO CỦA BẠN", f"LỊCH TRÌNH DU LỊCH {name_vietnamese.upper()} CỦA BẠN")
    content = content.replace("Ngày đầu tiên ở Côn Đảo", f"Ngày đầu tiên ở {name_vietnamese}")

    # 7. Apply TIMELINE & TEMPLATE & TAB3 replacements ATOMICALLY here!
    start_timeline = content.find('<div class="timeline-container space-y-2">')
    end_timeline = content.find('<!-- 2. Custom Planner View -->')
    
    if start_timeline != -1 and end_timeline != -1:
        prefix_html = content[:start_timeline + len('<div class="timeline-container space-y-2">\n                    ')]
        suffix_html = content[end_timeline:]
        
        timeline_content = ""
        template_content = ""
        tab3_content = ""
        
        if prefix == "dalat":
            timeline_content = dalat_preset_timeline
            template_content = dalat_template
            tab3_content = dalat_tab3
        elif prefix == "vungtau":
            timeline_content = vungtau_preset_timeline
            template_content = vungtau_template
            tab3_content = vungtau_tab3
        elif prefix == "vinhhy":
            timeline_content = vinhhy_preset_timeline
            template_content = vinhhy_template
            tab3_content = vinhhy_tab3
            
        # Perform replacements on content!
        content = prefix_html + timeline_content + "\n                    </div>\n                </div>\n                </div>\n\n" + suffix_html
        print(f"  Replaced preset timeline in {filename}!")
        
        # Replace default template
        content = re.sub(r"function loadDefaultTemplate\(\) \{[\s\S]+?\}", template_content, content, count=1)
        print(f"  Replaced default template in {filename}!")
        
        # Replace tab3 channel
        tab3_target = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-ship mr-2"></i> Kênh Di Chuyển Ra Đảo</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-2"><i class="fa-solid fa-plane text-teal-600 mr-2"></i> Bằng Máy Bay</h4>
                        <p class="text-gray-600 text-sm mb-2">Đường bay thẳng được khai thác bởi Vietnam Airlines, Vietjet Airs và Bamboo Airways[cite: 76].</p>
                        <ul class="list-disc pl-5 text-gray-600 text-sm space-y-1">
                            <li><strong>Từ TP.HCM & Cần Thơ:</strong> Thời gian bay khoảng 55 phút[cite: 78]. Giá tham khảo dao động từ 1.200.000đ - 1.800.000đ/chiều.</li>
                            <li><strong>Từ Hà Nội:</strong> Thời gian bay khoảng 3 giờ 30 phút[cite: 79].</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-3"><i class="fa-solid fa-ferry text-teal-600 mr-2"></i> Bằng Tàu Cao Tốc</h4>
                        <p class="text-gray-600 text-sm mb-4">Hiện có các tuyến tàu cao tốc chất lượng cao phục vụ việc di chuyển ra Côn Đảo với mức giá và lịch trình khác nhau:</p>

                        <div class="space-y-4">
                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-anchor text-teal-600"></i> Tuyến Vũng Tàu - Côn Đảo</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 3.5 - 4 tiếng</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Được khai thác chủ yếu bởi hãng Phú Quốc Express (Tàu Thăng Long - Tàu cao tốc lớn nhất Việt Nam). Chịu sóng gió tốt, tiện nghi 5 sao.</p>
                                <div class="bg-white p-3 rounded-lg border border-gray-100 text-sm">
                                    <p class="font-semibold text-teal-700 mb-1 border-b pb-1">Bảng giá tham khảo:</p>
                                    <ul class="space-y-1.5 text-gray-600 mt-2">
                                        <li class="flex justify-between"><span>Vé ECO (Thứ 2 - Thứ 5):</span> <span class="font-bold text-gray-800">790.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Vé ECO (Thứ 6 - CN, Lễ):</span> <span class="font-bold text-gray-800">950.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Trẻ em / Người cao tuổi:</span> <span class="font-bold text-gray-800">630.000đ - 760.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Vé VIP:</span> <span class="font-bold text-orange-600">1.000.000 - 1.100.000 VNĐ</span></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-anchor text-teal-600"></i> Tuyến Trần Đề (Sóc Trăng) - Côn Đảo</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 2 - 2.5 tiếng</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Được khai thác bởi Phú Quốc Express (Côn Đảo Express) và Superdong. Thời gian di chuyển ngắn nhất, phù hợp cho du khách xuất phát từ miền Tây.</p>
                                <div class="bg-white p-3 rounded-lg border border-gray-100 text-sm">
                                    <p class="font-semibold text-teal-700 mb-1 border-b pb-1">Bảng giá tham khảo (Côn Đảo Express):</p>
                                    <ul class="space-y-1.5 text-gray-600 mt-2">
                                        <li class="flex justify-between"><span>Vé ECO (Thứ 2 - Thứ 5):</span> <span class="font-bold text-gray-800">390.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Vé ECO (Thứ 6 - CN, Lễ):</span> <span class="font-bold text-gray-800">450.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Trẻ em / Người cao tuổi:</span> <span class="font-bold text-gray-800">312.000đ - 360.000 VNĐ</span></li>
                                        <li class="flex justify-between"><span>Vé VIP:</span> <span class="font-bold text-orange-600">590.000 VNĐ</span></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="mt-4 bg-amber-50/80 border border-amber-100 p-4 rounded-xl flex gap-3 shadow-xs">
                                <div class="text-amber-500 text-lg shrink-0 mt-0.5"><i class="fa-solid fa-lightbulb"></i></div>
                                <div>
                                    <h6 class="font-bold text-amber-800 text-sm">Lưu ý</h6>
                                    <p class="text-amber-900/80 text-xs mt-1 leading-relaxed">Giá vé có thể thay đổi tùy hãng tàu và chưa bao gồm phí cảng (khoảng 18.000 VNĐ/lượt). Nên mua vé khứ hồi trước 1-2 tuần vào mùa cao điểm để tránh cháy vé.</p>
                                </div>
                            </div>
                        </div>
                    </div>"""
        content = content.replace(tab3_target, tab3_content)
        print(f"  Replaced transport channel in {filename}!")
    else:
        print(f"  WARNING: Timeline boundary elements NOT found in {filename}!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully processed and localized {filename}!")

if __name__ == "__main__":
    process_index()
    process_condao()
    process_subpage("dalat.html", "dalat", "Đà Lạt")
    process_subpage("vungtau.html", "vungtau", "Vũng Tàu")
    process_subpage("vinhhy.html", "vinhhy", "Vĩnh Hy")
    print("ALL STEPS COMPLETED SUCCESSFULLY!")
