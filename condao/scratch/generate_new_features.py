import sys, re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original file: {len(html)} chars, {html.count(chr(10))} lines")

# ============================================================
# PART 1: NEW CSS (insert before </style>)
# ============================================================
NEW_CSS = r"""
/* ===== ADMIN PANEL ===== */
.admin-login-overlay {
    position: fixed; inset: 0; z-index: 10000;
    background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%);
    display: flex; align-items: center; justify-content: center;
}
.admin-panel-container {
    display: grid;
    grid-template-columns: 220px 1fr;
    height: 100%;
    min-height: 0;
}
@media(max-width:768px){ .admin-panel-container { grid-template-columns: 1fr; } }
.admin-sidebar {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    padding: 1.5rem 1rem;
    display: flex; flex-direction: column; gap: 0.375rem;
    overflow-y: auto;
    border-right: 1px solid rgba(255,255,255,0.08);
}
.admin-sidebar-item {
    padding: 0.75rem 1rem; border-radius: 0.75rem; cursor: pointer;
    transition: all 0.2s; display: flex; align-items: center;
    gap: 0.625rem; font-size: 0.8rem; font-weight: 600;
    color: rgba(255,255,255,0.6); border: 1px solid transparent;
}
.admin-sidebar-item:hover { background: rgba(255,255,255,0.07); color: #5eead4; }
.admin-sidebar-item.admin-active {
    background: linear-gradient(135deg, #0d9488, #0f766e);
    color: #fff; border-color: #0d9488;
    box-shadow: 0 4px 12px rgba(13,148,136,0.3);
}
.admin-main { overflow-y: auto; padding: 1.5rem; background: #f8fafc; }
.admin-section { display: none; }
.admin-section.admin-section-visible { display: block; }
.admin-form-label {
    font-size: 0.7rem; font-weight: 700; color: #374151;
    margin-bottom: 0.25rem; display: block; text-transform: uppercase; letter-spacing: 0.05em;
}
.admin-form-input {
    width: 100%; border: 1.5px solid #e2e8f0; border-radius: 0.625rem;
    padding: 0.5rem 0.75rem; font-size: 0.85rem; transition: border-color 0.2s;
    outline: none; background: white; color: #1e293b;
}
.admin-form-input:focus { border-color: #0d9488; box-shadow: 0 0 0 3px rgba(13,148,136,0.12); }
.admin-form-textarea { resize: vertical; min-height: 72px; }
.admin-item-row {
    background: white; border: 1px solid #e2e8f0; border-radius: 0.875rem;
    padding: 0.875rem 1rem; display: flex; gap: 0.875rem;
    align-items: center; transition: all 0.2s; margin-bottom: 0.5rem;
}
.admin-item-row:hover { border-color: #0d9488; box-shadow: 0 2px 8px rgba(13,148,136,0.1); }
.admin-item-thumb {
    width: 56px; height: 56px; border-radius: 0.625rem; object-fit: cover;
    background: #f1f5f9; flex-shrink: 0;
}
.admin-btn-primary {
    background: linear-gradient(135deg, #0d9488, #0f766e);
    color: white; border: none; border-radius: 0.625rem;
    padding: 0.5rem 1rem; font-size: 0.8rem; font-weight: 700;
    cursor: pointer; transition: all 0.2s; display: inline-flex;
    align-items: center; gap: 0.375rem;
}
.admin-btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(13,148,136,0.3); }
.admin-btn-danger {
    background: #fff5f5; color: #e53e3e; border: 1px solid #fed7d7;
    border-radius: 0.5rem; padding: 0.375rem 0.625rem; font-size: 0.75rem;
    font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.admin-btn-danger:hover { background: #e53e3e; color: white; }
.admin-btn-secondary {
    background: white; color: #475569; border: 1.5px solid #e2e8f0;
    border-radius: 0.625rem; padding: 0.5rem 1rem; font-size: 0.8rem;
    font-weight: 700; cursor: pointer; transition: all 0.2s;
    display: inline-flex; align-items: center; gap: 0.375rem;
}
.admin-btn-secondary:hover { border-color: #0d9488; color: #0d9488; }
.admin-badge {
    padding: 0.2rem 0.5rem; border-radius: 9999px; font-size: 0.65rem;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}
.admin-image-preview {
    width: 100%; aspect-ratio: 16/9; object-fit: cover;
    border-radius: 0.625rem; background: #f1f5f9; border: 2px dashed #cbd5e1;
    display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.github-push-badge {
    display: inline-flex; align-items: center; gap: 0.375rem;
    background: #1a1a2e; color: #a8edea; font-size: 0.7rem; font-weight: 700;
    padding: 0.25rem 0.625rem; border-radius: 9999px; border: 1px solid rgba(168,237,234,0.3);
}

/* ===== MEMORIES TAB ===== */
.memory-gate {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 55vh; padding: 2rem;
}
.memory-album-card {
    background: white; border-radius: 1.25rem; overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06); transition: all 0.4s cubic-bezier(0.16,1,0.3,1);
    cursor: pointer; border: 1px solid #e2e8f0; position: relative;
}
.memory-album-card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 20px 40px rgba(13,148,136,0.15);
    border-color: rgba(13,148,136,0.35);
}
.memory-album-cover {
    width: 100%; aspect-ratio: 4/3; object-fit: cover;
    background: linear-gradient(135deg, #0f172a, #134e4a);
}
.memory-media-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.625rem; }
@media(min-width:640px){ .memory-media-grid { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); } }
.memory-media-item {
    border-radius: 0.875rem; overflow: hidden; aspect-ratio: 1; cursor: pointer;
    position: relative; background: #f1f5f9; border: 1px solid #e2e8f0;
    transition: all 0.3s;
}
.memory-media-item:hover { transform: scale(1.03); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
.memory-media-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.memory-media-item:hover img { transform: scale(1.06); }
.memory-media-caption {
    position: absolute; bottom: 0; inset-x: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
    color: white; font-size: 0.65rem; padding: 0.5rem 0.375rem 0.375rem;
    text-align: center; font-weight: 500;
}
.memory-video-item {
    border-radius: 0.875rem; overflow: hidden; aspect-ratio: 16/9;
    grid-column: span 2; background: #0f172a; position: relative;
}
.memory-video-item iframe { width: 100%; height: 100%; border: none; }

/* ===== LIGHTBOX ===== */
.lightbox-overlay {
    position: fixed; inset: 0; z-index: 99999; background: rgba(0,0,0,0.94);
    display: flex; align-items: center; justify-content: center;
    padding: 1rem; animation: fadeIn 0.2s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.lightbox-inner { position: relative; max-width: min(1000px, 95vw); max-height: 90vh; display: flex; flex-direction: column; align-items: center; }
.lightbox-inner img { max-width: 100%; max-height: 82vh; border-radius: 0.875rem; object-fit: contain; box-shadow: 0 25px 60px rgba(0,0,0,0.4); }
.lightbox-close {
    position: absolute; top: -3rem; right: 0; background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2); color: white; width: 40px; height: 40px;
    border-radius: 50%; font-size: 1.1rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}
.lightbox-close:hover { background: rgba(255,255,255,0.25); }
.lightbox-caption { color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.875rem; text-align: center; font-style: italic; }

/* ===== FOOTER ===== */
.site-footer { background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%); color: white; padding: 3.5rem 0 0; margin-top: 0; }
.footer-brand-icon { width: 52px; height: 52px; background: linear-gradient(135deg, #0d9488, #5eead4); border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 1rem; }
.footer-link { color: rgba(255,255,255,0.6); transition: color 0.2s; display: block; padding: 0.25rem 0; font-size: 0.875rem; text-decoration: none; }
.footer-link:hover { color: #5eead4; padding-left: 0.375rem; }
.footer-social-btn { width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.7); font-size: 0.95rem; transition: all 0.2s; cursor: pointer; text-decoration: none; }
.footer-social-btn:hover { background: #0d9488; border-color: #0d9488; color: white; transform: translateY(-2px); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding: 1.25rem 0; text-align: center; font-size: 0.8rem; color: rgba(255,255,255,0.4); }

/* ===== CLICKABLE CARD LINKS ===== */
.card-with-link { text-decoration: none; color: inherit; display: block; }
.card-with-link:hover { text-decoration: none; }
"""

html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
print("CSS inserted OK")

# ============================================================
# PART 2: NEW NAV BUTTONS (after tab4 button)
# ============================================================
NAV_ANCHOR = '                <i class="fa-solid fa-utensils mr-2"></i>Ẩm Thực & Cafe\n            </button>'
NEW_NAV = '''                <i class="fa-solid fa-utensils mr-2"></i>Ẩm Thực & Cafe
            </button>
            <button onclick="switchTab('tab5')" id="btn-tab5" class="tab-btn px-6 py-4 text-gray-500 font-semibold border-b-4 border-transparent transition-colors whitespace-nowrap hover:bg-teal-50 hover:text-teal-700">
                <i class="fa-solid fa-heart mr-2"></i>Kỷ Niệm Đáng Nhớ
            </button>
            <button onclick="openAdminPanel()" id="btn-admin" class="tab-btn px-4 py-4 text-gray-400 font-semibold border-b-4 border-transparent transition-colors whitespace-nowrap hover:bg-gray-50 hover:text-gray-700 ml-auto border-l border-gray-100">
                <i class="fa-solid fa-shield-halved mr-1.5"></i><span class="text-xs">Admin</span>
            </button>'''
html = html.replace(NAV_ANCHOR, NEW_NAV, 1)
print("Nav buttons inserted OK")

# ============================================================
# PART 3: NEW TAB SECTIONS (before </main>)
# ============================================================
TAB5_AND_ADMIN_HTML = '''
        <!-- ========= TAB 5: KỶ NIỆM ĐÁNG NHỚ ========= -->
        <section id="tab5" class="tab-content hidden animate-fade-in">
            <!-- Password Gate -->
            <div id="mem-gate" class="memory-gate">
                <div class="text-center max-w-sm mx-auto">
                    <div class="w-20 h-20 bg-gradient-to-br from-pink-500 to-rose-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                        <i class="fa-solid fa-heart text-white text-3xl"></i>
                    </div>
                    <h2 class="text-2xl font-extrabold text-gray-800 mb-2">Kỷ Niệm Đáng Nhớ</h2>
                    <p class="text-gray-500 text-sm mb-6">Không gian riêng tư lưu giữ những khoảnh khắc đáng trân trọng.<br>Nhập mật khẩu để xem.</p>
                    <div class="relative mb-4">
                        <input id="mem-pass-input" type="password" placeholder="Mật khẩu..." onkeydown="if(event.key==='Enter')checkMemPass()"
                            class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-center font-bold text-lg focus:outline-none focus:border-rose-400 transition-colors tracking-widest">
                        <button onclick="checkMemPass()" class="absolute right-3 top-1/2 -translate-y-1/2 text-rose-500 hover:text-rose-700 transition-colors">
                            <i class="fa-solid fa-arrow-right-to-bracket text-xl"></i>
                        </button>
                    </div>
                    <p id="mem-pass-err" class="text-red-500 text-sm hidden">Mật khẩu không đúng. Thử lại nhé!</p>
                </div>
            </div>

            <!-- Memories Content (hidden until unlocked) -->
            <div id="mem-content" class="hidden">
                <!-- Header -->
                <div class="text-center mb-10">
                    <div class="inline-flex items-center gap-3 bg-gradient-to-r from-pink-50 to-rose-50 border border-rose-100 rounded-2xl px-6 py-3 mb-4">
                        <i class="fa-solid fa-heart text-rose-500 text-xl"></i>
                        <span class="font-extrabold text-rose-700 text-lg">Những Kỷ Niệm Không Thể Quên</span>
                    </div>
                    <p class="text-gray-500 text-sm">Lưu trữ những khoảnh khắc đẹp nhất của chuyến hành trình Côn Đảo.</p>
                </div>

                <!-- Album Grid -->
                <div id="memories-album-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8"></div>

                <!-- Album Detail View -->
                <div id="mem-album-detail" class="hidden">
                    <div class="flex items-center gap-3 mb-6">
                        <button onclick="closeAlbumDetail()" class="flex items-center gap-2 text-teal-600 hover:text-teal-800 font-bold transition-colors text-sm bg-teal-50 hover:bg-teal-100 px-4 py-2 rounded-xl">
                            <i class="fa-solid fa-arrow-left"></i> Quay lại Albums
                        </button>
                        <div id="mem-album-title" class="font-extrabold text-2xl text-gray-800"></div>
                    </div>
                    <div id="mem-album-desc" class="text-gray-500 text-sm mb-6"></div>
                    <div id="mem-album-items-grid" class="memory-media-grid"></div>
                </div>

                <!-- Empty State -->
                <div id="mem-empty-state" class="hidden text-center py-16 text-gray-400">
                    <i class="fa-solid fa-images text-5xl mb-4 opacity-30"></i>
                    <p class="font-bold text-lg">Chưa có kỷ niệm nào</p>
                    <p class="text-sm mt-1">Admin có thể thêm albums và hình ảnh qua tab Admin.</p>
                </div>
            </div>
        </section>

        <!-- ========= LIGHTBOX (Global, nằm ngoài tab) ========= -->
        <div id="lightbox-overlay" class="lightbox-overlay hidden" onclick="closeLightbox(event)">
            <div class="lightbox-inner">
                <button class="lightbox-close" onclick="closeLightboxBtn()"><i class="fa-solid fa-xmark"></i></button>
                <img id="lightbox-img" src="" alt="">
                <p id="lightbox-caption" class="lightbox-caption"></p>
            </div>
        </div>

        <!-- ========= ADMIN MODAL (overlay toàn màn hình) ========= -->
        <div id="admin-modal" class="fixed inset-0 z-[9990] bg-black/50 hidden" onclick="closeAdminIfBackdrop(event)">
            <!-- Admin Login Screen -->
            <div id="admin-login-screen" class="flex items-center justify-center h-full">
                <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-sm mx-4 text-center">
                    <div class="w-16 h-16 bg-gradient-to-br from-teal-500 to-teal-700 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-lg">
                        <i class="fa-solid fa-shield-halved text-white text-2xl"></i>
                    </div>
                    <h2 class="text-xl font-extrabold text-gray-800 mb-1">Khu Vực Admin</h2>
                    <p class="text-gray-400 text-xs mb-5">Chỉ dành cho quản trị viên website</p>
                    <div class="relative mb-3">
                        <input id="admin-pass-input" type="password" placeholder="Nhập mật khẩu admin..." onkeydown="if(event.key==='Enter')checkAdminPass()"
                            class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-center font-bold focus:outline-none focus:border-teal-400 transition-colors tracking-widest">
                    </div>
                    <p id="admin-pass-err" class="text-red-500 text-xs mb-3 hidden">Mật khẩu không chính xác!</p>
                    <div class="flex gap-2">
                        <button onclick="checkAdminPass()" class="flex-1 bg-teal-600 hover:bg-teal-700 text-white font-bold py-2.5 rounded-xl transition-colors">
                            <i class="fa-solid fa-unlock mr-1.5"></i>Đăng Nhập
                        </button>
                        <button onclick="closeAdminModal()" class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-2.5 rounded-xl transition-colors">Hủy</button>
                    </div>
                </div>
            </div>

            <!-- Admin Panel (sau khi đăng nhập) -->
            <div id="admin-panel" class="hidden h-full flex flex-col bg-white">
                <!-- Admin Top Bar -->
                <div class="flex items-center justify-between px-5 py-3 bg-gray-900 text-white border-b border-gray-800 shrink-0">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center">
                            <i class="fa-solid fa-shield-halved text-white text-sm"></i>
                        </div>
                        <span class="font-extrabold text-sm">Admin Dashboard — Côn Đảo</span>
                        <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">Đang đăng nhập</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="exportCMSData()" class="text-gray-400 hover:text-teal-400 text-xs flex items-center gap-1 transition-colors">
                            <i class="fa-solid fa-download"></i> Export JSON
                        </button>
                        <label class="text-gray-400 hover:text-teal-400 text-xs flex items-center gap-1 transition-colors cursor-pointer">
                            <i class="fa-solid fa-upload"></i> Import JSON
                            <input type="file" accept=".json" class="hidden" onchange="importCMSData(event)">
                        </label>
                        <button onclick="logoutAdmin()" class="ml-2 text-gray-400 hover:text-red-400 text-xs flex items-center gap-1 transition-colors">
                            <i class="fa-solid fa-right-from-bracket"></i> Đăng xuất
                        </button>
                        <button onclick="closeAdminModal()" class="ml-2 text-gray-400 hover:text-white w-7 h-7 flex items-center justify-center rounded-full hover:bg-gray-700 transition-colors">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                </div>

                <!-- Admin Body -->
                <div class="admin-panel-container flex-1 min-h-0 overflow-hidden">
                    <!-- Sidebar -->
                    <div class="admin-sidebar hidden md:flex">
                        <div class="text-xs font-bold text-gray-500 uppercase tracking-widest px-2 mb-2 mt-1">Quản Lý Nội Dung</div>
                        <div class="admin-sidebar-item admin-active" onclick="showAdminSection('dest')">
                            <i class="fa-solid fa-location-dot"></i> Địa Điểm
                        </div>
                        <div class="admin-sidebar-item" onclick="showAdminSection('hotel')">
                            <i class="fa-solid fa-hotel"></i> Lưu Trú
                        </div>
                        <div class="admin-sidebar-item" onclick="showAdminSection('food')">
                            <i class="fa-solid fa-utensils"></i> Ẩm Thực
                        </div>
                        <div class="admin-sidebar-item" onclick="showAdminSection('mem')">
                            <i class="fa-solid fa-images"></i> Kỷ Niệm
                        </div>
                        <div class="text-xs font-bold text-gray-500 uppercase tracking-widest px-2 mb-2 mt-4">Hệ Thống</div>
                        <div class="admin-sidebar-item" onclick="showAdminSection('settings')">
                            <i class="fa-solid fa-sliders"></i> Cài Đặt
                        </div>
                    </div>

                    <!-- Mobile Tab Selector -->
                    <div class="md:hidden flex overflow-x-auto gap-1 bg-gray-900 px-3 py-2 border-b border-gray-800 shrink-0" style="position:absolute;top:53px;left:0;right:0;z-index:1;">
                        <button onclick="showAdminSection('dest')" class="admin-mob-btn text-white bg-teal-600 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap">📍 Địa Điểm</button>
                        <button onclick="showAdminSection('hotel')" class="admin-mob-btn text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap">🏨 Lưu Trú</button>
                        <button onclick="showAdminSection('food')" class="admin-mob-btn text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap">🍽 Ẩm Thực</button>
                        <button onclick="showAdminSection('mem')" class="admin-mob-btn text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap">📸 Kỷ Niệm</button>
                        <button onclick="showAdminSection('settings')" class="admin-mob-btn text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap">⚙️ Cài Đặt</button>
                    </div>

                    <!-- Main Content Area -->
                    <div class="admin-main md:mt-0 mt-12">
                        <!-- ---- SECTION: DESTINATIONS ---- -->
                        <div id="admin-sec-dest" class="admin-section admin-section-visible">
                            <div class="flex items-center justify-between mb-5">
                                <div>
                                    <h2 class="text-xl font-extrabold text-gray-800">📍 Quản Lý Địa Điểm</h2>
                                    <p class="text-gray-400 text-xs mt-0.5">Thêm/sửa/xóa các địa điểm hiển thị ở Tab 1</p>
                                </div>
                                <button onclick="showDestForm(null)" class="admin-btn-primary">
                                    <i class="fa-solid fa-plus"></i> Thêm Mới
                                </button>
                            </div>

                            <!-- Add/Edit Form -->
                            <div id="dest-form-area" class="hidden mb-6 bg-white rounded-2xl border border-teal-100 p-5 shadow-sm">
                                <h3 id="dest-form-title" class="font-extrabold text-gray-800 mb-4">Thêm Địa Điểm Mới</h3>
                                <input type="hidden" id="dest-edit-id">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="admin-form-label">Tên địa điểm *</label>
                                        <input id="dest-name" type="text" class="admin-form-input" placeholder="Ví dụ: Bãi Đầm Trầu">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Danh mục *</label>
                                        <select id="dest-category" class="admin-form-input">
                                            <option value="beach">🏖 Bãi Tắm & Sinh Thái Biển</option>
                                            <option value="dive">🤿 Lặn Biển & Hải Đảo</option>
                                            <option value="history">🏛 Di Tích Lịch Sử</option>
                                            <option value="spiritual">🙏 Tâm Linh & Văn Hóa</option>
                                            <option value="nature">🌿 Thiên Nhiên & Rừng</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Đánh giá (0-5)</label>
                                        <input id="dest-rating" type="number" step="0.1" min="0" max="5" class="admin-form-input" placeholder="4.5">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link Google Maps</label>
                                        <input id="dest-maps" type="url" class="admin-form-input" placeholder="https://maps.google.com/...">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link ngoài (tùy chọn) — nhấn vào card mở link này</label>
                                        <input id="dest-link" type="url" class="admin-form-input" placeholder="https://...">
                                    </div>
                                    <div></div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Mô tả ngắn *</label>
                                        <input id="dest-desc-short" type="text" class="admin-form-input" placeholder="Mô tả 1 dòng ngắn gọn hiển thị ở card">
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Mô tả chi tiết</label>
                                        <textarea id="dest-desc-long" class="admin-form-input admin-form-textarea" placeholder="Giới thiệu đầy đủ..."></textarea>
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Trải nghiệm nổi bật (mỗi điểm 1 dòng)</label>
                                        <textarea id="dest-highlights" class="admin-form-input admin-form-textarea" placeholder="Tắm biển nước trong vắt&#10;Ngắm máy bay hạ cánh&#10;Đi bộ sang Bãi Suối Nóng"></textarea>
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Thời điểm lý tưởng</label>
                                        <input id="dest-best-time" type="text" class="admin-form-input" placeholder="Buổi sáng sớm, tránh mùa mưa tháng 7-9">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Ảnh chính <span class="github-push-badge"><i class="fa-brands fa-github"></i> Auto push GitHub</span></label>
                                        <input id="dest-img1-file" type="file" accept="image/*" onchange="previewImage(this,'dest-img1-preview')" class="admin-form-input">
                                        <img id="dest-img1-preview" src="" alt="" class="mt-2 rounded-xl hidden" style="max-height:120px;object-fit:cover;width:100%;">
                                        <input id="dest-img1-url" type="url" class="admin-form-input mt-2" placeholder="Hoặc dán URL ảnh trực tiếp">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Ảnh phụ (tùy chọn) <span class="github-push-badge"><i class="fa-brands fa-github"></i> Auto push GitHub</span></label>
                                        <input id="dest-img2-file" type="file" accept="image/*" onchange="previewImage(this,'dest-img2-preview')" class="admin-form-input">
                                        <img id="dest-img2-preview" src="" alt="" class="mt-2 rounded-xl hidden" style="max-height:120px;object-fit:cover;width:100%;">
                                        <input id="dest-img2-url" type="url" class="admin-form-input mt-2" placeholder="Hoặc dán URL ảnh trực tiếp">
                                    </div>
                                    <div class="md:col-span-2">
                                        <div id="dest-github-status" class="hidden text-xs text-teal-700 bg-teal-50 border border-teal-100 rounded-lg px-3 py-2 mb-3">
                                            <i class="fa-solid fa-circle-notch fa-spin mr-1"></i> Đang đẩy ảnh lên GitHub...
                                        </div>
                                        <div class="flex gap-2">
                                            <button onclick="saveDestination()" class="admin-btn-primary">
                                                <i class="fa-solid fa-floppy-disk"></i> Lưu & Cập Nhật
                                            </button>
                                            <button onclick="hideDestForm()" class="admin-btn-secondary">Hủy</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- List of Admin-added Destinations -->
                            <div id="admin-dest-list"></div>

                            <!-- Note about existing items -->
                            <div class="mt-6 bg-blue-50 border border-blue-100 rounded-xl p-4 text-xs text-blue-700">
                                <i class="fa-solid fa-circle-info mr-1"></i>
                                <strong>Lưu ý:</strong> Các địa điểm bạn thêm qua đây sẽ xuất hiện ở đầu danh sách Tab 1. 
                                Các địa điểm gốc được hardcode vẫn hiển thị bên dưới. Dữ liệu lưu tại localStorage trình duyệt này.
                            </div>
                        </div>

                        <!-- ---- SECTION: HOTELS ---- -->
                        <div id="admin-sec-hotel" class="admin-section">
                            <div class="flex items-center justify-between mb-5">
                                <div>
                                    <h2 class="text-xl font-extrabold text-gray-800">🏨 Quản Lý Lưu Trú</h2>
                                    <p class="text-gray-400 text-xs mt-0.5">Thêm/sửa/xóa khách sạn hiển thị ở Tab 3</p>
                                </div>
                                <button onclick="showHotelForm(null)" class="admin-btn-primary">
                                    <i class="fa-solid fa-plus"></i> Thêm Mới
                                </button>
                            </div>

                            <div id="hotel-form-area" class="hidden mb-6 bg-white rounded-2xl border border-teal-100 p-5 shadow-sm">
                                <h3 id="hotel-form-title" class="font-extrabold text-gray-800 mb-4">Thêm Khách Sạn Mới</h3>
                                <input type="hidden" id="hotel-edit-id">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="admin-form-label">Tên khách sạn/resort *</label>
                                        <input id="hotel-name" type="text" class="admin-form-input" placeholder="Tên nơi lưu trú">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Số sao</label>
                                        <select id="hotel-stars" class="admin-form-input">
                                            <option value="5">⭐⭐⭐⭐⭐ (5 sao)</option>
                                            <option value="4">⭐⭐⭐⭐ (4 sao)</option>
                                            <option value="3" selected>⭐⭐⭐ (3 sao)</option>
                                            <option value="2">⭐⭐ (2 sao)</option>
                                            <option value="Boutique">🏡 Boutique</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Khoảng giá/đêm</label>
                                        <input id="hotel-price" type="text" class="admin-form-input" placeholder="~ 1.5M - 2.5M VNĐ">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Địa chỉ</label>
                                        <input id="hotel-address" type="text" class="admin-form-input" placeholder="Số nhà, đường, khu">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link Google Maps</label>
                                        <input id="hotel-maps" type="url" class="admin-form-input" placeholder="https://maps.google.com/...">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link đặt phòng (Booking/Agoda...)</label>
                                        <input id="hotel-link" type="url" class="admin-form-input" placeholder="https://booking.com/...">
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Mô tả</label>
                                        <textarea id="hotel-desc" class="admin-form-input admin-form-textarea" placeholder="Mô tả tổng quan về nơi lưu trú..."></textarea>
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Ảnh thumbnail <span class="github-push-badge"><i class="fa-brands fa-github"></i> Auto push GitHub</span></label>
                                        <input id="hotel-img-file" type="file" accept="image/*" onchange="previewImage(this,'hotel-img-preview')" class="admin-form-input">
                                        <img id="hotel-img-preview" src="" alt="" class="mt-2 rounded-xl hidden" style="max-height:100px;object-fit:cover;width:100%;">
                                        <input id="hotel-img-url" type="url" class="admin-form-input mt-2" placeholder="Hoặc dán URL ảnh">
                                    </div>
                                    <div class="md:col-span-2">
                                        <div id="hotel-github-status" class="hidden text-xs text-teal-700 bg-teal-50 border border-teal-100 rounded-lg px-3 py-2 mb-3">
                                            <i class="fa-solid fa-circle-notch fa-spin mr-1"></i> Đang đẩy ảnh lên GitHub...
                                        </div>
                                        <div class="flex gap-2">
                                            <button onclick="saveHotel()" class="admin-btn-primary">
                                                <i class="fa-solid fa-floppy-disk"></i> Lưu & Cập Nhật
                                            </button>
                                            <button onclick="hideHotelForm()" class="admin-btn-secondary">Hủy</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div id="admin-hotel-list"></div>
                        </div>

                        <!-- ---- SECTION: FOOD ---- -->
                        <div id="admin-sec-food" class="admin-section">
                            <div class="flex items-center justify-between mb-5">
                                <div>
                                    <h2 class="text-xl font-extrabold text-gray-800">🍽️ Quản Lý Ẩm Thực</h2>
                                    <p class="text-gray-400 text-xs mt-0.5">Thêm/sửa/xóa món ăn & quán hiển thị ở Tab 4</p>
                                </div>
                                <button onclick="showFoodForm(null)" class="admin-btn-primary">
                                    <i class="fa-solid fa-plus"></i> Thêm Mới
                                </button>
                            </div>

                            <div id="food-form-area" class="hidden mb-6 bg-white rounded-2xl border border-teal-100 p-5 shadow-sm">
                                <h3 id="food-form-title" class="font-extrabold text-gray-800 mb-4">Thêm Món Ăn / Quán Mới</h3>
                                <input type="hidden" id="food-edit-id">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="admin-form-label">Tên món ăn / quán *</label>
                                        <input id="food-name" type="text" class="admin-form-input" placeholder="Tên món hoặc nhà hàng">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Danh mục *</label>
                                        <select id="food-category" class="admin-form-input">
                                            <option value="seafood">🦞 Hải Sản</option>
                                            <option value="specialty">🌟 Đặc Sản Phải Thử</option>
                                            <option value="cafe">☕ Cafe & Đồ Uống</option>
                                            <option value="restaurant">🍽 Nhà Hàng</option>
                                            <option value="street">🛵 Ăn Vặt & Đường Phố</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Địa chỉ</label>
                                        <input id="food-address" type="text" class="admin-form-input" placeholder="Địa chỉ quán">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link Google Maps</label>
                                        <input id="food-maps" type="url" class="admin-form-input" placeholder="https://maps.google.com/...">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Link review / đặt bàn (tùy chọn)</label>
                                        <input id="food-link" type="url" class="admin-form-input" placeholder="https://...">
                                    </div>
                                    <div></div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Mô tả / Đặc trưng</label>
                                        <textarea id="food-desc" class="admin-form-input admin-form-textarea" placeholder="Mô tả món ăn, hương vị, nét đặc trưng..."></textarea>
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Ảnh món ăn <span class="github-push-badge"><i class="fa-brands fa-github"></i> Auto push GitHub</span></label>
                                        <input id="food-img-file" type="file" accept="image/*" onchange="previewImage(this,'food-img-preview')" class="admin-form-input">
                                        <img id="food-img-preview" src="" alt="" class="mt-2 rounded-xl hidden" style="max-height:100px;object-fit:cover;width:100%;">
                                        <input id="food-img-url" type="url" class="admin-form-input mt-2" placeholder="Hoặc dán URL ảnh">
                                    </div>
                                    <div class="md:col-span-2">
                                        <div id="food-github-status" class="hidden text-xs text-teal-700 bg-teal-50 border border-teal-100 rounded-lg px-3 py-2 mb-3"></div>
                                        <div class="flex gap-2">
                                            <button onclick="saveFood()" class="admin-btn-primary">
                                                <i class="fa-solid fa-floppy-disk"></i> Lưu & Cập Nhật
                                            </button>
                                            <button onclick="hideFoodForm()" class="admin-btn-secondary">Hủy</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div id="admin-food-list"></div>
                        </div>

                        <!-- ---- SECTION: MEMORIES ADMIN ---- -->
                        <div id="admin-sec-mem" class="admin-section">
                            <div class="flex items-center justify-between mb-5">
                                <div>
                                    <h2 class="text-xl font-extrabold text-gray-800">📸 Quản Lý Kỷ Niệm</h2>
                                    <p class="text-gray-400 text-xs mt-0.5">Tạo album và thêm ảnh/video cho Tab Kỷ Niệm</p>
                                </div>
                                <button onclick="showAlbumForm()" class="admin-btn-primary">
                                    <i class="fa-solid fa-plus"></i> Tạo Album
                                </button>
                            </div>

                            <!-- Album Create Form -->
                            <div id="album-form-area" class="hidden mb-6 bg-white rounded-2xl border border-pink-100 p-5 shadow-sm">
                                <h3 class="font-extrabold text-gray-800 mb-4">Tạo Album Kỷ Niệm Mới</h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="admin-form-label">Tên album *</label>
                                        <input id="album-name" type="text" class="admin-form-input" placeholder="Ví dụ: Ngày đầu tiên ở Côn Đảo">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Emoji đại diện</label>
                                        <input id="album-emoji" type="text" class="admin-form-input" placeholder="🌊" maxlength="4">
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Mô tả album</label>
                                        <input id="album-desc" type="text" class="admin-form-input" placeholder="Mô tả ngắn về album này">
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Ảnh bìa album (URL hoặc link Drive chia sẻ)</label>
                                        <input id="album-cover" type="url" class="admin-form-input" placeholder="https://drive.google.com/... hoặc https://...">
                                    </div>
                                    <div class="md:col-span-2 flex gap-2">
                                        <button onclick="createAlbum()" class="admin-btn-primary"><i class="fa-solid fa-plus"></i> Tạo Album</button>
                                        <button onclick="hideAlbumForm()" class="admin-btn-secondary">Hủy</button>
                                    </div>
                                </div>
                            </div>

                            <!-- Albums Manager -->
                            <div id="admin-mem-list"></div>
                        </div>

                        <!-- ---- SECTION: SETTINGS ---- -->
                        <div id="admin-sec-settings" class="admin-section">
                            <h2 class="text-xl font-extrabold text-gray-800 mb-2">⚙️ Cài Đặt Hệ Thống</h2>
                            <p class="text-gray-400 text-xs mb-6">Cấu hình GitHub API và bảo mật</p>

                            <!-- GitHub Config -->
                            <div class="bg-white rounded-2xl border border-gray-200 p-5 mb-4 shadow-sm">
                                <div class="flex items-center gap-2 mb-4">
                                    <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
                                        <i class="fa-brands fa-github text-white text-sm"></i>
                                    </div>
                                    <h3 class="font-extrabold text-gray-800">GitHub Integration</h3>
                                </div>
                                <div class="bg-amber-50 border border-amber-100 rounded-xl p-3 mb-4 text-xs text-amber-700">
                                    <i class="fa-solid fa-triangle-exclamation mr-1"></i>
                                    <strong>Cảnh báo bảo mật:</strong> Token được lưu trong localStorage trình duyệt. Chỉ sử dụng Fine-grained token với quyền tối thiểu (chỉ write vào repo này).
                                </div>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">GitHub Personal Access Token</label>
                                        <input id="gh-token" type="password" class="admin-form-input" placeholder="ghp_xxxxxxxxxxxx">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Repository (owner/repo)</label>
                                        <input id="gh-repo" type="text" class="admin-form-input" value="LarryVan-engin/Some_stuff_case" placeholder="owner/repo-name">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Branch</label>
                                        <input id="gh-branch" type="text" class="admin-form-input" value="main" placeholder="main">
                                    </div>
                                    <div class="md:col-span-2">
                                        <label class="admin-form-label">Đường dẫn thư mục ảnh</label>
                                        <input id="gh-path" type="text" class="admin-form-input" value="condao/images/" placeholder="condao/images/">
                                    </div>
                                    <div class="md:col-span-2">
                                        <button onclick="saveGithubConfig()" class="admin-btn-primary">
                                            <i class="fa-solid fa-floppy-disk"></i> Lưu Cài Đặt GitHub
                                        </button>
                                        <button onclick="testGithubConfig()" class="admin-btn-secondary ml-2">
                                            <i class="fa-solid fa-plug"></i> Test kết nối
                                        </button>
                                    </div>
                                    <div id="gh-test-result" class="md:col-span-2 text-xs rounded-lg px-3 py-2 hidden"></div>
                                </div>
                            </div>

                            <!-- Memory Password -->
                            <div class="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">
                                <div class="flex items-center gap-2 mb-4">
                                    <div class="w-8 h-8 bg-rose-500 rounded-lg flex items-center justify-center">
                                        <i class="fa-solid fa-heart text-white text-sm"></i>
                                    </div>
                                    <h3 class="font-extrabold text-gray-800">Mật Khẩu Tab Kỷ Niệm</h3>
                                </div>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="admin-form-label">Mật khẩu mới</label>
                                        <input id="new-mem-pass" type="password" class="admin-form-input" placeholder="Nhập mật khẩu mới">
                                    </div>
                                    <div>
                                        <label class="admin-form-label">Xác nhận mật khẩu</label>
                                        <input id="confirm-mem-pass" type="password" class="admin-form-input" placeholder="Nhập lại mật khẩu">
                                    </div>
                                    <div class="md:col-span-2">
                                        <button onclick="changeMemoryPass()" class="admin-btn-primary">
                                            <i class="fa-solid fa-key"></i> Đổi Mật Khẩu
                                        </button>
                                    </div>
                                    <div id="mem-pass-change-result" class="md:col-span-2 text-xs rounded-lg px-3 py-2 hidden"></div>
                                </div>
                            </div>
                        </div>
                    </div><!-- end admin-main -->
                </div><!-- end admin-panel-container -->
            </div><!-- end admin-panel -->
        </div><!-- end admin-modal -->
'''

html = html.replace('    </main>', TAB5_AND_ADMIN_HTML + '\n    </main>', 1)
print("Tab5 and Admin modal HTML inserted OK")

# ============================================================
# PART 4: FOOTER (after </main>)
# ============================================================
FOOTER_HTML = '''
    <!-- ===== SITE FOOTER ===== -->
    <footer class="site-footer">
        <div class="max-w-6xl mx-auto px-4 sm:px-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 pb-10">
                <!-- Col 1: Brand -->
                <div>
                    <div class="footer-brand-icon">
                        <i class="fa-solid fa-umbrella-beach text-white"></i>
                    </div>
                    <h3 class="text-xl font-extrabold text-white mb-2">Khám Phá Côn Đảo</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        Trang web cá nhân ghi lại hành trình khám phá Côn Đảo — viên ngọc hoang sơ, chốn bình yên mang đậm dấu ấn lịch sử hào hùng.
                    </p>
                    <div class="flex items-center gap-2 mt-4">
                        <a href="https://github.com/LarryVan-engin" target="_blank" class="footer-social-btn" title="GitHub">
                            <i class="fa-brands fa-github"></i>
                        </a>
                        <a href="#" class="footer-social-btn" title="Facebook">
                            <i class="fa-brands fa-facebook-f"></i>
                        </a>
                        <a href="#" class="footer-social-btn" title="Instagram">
                            <i class="fa-brands fa-instagram"></i>
                        </a>
                    </div>
                </div>

                <!-- Col 2: Quick Links -->
                <div>
                    <h4 class="text-sm font-extrabold text-white/90 uppercase tracking-widest mb-4">Điều Hướng Nhanh</h4>
                    <nav class="space-y-1">
                        <a onclick="switchTab('tab1')" href="#" class="footer-link"><i class="fa-solid fa-camera-retro mr-2 text-teal-400 text-xs"></i>Khám Phá Địa Điểm</a>
                        <a onclick="switchTab('tab2')" href="#" class="footer-link"><i class="fa-solid fa-map-location-dot mr-2 text-teal-400 text-xs"></i>Lịch Trình 4N3Đ</a>
                        <a onclick="switchTab('tab3')" href="#" class="footer-link"><i class="fa-solid fa-plane-departure mr-2 text-teal-400 text-xs"></i>Kênh Di Chuyển & Lưu Trú</a>
                        <a onclick="switchTab('tab4')" href="#" class="footer-link"><i class="fa-solid fa-utensils mr-2 text-teal-400 text-xs"></i>Ẩm Thực & Cafe</a>
                        <a onclick="switchTab('tab5')" href="#" class="footer-link"><i class="fa-solid fa-heart mr-2 text-rose-400 text-xs"></i>Kỷ Niệm Đáng Nhớ</a>
                    </nav>
                </div>

                <!-- Col 3: Author Info -->
                <div>
                    <h4 class="text-sm font-extrabold text-white/90 uppercase tracking-widest mb-4">Về Tác Giả</h4>
                    <div class="flex items-start gap-3 mb-4">
                        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-teal-700 flex items-center justify-center shrink-0 shadow-lg">
                            <i class="fa-solid fa-user text-white text-lg"></i>
                        </div>
                        <div>
                            <p class="font-bold text-white text-sm">LarryVan</p>
                            <p class="text-gray-400 text-xs leading-relaxed mt-0.5">
                                Lữ khách yêu thiên nhiên, nhiếp ảnh và những hành trình khám phá đảo ngọc hoang sơ.
                            </p>
                        </div>
                    </div>
                    <div class="space-y-2 text-xs text-gray-500">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-map-marker-alt text-teal-500"></i>
                            <span>Việt Nam</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="fa-brands fa-github text-teal-500"></i>
                            <a href="https://github.com/LarryVan-engin/Some_stuff_case" target="_blank" class="text-teal-400 hover:text-teal-300 transition-colors">LarryVan-engin/Some_stuff_case</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="max-w-6xl mx-auto px-4">
                <p>© 2026 <strong class="text-teal-400">LarryVan</strong>. All rights reserved. Made with <i class="fa-solid fa-heart text-rose-400 mx-0.5"></i> for Côn Đảo.</p>
                <p class="mt-1 text-[11px] opacity-60">Trang web cá nhân, phi thương mại. Hình ảnh thuộc về chủ sở hữu hoặc nguồn Wikipedia Commons.</p>
            </div>
        </div>
    </footer>
'''

html = html.replace('    </main>\n\n    <script>', '    </main>\n\n' + FOOTER_HTML + '\n    <script>', 1)
print("Footer HTML inserted OK")

# ============================================================
# PART 5: ADMIN + MEMORIES JAVASCRIPT (before </script>)
# ============================================================
NEW_JS = r"""
// ============================================================
// ===== ADMIN & MEMORIES ENGINE =====
// ============================================================

// --- Constants & State ---
const ADMIN_PASSWORD = 'Thaodangiu';
const DEFAULT_MEM_PASSWORD = 'ConDao2026';
let adminCurrentSection = 'dest';
let editingAlbumId = null;

// --- Storage Keys ---
const KEYS = {
    adminDests:  'condao_admin_destinations',
    adminHotels: 'condao_admin_hotels',
    adminFood:   'condao_admin_food',
    memories:    'condao_memories',
    memPass:     'condao_memory_pass',
    ghToken:     'condao_github_token',
    ghConfig:    'condao_github_config',
};

// --- Utilities ---
function loadData(key, def=[]) {
    try { return JSON.parse(localStorage.getItem(key)) || def; }
    catch(e){ return def; }
}
function saveData(key, data) { localStorage.setItem(key, JSON.stringify(data)); }
function genId() { return Date.now().toString(36) + Math.random().toString(36).slice(2); }

// --- Simple hash (not cryptographic, just obfuscation) ---
function simpleHash(str) {
    let h = 5381;
    for(let i=0;i<str.length;i++){ h = ((h<<5)+h)+str.charCodeAt(i); h|=0; }
    return h.toString(16);
}

// ============================================================
// ADMIN AUTH
// ============================================================
function openAdminPanel() {
    const modal = document.getElementById('admin-modal');
    modal.classList.remove('hidden');
    if(sessionStorage.getItem('adminLoggedIn') === 'yes') {
        showAdminPanelContent();
    } else {
        document.getElementById('admin-login-screen').classList.remove('hidden');
        document.getElementById('admin-panel').classList.add('hidden');
        setTimeout(()=>document.getElementById('admin-pass-input').focus(), 100);
    }
}

function checkAdminPass() {
    const input = document.getElementById('admin-pass-input').value;
    if(input === ADMIN_PASSWORD) {
        sessionStorage.setItem('adminLoggedIn','yes');
        document.getElementById('admin-pass-err').classList.add('hidden');
        document.getElementById('admin-pass-input').value = '';
        showAdminPanelContent();
    } else {
        document.getElementById('admin-pass-err').classList.remove('hidden');
        document.getElementById('admin-pass-input').value = '';
        document.getElementById('admin-pass-input').focus();
    }
}

function showAdminPanelContent() {
    document.getElementById('admin-login-screen').classList.add('hidden');
    document.getElementById('admin-panel').classList.remove('hidden');
    loadGithubConfigToForm();
    showAdminSection(adminCurrentSection);
}

function closeAdminModal() {
    document.getElementById('admin-modal').classList.add('hidden');
}

function closeAdminIfBackdrop(e) {
    if(e.target === document.getElementById('admin-modal')) closeAdminModal();
}

function logoutAdmin() {
    sessionStorage.removeItem('adminLoggedIn');
    closeAdminModal();
}

// ============================================================
// ADMIN SECTION NAVIGATION
// ============================================================
function showAdminSection(sec) {
    adminCurrentSection = sec;
    document.querySelectorAll('.admin-section').forEach(el=>el.classList.remove('admin-section-visible'));
    document.getElementById('admin-sec-'+sec).classList.add('admin-section-visible');
    document.querySelectorAll('.admin-sidebar-item').forEach(el=>el.classList.remove('admin-active'));
    const items = document.querySelectorAll('.admin-sidebar-item');
    const map = { dest:0, hotel:1, food:2, mem:3, settings:4 };
    if(items[map[sec]]) items[map[sec]].classList.add('admin-active');
    document.querySelectorAll('.admin-mob-btn').forEach((btn,i)=>{
        btn.classList.remove('bg-teal-600','text-white');
        btn.classList.add('text-gray-400');
    });
    if(sec==='dest') renderAdminDestList();
    if(sec==='hotel') renderAdminHotelList();
    if(sec==='food') renderAdminFoodList();
    if(sec==='mem') renderAdminMemList();
    if(sec==='settings') loadGithubConfigToForm();
}

// ============================================================
// IMAGE UTILS
// ============================================================
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];
    if(!file) return;
    const reader = new FileReader();
    reader.onload = e => {
        preview.src = e.target.result;
        preview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

async function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

async function pushImageToGitHub(fileInput, urlInput, statusElId, filenamePrefix) {
    const urlVal = urlInput.value.trim();
    const file = fileInput.files[0];

    // If only URL is given, no GitHub push needed
    if(!file) return urlVal || '';

    const config = loadData(KEYS.ghConfig, {});
    const token = localStorage.getItem(KEYS.ghToken) || '';
    if(!token) {
        const el = document.getElementById(statusElId);
        if(el) { el.innerHTML='<i class="fa-solid fa-triangle-exclamation text-amber-500 mr-1"></i> Chưa cấu hình GitHub Token. Ảnh lưu cục bộ.'; el.classList.remove('hidden'); }
        return URL.createObjectURL(file);
    }

    const repo = (config.repo||'LarryVan-engin/Some_stuff_case');
    const branch = (config.branch||'main');
    const path = (config.path||'condao/images/');
    const ext = file.name.split('.').pop();
    const filename = `${filenamePrefix}_${Date.now()}.${ext}`;
    const fullPath = `${path}${filename}`.replace(/\/\//g,'/');
    const el = document.getElementById(statusElId);
    if(el) { el.innerHTML='<i class="fa-solid fa-circle-notch fa-spin mr-1"></i> Đang đẩy ảnh lên GitHub...'; el.classList.remove('hidden'); }

    try {
        const content = await fileToBase64(file);
        const resp = await fetch(`https://api.github.com/repos/${repo}/contents/${fullPath}`, {
            method: 'PUT',
            headers: { 'Authorization': `token ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: `Add image: ${filename}`, content, branch })
        });
        const data = await resp.json();
        if(resp.ok && data.content) {
            const rawUrl = data.content.download_url;
            if(el) { el.innerHTML=`<i class="fa-solid fa-check text-green-600 mr-1"></i> Đẩy lên GitHub thành công! <a href="${rawUrl}" target="_blank" class="text-teal-600 underline">Xem ảnh</a>`; }
            return rawUrl;
        } else {
            if(el) { el.innerHTML=`<i class="fa-solid fa-xmark text-red-500 mr-1"></i> GitHub Error: ${data.message||'Unknown error'}`; }
            return URL.createObjectURL(file);
        }
    } catch(err) {
        if(el) { el.innerHTML=`<i class="fa-solid fa-xmark text-red-500 mr-1"></i> Lỗi kết nối: ${err.message}`; }
        return URL.createObjectURL(file);
    }
}

// ============================================================
// CMS: DESTINATIONS
// ============================================================
function showDestForm(id) {
    const area = document.getElementById('dest-form-area');
    area.classList.remove('hidden');
    document.getElementById('dest-form-title').textContent = id ? 'Chỉnh Sửa Địa Điểm' : 'Thêm Địa Điểm Mới';
    document.getElementById('dest-edit-id').value = id || '';
    if(id) {
        const items = loadData(KEYS.adminDests);
        const item = items.find(d=>d.id===id);
        if(item) {
            document.getElementById('dest-name').value = item.name||'';
            document.getElementById('dest-category').value = item.category||'beach';
            document.getElementById('dest-rating').value = item.rating||'';
            document.getElementById('dest-maps').value = item.mapsUrl||'';
            document.getElementById('dest-link').value = item.linkUrl||'';
            document.getElementById('dest-desc-short').value = item.descShort||'';
            document.getElementById('dest-desc-long').value = item.descLong||'';
            document.getElementById('dest-highlights').value = (item.highlights||[]).join('\n');
            document.getElementById('dest-best-time').value = item.bestTime||'';
            document.getElementById('dest-img1-url').value = item.img1||'';
            document.getElementById('dest-img2-url').value = item.img2||'';
            if(item.img1) { document.getElementById('dest-img1-preview').src=item.img1; document.getElementById('dest-img1-preview').classList.remove('hidden'); }
            if(item.img2) { document.getElementById('dest-img2-preview').src=item.img2; document.getElementById('dest-img2-preview').classList.remove('hidden'); }
        }
    } else {
        ['dest-name','dest-rating','dest-maps','dest-link','dest-desc-short','dest-desc-long','dest-highlights','dest-best-time','dest-img1-url','dest-img2-url'].forEach(id=>document.getElementById(id).value='');
        ['dest-img1-preview','dest-img2-preview'].forEach(id=>{document.getElementById(id).src=''; document.getElementById(id).classList.add('hidden');});
    }
    area.scrollIntoView({behavior:'smooth'});
}

function hideDestForm() { document.getElementById('dest-form-area').classList.add('hidden'); }

async function saveDestination() {
    const name = document.getElementById('dest-name').value.trim();
    if(!name) { alert('Vui lòng nhập tên địa điểm!'); return; }
    const img1 = await pushImageToGitHub(
        document.getElementById('dest-img1-file'),
        document.getElementById('dest-img1-url'),
        'dest-github-status', 'dest_'+name.replace(/\s/g,'_').slice(0,20)+'_1'
    );
    const img2 = await pushImageToGitHub(
        document.getElementById('dest-img2-file'),
        document.getElementById('dest-img2-url'),
        'dest-github-status', 'dest_'+name.replace(/\s/g,'_').slice(0,20)+'_2'
    );
    const editId = document.getElementById('dest-edit-id').value;
    const item = {
        id: editId || genId(),
        name, img1, img2,
        category: document.getElementById('dest-category').value,
        rating: document.getElementById('dest-rating').value,
        mapsUrl: document.getElementById('dest-maps').value.trim(),
        linkUrl: document.getElementById('dest-link').value.trim(),
        descShort: document.getElementById('dest-desc-short').value.trim(),
        descLong: document.getElementById('dest-desc-long').value.trim(),
        highlights: document.getElementById('dest-highlights').value.split('\n').map(s=>s.trim()).filter(Boolean),
        bestTime: document.getElementById('dest-best-time').value.trim(),
    };
    let items = loadData(KEYS.adminDests);
    if(editId) { items = items.map(d=>d.id===editId ? item : d); }
    else { items.unshift(item); }
    saveData(KEYS.adminDests, items);
    renderAdminDestList();
    renderAdminDestCardsInTab1();
    hideDestForm();
}

function deleteDestination(id) {
    if(!confirm('Xóa địa điểm này?')) return;
    let items = loadData(KEYS.adminDests).filter(d=>d.id!==id);
    saveData(KEYS.adminDests, items);
    renderAdminDestList();
    renderAdminDestCardsInTab1();
}

function renderAdminDestList() {
    const items = loadData(KEYS.adminDests);
    const el = document.getElementById('admin-dest-list');
    if(!items.length) { el.innerHTML='<div class="text-center text-gray-400 py-8 text-sm"><i class="fa-solid fa-inbox text-3xl mb-2 block opacity-30"></i>Chưa có địa điểm nào được thêm.</div>'; return; }
    el.innerHTML = items.map(d=>`
        <div class="admin-item-row">
            ${d.img1?`<img src="${d.img1}" class="admin-item-thumb" onerror="this.style.display='none'">`:
            `<div class="admin-item-thumb bg-teal-50 flex items-center justify-center text-2xl">🌴</div>`}
            <div class="flex-grow min-w-0">
                <div class="font-bold text-gray-800 text-sm truncate">${d.name}</div>
                <div class="text-gray-400 text-xs truncate mt-0.5">${d.descShort||''}</div>
                <div class="flex items-center gap-2 mt-1">
                    ${d.rating?`<span class="text-amber-500 text-xs font-bold">⭐ ${d.rating}</span>`:''}
                    <span class="admin-badge bg-teal-50 text-teal-700 border border-teal-100">${d.category}</span>
                </div>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
                ${d.mapsUrl?`<a href="${d.mapsUrl}" target="_blank" class="text-teal-500 hover:text-teal-700 text-sm p-1.5" title="Xem Maps"><i class="fa-solid fa-map-location-dot"></i></a>`:''}
                <button onclick="showDestForm('${d.id}')" class="text-blue-500 hover:text-blue-700 text-sm p-1.5" title="Sửa"><i class="fa-solid fa-pen"></i></button>
                <button onclick="deleteDestination('${d.id}')" class="admin-btn-danger" title="Xóa"><i class="fa-solid fa-trash-can"></i></button>
            </div>
        </div>
    `).join('');
}

const DEST_CATEGORY_LABELS = {
    beach: '🏖 Bãi Tắm & Sinh Thái Biển',
    dive:  '🤿 Lặn Biển & Hải Đảo',
    history: '🏛 Di Tích Lịch Sử',
    spiritual: '🙏 Tâm Linh & Văn Hóa',
    nature: '🌿 Thiên Nhiên & Rừng',
};

function renderAdminDestCardsInTab1() {
    let container = document.getElementById('admin-added-dests');
    if(!container) {
        const destsContainer = document.getElementById('destinations-container');
        if(!destsContainer) return;
        container = document.createElement('div');
        container.id = 'admin-added-dests';
        destsContainer.parentNode.insertBefore(container, destsContainer);
    }
    const items = loadData(KEYS.adminDests);
    if(!items.length) { container.innerHTML=''; return; }
    container.innerHTML = `
        <div class="mb-4 flex items-center gap-2 text-xs font-bold text-teal-700 bg-teal-50 border border-teal-100 px-4 py-2 rounded-xl w-fit">
            <i class="fa-solid fa-star"></i> Địa điểm mới được thêm bởi Admin
        </div>
        <div class="grid grid-cols-1 gap-6 mb-8">
            ${items.map(d => renderDestCard(d)).join('')}
        </div>
    `;
    // Re-attach IntersectionObserver for new cards
    document.querySelectorAll('#admin-added-dests .destination-card').forEach(el => observer && observer.observe(el));
}

function renderDestCard(d) {
    const catLabel = DEST_CATEGORY_LABELS[d.category] || d.category;
    const highlights = (d.highlights||[]).map(h=>`<li>${h}</li>`).join('');
    const img1HTML = d.img1 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img1}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    const img2HTML = d.img2 ? `<div class="group/img overflow-hidden rounded-xl shadow-sm border border-gray-100 aspect-[4/3] relative">
        <img src="${d.img2}" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-500" alt="${d.name}">
    </div>` : '';
    const cardWrapper = d.linkUrl ? `onclick="window.open('${d.linkUrl}','_blank')"` : `onclick="toggleDestDetail(this)"`;
    return `
    <div class="destination-card p-4 md:p-6" ${cardWrapper}>
        <div class="flex flex-col md:flex-row gap-4 items-start">
            ${d.img1?`<div class="dest-img-container w-full md:w-56 shrink-0"><img src="${d.img1}" class="dest-img" alt="${d.name}"></div>`:''}
            <div class="flex-grow">
                <div class="flex flex-wrap items-center gap-2 mb-1">
                    <h3 class="text-lg font-extrabold text-gray-800">${d.name}</h3>
                    ${d.rating?`<span class="bg-amber-50 text-amber-700 border border-amber-100 text-xs font-bold px-2 py-0.5 rounded-full">⭐ ${d.rating}/5</span>`:''}
                    <span class="bg-teal-50 text-teal-700 border border-teal-100 text-xs font-bold px-2 py-0.5 rounded-full">${catLabel}</span>
                </div>
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
}

function toggleDestDetail(card) {
    const panel = card.querySelector('.detail-panel');
    if(!panel) return;
    const isOpen = panel.style.maxHeight && panel.style.maxHeight !== '0px';
    if(isOpen) {
        panel.style.maxHeight = '0'; panel.style.opacity = '0';
        panel.style.marginTop = '0'; panel.style.paddingTop = '0';
    } else {
        panel.style.maxHeight = panel.scrollHeight + 200 + 'px';
        panel.style.opacity = '1'; panel.style.marginTop = '1rem'; panel.style.paddingTop = '1rem';
    }
}

// ============================================================
// CMS: HOTELS
// ============================================================
function showHotelForm(id) {
    const area = document.getElementById('hotel-form-area');
    area.classList.remove('hidden');
    document.getElementById('hotel-form-title').textContent = id ? 'Chỉnh Sửa Lưu Trú' : 'Thêm Khách Sạn Mới';
    document.getElementById('hotel-edit-id').value = id || '';
    if(id) {
        const item = loadData(KEYS.adminHotels).find(h=>h.id===id);
        if(item) {
            ['name','stars','price','address','maps','link','desc','img-url'].forEach(f=>{
                const el = document.getElementById('hotel-'+f);
                if(el) el.value = item[f.replace('-url','Url').replace('-','').replace('maps','mapsUrl').replace('link','linkUrl')]||item[f]||'';
            });
            document.getElementById('hotel-name').value=item.name||'';
            document.getElementById('hotel-stars').value=item.stars||'3';
            document.getElementById('hotel-price').value=item.price||'';
            document.getElementById('hotel-address').value=item.address||'';
            document.getElementById('hotel-maps').value=item.mapsUrl||'';
            document.getElementById('hotel-link').value=item.linkUrl||'';
            document.getElementById('hotel-desc').value=item.desc||'';
            document.getElementById('hotel-img-url').value=item.imgUrl||'';
            if(item.imgUrl){ document.getElementById('hotel-img-preview').src=item.imgUrl; document.getElementById('hotel-img-preview').classList.remove('hidden');}
        }
    } else {
        ['hotel-name','hotel-price','hotel-address','hotel-maps','hotel-link','hotel-desc','hotel-img-url'].forEach(id2=>document.getElementById(id2).value='');
        document.getElementById('hotel-img-preview').src=''; document.getElementById('hotel-img-preview').classList.add('hidden');
    }
    area.scrollIntoView({behavior:'smooth'});
}

function hideHotelForm() { document.getElementById('hotel-form-area').classList.add('hidden'); }

async function saveHotel() {
    const name = document.getElementById('hotel-name').value.trim();
    if(!name){ alert('Vui lòng nhập tên!'); return; }
    const imgUrl = await pushImageToGitHub(
        document.getElementById('hotel-img-file'),
        document.getElementById('hotel-img-url'),
        'hotel-github-status', 'hotel_'+name.replace(/\s/g,'_').slice(0,20)
    );
    const editId = document.getElementById('hotel-edit-id').value;
    const item = {
        id: editId||genId(), name, imgUrl,
        stars: document.getElementById('hotel-stars').value,
        price: document.getElementById('hotel-price').value.trim(),
        address: document.getElementById('hotel-address').value.trim(),
        mapsUrl: document.getElementById('hotel-maps').value.trim(),
        linkUrl: document.getElementById('hotel-link').value.trim(),
        desc: document.getElementById('hotel-desc').value.trim(),
    };
    let items = loadData(KEYS.adminHotels);
    if(editId) items = items.map(h=>h.id===editId?item:h); else items.unshift(item);
    saveData(KEYS.adminHotels, items);
    renderAdminHotelList();
    renderAdminHotelsInTab3();
    hideHotelForm();
}

function deleteHotel(id) {
    if(!confirm('Xóa lưu trú này?')) return;
    saveData(KEYS.adminHotels, loadData(KEYS.adminHotels).filter(h=>h.id!==id));
    renderAdminHotelList();
    renderAdminHotelsInTab3();
}

function renderAdminHotelList() {
    const items = loadData(KEYS.adminHotels);
    const el = document.getElementById('admin-hotel-list');
    if(!items.length){ el.innerHTML='<div class="text-center text-gray-400 py-8 text-sm"><i class="fa-solid fa-inbox text-3xl mb-2 block opacity-30"></i>Chưa có lưu trú nào được thêm.</div>'; return; }
    el.innerHTML = items.map(h=>`
        <div class="admin-item-row">
            ${h.imgUrl?`<img src="${h.imgUrl}" class="admin-item-thumb" onerror="this.style.display='none'">`:`<div class="admin-item-thumb bg-blue-50 flex items-center justify-center text-2xl">🏨</div>`}
            <div class="flex-grow min-w-0">
                <div class="font-bold text-gray-800 text-sm">${h.name}</div>
                <div class="text-gray-400 text-xs mt-0.5">${h.address||''}</div>
                <div class="flex items-center gap-2 mt-1">
                    <span class="admin-badge bg-amber-50 text-amber-700 border border-amber-100">${h.stars} ★</span>
                    <span class="text-teal-600 text-xs font-bold">${h.price||''}</span>
                </div>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
                ${h.linkUrl?`<a href="${h.linkUrl}" target="_blank" class="text-green-500 hover:text-green-700 text-sm p-1.5" title="Booking"><i class="fa-solid fa-link"></i></a>`:''}
                <button onclick="showHotelForm('${h.id}')" class="text-blue-500 hover:text-blue-700 text-sm p-1.5"><i class="fa-solid fa-pen"></i></button>
                <button onclick="deleteHotel('${h.id}')" class="admin-btn-danger"><i class="fa-solid fa-trash-can"></i></button>
            </div>
        </div>
    `).join('');
}

function renderAdminHotelsInTab3() {
    let container = document.getElementById('admin-added-hotels');
    const hotelScrollDiv = document.querySelector('#tab3 .flex-grow.overflow-y-auto');
    if(!hotelScrollDiv) return;
    if(!container) {
        container = document.createElement('div');
        container.id = 'admin-added-hotels';
        hotelScrollDiv.prepend(container);
    }
    const items = loadData(KEYS.adminHotels);
    if(!items.length){ container.innerHTML=''; return; }
    container.innerHTML = items.map(h=>`
        <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl flex flex-col sm:flex-row gap-4 transition-all duration-300 shadow-sm hover:shadow-md group ${h.linkUrl?'cursor-pointer':''}"
            ${h.linkUrl?`onclick="window.open('${h.linkUrl}','_blank')"`:''}>
            <div class="w-full sm:w-32 h-24 rounded-lg overflow-hidden shrink-0 shadow-sm relative">
                <img src="${h.imgUrl||'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400'}" alt="${h.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'">
                <span class="absolute top-1 left-1 bg-amber-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm">${h.stars} ★</span>
            </div>
            <div class="flex-grow flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start gap-2">
                        <h4 class="font-bold text-gray-800 group-hover:text-teal-700 transition-colors text-sm sm:text-base">${h.name}</h4>
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
    `).join('');
}

// ============================================================
// CMS: FOOD
// ============================================================
function showFoodForm(id) {
    const area = document.getElementById('food-form-area');
    area.classList.remove('hidden');
    document.getElementById('food-form-title').textContent = id ? 'Chỉnh Sửa Ẩm Thực' : 'Thêm Món Ăn / Quán Mới';
    document.getElementById('food-edit-id').value = id || '';
    if(id) {
        const item = loadData(KEYS.adminFood).find(f=>f.id===id);
        if(item) {
            document.getElementById('food-name').value=item.name||'';
            document.getElementById('food-category').value=item.category||'seafood';
            document.getElementById('food-address').value=item.address||'';
            document.getElementById('food-maps').value=item.mapsUrl||'';
            document.getElementById('food-link').value=item.linkUrl||'';
            document.getElementById('food-desc').value=item.desc||'';
            document.getElementById('food-img-url').value=item.imgUrl||'';
            if(item.imgUrl){ document.getElementById('food-img-preview').src=item.imgUrl; document.getElementById('food-img-preview').classList.remove('hidden'); }
        }
    } else {
        ['food-name','food-address','food-maps','food-link','food-desc','food-img-url'].forEach(id2=>document.getElementById(id2).value='');
        document.getElementById('food-img-preview').src=''; document.getElementById('food-img-preview').classList.add('hidden');
    }
    area.scrollIntoView({behavior:'smooth'});
}

function hideFoodForm() { document.getElementById('food-form-area').classList.add('hidden'); }

async function saveFood() {
    const name = document.getElementById('food-name').value.trim();
    if(!name){ alert('Vui lòng nhập tên!'); return; }
    const imgUrl = await pushImageToGitHub(
        document.getElementById('food-img-file'),
        document.getElementById('food-img-url'),
        'food-github-status', 'food_'+name.replace(/\s/g,'_').slice(0,20)
    );
    const editId = document.getElementById('food-edit-id').value;
    const item = {
        id: editId||genId(), name, imgUrl,
        category: document.getElementById('food-category').value,
        address: document.getElementById('food-address').value.trim(),
        mapsUrl: document.getElementById('food-maps').value.trim(),
        linkUrl: document.getElementById('food-link').value.trim(),
        desc: document.getElementById('food-desc').value.trim(),
    };
    let items = loadData(KEYS.adminFood);
    if(editId) items = items.map(f=>f.id===editId?item:f); else items.unshift(item);
    saveData(KEYS.adminFood, items);
    renderAdminFoodList();
    renderAdminFoodInTab4();
    hideFoodForm();
}

function deleteFood(id) {
    if(!confirm('Xóa mục ẩm thực này?')) return;
    saveData(KEYS.adminFood, loadData(KEYS.adminFood).filter(f=>f.id!==id));
    renderAdminFoodList();
    renderAdminFoodInTab4();
}

function renderAdminFoodList() {
    const items = loadData(KEYS.adminFood);
    const el = document.getElementById('admin-food-list');
    if(!items.length){ el.innerHTML='<div class="text-center text-gray-400 py-8 text-sm"><i class="fa-solid fa-inbox text-3xl mb-2 block opacity-30"></i>Chưa có món ăn nào được thêm.</div>'; return; }
    el.innerHTML = items.map(f=>`
        <div class="admin-item-row">
            ${f.imgUrl?`<img src="${f.imgUrl}" class="admin-item-thumb" onerror="this.style.display='none'">`:`<div class="admin-item-thumb bg-orange-50 flex items-center justify-center text-2xl">🍜</div>`}
            <div class="flex-grow min-w-0">
                <div class="font-bold text-gray-800 text-sm">${f.name}</div>
                <div class="text-gray-400 text-xs mt-0.5 truncate">${f.address||''}</div>
                <span class="admin-badge bg-orange-50 text-orange-700 border border-orange-100 mt-1 inline-block">${f.category}</span>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
                ${f.mapsUrl?`<a href="${f.mapsUrl}" target="_blank" class="text-teal-500 hover:text-teal-700 text-sm p-1.5"><i class="fa-solid fa-map-location-dot"></i></a>`:''}
                <button onclick="showFoodForm('${f.id}')" class="text-blue-500 hover:text-blue-700 text-sm p-1.5"><i class="fa-solid fa-pen"></i></button>
                <button onclick="deleteFood('${f.id}')" class="admin-btn-danger"><i class="fa-solid fa-trash-can"></i></button>
            </div>
        </div>
    `).join('');
}

const FOOD_CAT_ICONS = { seafood:'🦞', specialty:'🌟', cafe:'☕', restaurant:'🍽', street:'🛵' };
const FOOD_CAT_DATA = { seafood:'seafood', specialty:'specialty', cafe:'cafe', restaurant:'restaurant', street:'street' };

function renderAdminFoodInTab4() {
    let container = document.getElementById('admin-added-food');
    const foodContainer = document.getElementById('food-container');
    if(!foodContainer) return;
    if(!container) {
        container = document.createElement('div');
        container.id = 'admin-added-food';
        foodContainer.parentNode.insertBefore(container, foodContainer);
    }
    const items = loadData(KEYS.adminFood);
    if(!items.length){ container.innerHTML=''; return; }
    container.innerHTML = items.map(f=>`
        <div class="food-card bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden group transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${f.linkUrl?'cursor-pointer':''}"
            data-category="${f.category}" ${f.linkUrl?`onclick="window.open('${f.linkUrl}','_blank')"`:''}> 
            <div class="relative overflow-hidden aspect-video">
                <img src="${f.imgUrl||'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600'}" alt="${f.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" onerror="this.src='https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600'">
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <span class="absolute top-3 left-3 bg-white/90 backdrop-blur-sm text-gray-700 text-xs font-bold px-2.5 py-1 rounded-full">${FOOD_CAT_ICONS[f.category]||'🍴'} ${f.category}</span>
            </div>
            <div class="p-4">
                <h3 class="font-extrabold text-gray-800 text-base group-hover:text-teal-700 transition-colors mb-1">${f.name}</h3>
                ${f.address?`<p class="text-xs text-gray-400 flex items-center gap-1 mb-2"><i class="fa-solid fa-location-dot text-teal-500"></i> ${f.address}</p>`:''}
                ${f.desc?`<p class="text-xs text-gray-600 leading-relaxed mb-3">${f.desc}</p>`:''}
                <div class="flex items-center gap-2">
                    ${f.mapsUrl?`<a href="${f.mapsUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-teal-600 hover:text-teal-800 font-semibold flex items-center gap-1 transition-colors"><i class="fa-solid fa-map-location-dot"></i> Maps</a>`:''}
                    ${f.linkUrl?`<a href="${f.linkUrl}" target="_blank" onclick="event.stopPropagation()" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1 transition-colors ml-auto"><i class="fa-solid fa-star"></i> Review</a>`:''}
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================================
// CMS: MEMORIES
// ============================================================
function checkMemPass() {
    const input = document.getElementById('mem-pass-input').value;
    const stored = localStorage.getItem(KEYS.memPass) || simpleHash(DEFAULT_MEM_PASSWORD);
    if(simpleHash(input) === stored) {
        sessionStorage.setItem('memoriesUnlocked','yes');
        document.getElementById('mem-gate').classList.add('hidden');
        document.getElementById('mem-content').classList.remove('hidden');
        document.getElementById('mem-pass-err').classList.add('hidden');
        renderMemoryAlbums();
    } else {
        document.getElementById('mem-pass-err').classList.remove('hidden');
        document.getElementById('mem-pass-input').value='';
        document.getElementById('mem-pass-input').focus();
    }
}

function renderMemoryAlbums() {
    const data = loadData(KEYS.memories, {albums:[]});
    const grid = document.getElementById('memories-album-grid');
    const empty = document.getElementById('mem-empty-state');
    if(!data.albums||!data.albums.length) {
        grid.innerHTML=''; empty.classList.remove('hidden'); return;
    }
    empty.classList.add('hidden');
    grid.innerHTML = data.albums.map(album=>`
        <div class="memory-album-card" onclick="openAlbum('${album.id}')">
            <div style="aspect-ratio:4/3;overflow:hidden;background:linear-gradient(135deg,#0f172a,#134e4a)">
                ${album.cover?`<img src="${getEmbedUrl(album.cover,'thumb')}" class="w-full h-full object-cover" onerror="this.style.display='none'">`:''}
                ${!album.cover?`<div class="w-full h-full flex items-center justify-center text-5xl">${album.emoji||'📸'}</div>`:''}
            </div>
            <div class="p-4">
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-2xl">${album.emoji||'📸'}</span>
                    <h3 class="font-extrabold text-gray-800 text-base">${album.name}</h3>
                </div>
                ${album.desc?`<p class="text-gray-500 text-xs">${album.desc}</p>`:''}
                <div class="flex items-center gap-1 mt-2 text-xs text-gray-400">
                    <i class="fa-solid fa-images"></i>
                    <span>${(album.items||[]).length} mục</span>
                </div>
            </div>
        </div>
    `).join('');
}

function openAlbum(albumId) {
    const data = loadData(KEYS.memories, {albums:[]});
    const album = (data.albums||[]).find(a=>a.id===albumId);
    if(!album) return;
    document.getElementById('memories-album-grid').classList.add('hidden');
    document.getElementById('mem-album-detail').classList.remove('hidden');
    document.getElementById('mem-album-title').innerHTML = `<span class="mr-2">${album.emoji||'📸'}</span>${album.name}`;
    document.getElementById('mem-album-desc').textContent = album.desc||'';
    const grid = document.getElementById('mem-album-items-grid');
    if(!album.items||!album.items.length) {
        grid.innerHTML='<div class="text-gray-400 text-sm py-8 text-center col-span-full"><i class="fa-solid fa-images text-3xl mb-2 block opacity-30"></i>Album chưa có ảnh/video nào.</div>';
        return;
    }
    grid.innerHTML = album.items.map((item,idx)=>{
        if(item.type==='video') return `
            <div class="memory-video-item">
                <iframe src="${getEmbedUrl(item.url,'video')}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                ${item.caption?`<div class="memory-media-caption">${item.caption}</div>`:''}
            </div>`;
        return `
            <div class="memory-media-item" onclick="openLightbox('${item.url.replace(/'/g,"\\'")}','${(item.caption||'').replace(/'/g,"\\'")}')">
                <img src="${getEmbedUrl(item.url,'thumb')}" alt="${item.caption||''}" loading="lazy" onerror="this.src='https://via.placeholder.com/200x200?text=No+Image'">
                ${item.caption?`<div class="memory-media-caption">${item.caption}</div>`:''}
            </div>`;
    }).join('');
}

function closeAlbumDetail() {
    document.getElementById('mem-album-detail').classList.add('hidden');
    document.getElementById('memories-album-grid').classList.remove('hidden');
}

function getEmbedUrl(url, type) {
    if(!url) return '';
    // YouTube
    const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\?]+)/);
    if(ytMatch) {
        if(type==='video') return `https://www.youtube.com/embed/${ytMatch[1]}`;
        return `https://img.youtube.com/vi/${ytMatch[1]}/hqdefault.jpg`;
    }
    // Google Drive view link → embed/thumbnail
    const driveMatch = url.match(/drive\.google\.com\/file\/d\/([^\/]+)/);
    if(driveMatch) {
        const id = driveMatch[1];
        if(type==='video') return `https://drive.google.com/file/d/${id}/preview`;
        return `https://drive.google.com/thumbnail?id=${id}&sz=w400`;
    }
    // Google Drive open link
    const driveOpen = url.match(/drive\.google\.com\/open\?id=([^&]+)/);
    if(driveOpen) {
        const id = driveOpen[1];
        if(type==='video') return `https://drive.google.com/file/d/${id}/preview`;
        return `https://drive.google.com/thumbnail?id=${id}&sz=w400`;
    }
    return url;
}

// Admin: Memories CRUD
function renderAdminMemList() {
    const data = loadData(KEYS.memories, {albums:[]});
    const el = document.getElementById('admin-mem-list');
    if(!data.albums||!data.albums.length) {
        el.innerHTML='<div class="text-center text-gray-400 py-8 text-sm"><i class="fa-solid fa-inbox text-3xl mb-2 block opacity-30"></i>Chưa có album nào.</div>';
        return;
    }
    el.innerHTML = data.albums.map(album=>`
        <div class="bg-white border border-gray-200 rounded-2xl p-4 mb-4 shadow-sm">
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <span class="text-2xl">${album.emoji||'📸'}</span>
                    <div>
                        <div class="font-extrabold text-gray-800">${album.name}</div>
                        <div class="text-xs text-gray-400">${(album.items||[]).length} mục</div>
                    </div>
                </div>
                <button onclick="deleteAlbum('${album.id}')" class="admin-btn-danger text-xs">
                    <i class="fa-solid fa-trash-can"></i> Xóa Album
                </button>
            </div>
            <!-- Add item to this album -->
            <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
                <div class="text-xs font-bold text-gray-500 mb-2 uppercase tracking-widest">Thêm Ảnh / Video</div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mb-2">
                    <select id="mem-item-type-${album.id}" class="admin-form-input">
                        <option value="photo">🖼 Ảnh</option>
                        <option value="video">▶ Video (YouTube/Drive)</option>
                    </select>
                    <input id="mem-item-url-${album.id}" type="url" class="admin-form-input" placeholder="URL ảnh / YouTube / Google Drive link">
                    <input id="mem-item-cap-${album.id}" type="text" class="admin-form-input" placeholder="Chú thích (tùy chọn)">
                </div>
                <button onclick="addMemItem('${album.id}')" class="admin-btn-primary text-xs py-1.5">
                    <i class="fa-solid fa-plus"></i> Thêm Vào Album
                </button>
            </div>
            <!-- Items list -->
            ${(album.items||[]).length?`
            <div class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-2">
                ${album.items.map(item=>`
                    <div class="relative rounded-xl overflow-hidden aspect-square bg-gray-100 group">
                        <img src="${getEmbedUrl(item.url,'thumb')}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/100?text=...'">
                        ${item.type==='video'?'<div class="absolute inset-0 flex items-center justify-center"><i class="fa-solid fa-play text-white text-xl opacity-80"></i></div>':''}
                        <button onclick="deleteMemItem('${album.id}','${item.id}')" class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 text-xs hidden group-hover:flex items-center justify-center">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                `).join('')}
            </div>`:''}
        </div>
    `).join('');
}

function showAlbumForm() { document.getElementById('album-form-area').classList.remove('hidden'); }
function hideAlbumForm() { document.getElementById('album-form-area').classList.add('hidden'); }

function createAlbum() {
    const name = document.getElementById('album-name').value.trim();
    if(!name){ alert('Vui lòng nhập tên album!'); return; }
    const data = loadData(KEYS.memories, {albums:[]});
    data.albums.push({
        id: genId(),
        name,
        emoji: document.getElementById('album-emoji').value.trim()||'📸',
        desc: document.getElementById('album-desc').value.trim(),
        cover: document.getElementById('album-cover').value.trim(),
        items: []
    });
    saveData(KEYS.memories, data);
    renderAdminMemList();
    hideAlbumForm();
    ['album-name','album-emoji','album-desc','album-cover'].forEach(id=>document.getElementById(id).value='');
}

function deleteAlbum(albumId) {
    if(!confirm('Xóa album này và toàn bộ nội dung bên trong?')) return;
    const data = loadData(KEYS.memories, {albums:[]});
    data.albums = data.albums.filter(a=>a.id!==albumId);
    saveData(KEYS.memories, data);
    renderAdminMemList();
}

function addMemItem(albumId) {
    const type = document.getElementById(`mem-item-type-${albumId}`).value;
    const url = document.getElementById(`mem-item-url-${albumId}`).value.trim();
    const caption = document.getElementById(`mem-item-cap-${albumId}`).value.trim();
    if(!url){ alert('Vui lòng nhập URL!'); return; }
    const data = loadData(KEYS.memories, {albums:[]});
    const album = data.albums.find(a=>a.id===albumId);
    if(!album) return;
    album.items.push({ id: genId(), type, url, caption });
    saveData(KEYS.memories, data);
    renderAdminMemList();
    document.getElementById(`mem-item-url-${albumId}`).value='';
    document.getElementById(`mem-item-cap-${albumId}`).value='';
}

function deleteMemItem(albumId, itemId) {
    const data = loadData(KEYS.memories, {albums:[]});
    const album = data.albums.find(a=>a.id===albumId);
    if(!album) return;
    album.items = album.items.filter(i=>i.id!==itemId);
    saveData(KEYS.memories, data);
    renderAdminMemList();
}

// ============================================================
// GITHUB CONFIG
// ============================================================
function loadGithubConfigToForm() {
    const token = localStorage.getItem(KEYS.ghToken)||'';
    const config = loadData(KEYS.ghConfig, {repo:'LarryVan-engin/Some_stuff_case', branch:'main', path:'condao/images/'});
    if(document.getElementById('gh-token')) document.getElementById('gh-token').value=token;
    if(document.getElementById('gh-repo')) document.getElementById('gh-repo').value=config.repo||'LarryVan-engin/Some_stuff_case';
    if(document.getElementById('gh-branch')) document.getElementById('gh-branch').value=config.branch||'main';
    if(document.getElementById('gh-path')) document.getElementById('gh-path').value=config.path||'condao/images/';
}

function saveGithubConfig() {
    const token = document.getElementById('gh-token').value.trim();
    const config = {
        repo: document.getElementById('gh-repo').value.trim(),
        branch: document.getElementById('gh-branch').value.trim(),
        path: document.getElementById('gh-path').value.trim(),
    };
    if(token) localStorage.setItem(KEYS.ghToken, token);
    saveData(KEYS.ghConfig, config);
    showTestResult('gh-test-result', true, '✅ Đã lưu cài đặt GitHub!');
}

async function testGithubConfig() {
    const token = document.getElementById('gh-token').value.trim();
    const repo = document.getElementById('gh-repo').value.trim();
    const el = document.getElementById('gh-test-result');
    el.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin mr-1"></i> Đang kiểm tra...'; el.className='text-xs rounded-lg px-3 py-2 bg-gray-50 text-gray-600'; el.classList.remove('hidden');
    try {
        const resp = await fetch(`https://api.github.com/repos/${repo}`, { headers:{ Authorization: `token ${token}` } });
        const data = await resp.json();
        if(resp.ok) showTestResult('gh-test-result', true, `✅ Kết nối thành công! Repo: ${data.full_name} (${data.private?'Private':'Public'})`);
        else showTestResult('gh-test-result', false, `❌ Lỗi: ${data.message}`);
    } catch(e) {
        showTestResult('gh-test-result', false, `❌ Không thể kết nối: ${e.message}`);
    }
}

function showTestResult(elId, success, msg) {
    const el = document.getElementById(elId);
    if(!el) return;
    el.classList.remove('hidden');
    el.className = `text-xs rounded-lg px-3 py-2 ${success?'bg-green-50 text-green-700 border border-green-100':'bg-red-50 text-red-700 border border-red-100'}`;
    el.innerHTML = msg;
}

// ============================================================
// MEMORY PASSWORD CHANGE
// ============================================================
function changeMemoryPass() {
    const np = document.getElementById('new-mem-pass').value;
    const cp = document.getElementById('confirm-mem-pass').value;
    if(!np){ showTestResult('mem-pass-change-result', false, 'Vui lòng nhập mật khẩu mới!'); return; }
    if(np !== cp){ showTestResult('mem-pass-change-result', false, '❌ Mật khẩu xác nhận không khớp!'); return; }
    localStorage.setItem(KEYS.memPass, simpleHash(np));
    document.getElementById('new-mem-pass').value='';
    document.getElementById('confirm-mem-pass').value='';
    showTestResult('mem-pass-change-result', true, '✅ Đổi mật khẩu Tab Kỷ Niệm thành công!');
}

// ============================================================
// EXPORT / IMPORT CMS DATA
// ============================================================
function exportCMSData() {
    const backup = {
        destinations: loadData(KEYS.adminDests),
        hotels: loadData(KEYS.adminHotels),
        food: loadData(KEYS.adminFood),
        memories: loadData(KEYS.memories, {albums:[]}),
        exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(backup, null, 2)], {type:'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `condao_cms_backup_${Date.now()}.json`;
    link.click();
}

function importCMSData(event) {
    const file = event.target.files[0];
    if(!file) return;
    const reader = new FileReader();
    reader.onload = e => {
        try {
            const data = JSON.parse(e.target.result);
            if(data.destinations) saveData(KEYS.adminDests, data.destinations);
            if(data.hotels) saveData(KEYS.adminHotels, data.hotels);
            if(data.food) saveData(KEYS.adminFood, data.food);
            if(data.memories) saveData(KEYS.memories, data.memories);
            alert('✅ Import thành công! Tải lại trang để thấy thay đổi.');
            showAdminSection(adminCurrentSection);
            renderAdminDestCardsInTab1();
            renderAdminHotelsInTab3();
            renderAdminFoodInTab4();
        } catch(err) {
            alert('❌ File JSON không hợp lệ: ' + err.message);
        }
    };
    reader.readAsText(file);
}

// ============================================================
// LIGHTBOX
// ============================================================
function openLightbox(imgUrl, caption) {
    document.getElementById('lightbox-img').src = imgUrl;
    document.getElementById('lightbox-caption').textContent = caption||'';
    document.getElementById('lightbox-overlay').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeLightbox(e) {
    if(e && e.target !== document.getElementById('lightbox-overlay')) return;
    closeLightboxBtn();
}

function closeLightboxBtn() {
    document.getElementById('lightbox-overlay').classList.add('hidden');
    document.body.style.overflow = '';
}

// ESC key closes lightbox
document.addEventListener('keydown', e => {
    if(e.key==='Escape') {
        closeLightboxBtn();
        closeAdminModal();
    }
});

// ============================================================
// ON LOAD: Render admin-added items into tabs
// ============================================================
(function initAdminItems() {
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
    // Render admin-added content into existing tabs
    renderAdminDestCardsInTab1();
    renderAdminHotelsInTab3();
    renderAdminFoodInTab4();
})();
"""

html = html.replace('    </script>', NEW_JS + '\n    </script>', 1)
print("JavaScript inserted OK")

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! New file: {len(html)} chars")
print("Backup: file was originally 335402 chars")
