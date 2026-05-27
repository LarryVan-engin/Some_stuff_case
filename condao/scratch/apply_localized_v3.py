# -*- coding: utf-8 -*-
import os
import shutil
import re
import json

def replace_js_function(content, func_name, replacement):
    idx = content.find(f"function {func_name}(")
    if idx == -1:
        return content
    
    start_brace = content.find("{", idx)
    if start_brace == -1:
        return content
    
    brace_count = 1
    i = start_brace + 1
    while i < len(content) and brace_count > 0:
        if content[i] == "{":
            brace_count += 1
        elif content[i] == "}":
            brace_count -= 1
        i += 1
        
    if brace_count == 0:
        return content[:idx] + replacement + content[i:]
    return content

def replace_variable_declaration(content, var_name, replacement_str):
    idx = content.find(f"const {var_name} =")
    if idx == -1:
        idx = content.find(f"let {var_name} =")
    if idx == -1:
        return content
        
    # Find whether the next non-whitespace char is [ or {
    search_pos = idx + len(f"const {var_name} =")
    if content.find(f"let {var_name} =") != -1:
        search_pos = idx + len(f"let {var_name} =")
        
    # Skip whitespace
    while search_pos < len(content) and content[search_pos].isspace():
        search_pos += 1
        
    if search_pos >= len(content):
        return content
        
    start_char = content[search_pos]
    if start_char not in ["[", "{"]:
        return content
        
    end_char = "]" if start_char == "[" else "}"
    
    count = 1
    i = search_pos + 1
    while i < len(content) and count > 0:
        if content[i] == start_char:
            count += 1
        elif content[i] == end_char:
            count -= 1
        i += 1
        
    if count == 0:
        semicolon = content.find(";", i)
        end_idx = i
        if semicolon != -1 and (semicolon - i) < 5:
            end_idx = semicolon + 1
        return content[:idx] + f"const {var_name} = {replacement_str};" + content[end_idx:]
    return content

# Define all the rich localized data blocks
DALAT_DESTS = [
    {
        "id": "dalat_dest_1", "name": "Đỉnh Langbiang", "category": "nature", "rating": "4.6",
        "img1": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "tags": ["Nóc_nhà_Đà_Lạt", "Săn_mây", "Trekking"],
        "descShort": "Đỉnh núi cao nhất Đà Lạt, địa điểm ngắm toàn cảnh hồ Đan Kia lấp ló dưới màn sương mù bồng bềnh tuyệt đẹp.",
        "descLong": "Đứng từ đỉnh Langbiang huyền thoại, ngắm nhìn toàn cảnh thung lũng, mây trắng bồng bềnh trôi lững lờ dưới chân đồi mang lại cảm giác chinh phục thiên nhiên cực kỳ sảng khoái cho chuyến đi.",
        "highlights": ["Đi xe Jeep xuyên rừng thông", "Săn mây vào sáng sớm tinh sương", "Ngắm toàn cảnh thung lũng từ trên cao"],
        "bestTime": "Nên ghé lúc sáng sớm từ 5h30 để đón biển mây lãng mạn.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Đỉnh+Langbiang+Đà+Lạt", "linkUrl": "", "isDefault": True
    },
    {
        "id": "dalat_dest_2", "name": "Hồ Tuyền Lâm", "category": "nature", "rating": "4.8",
        "img1": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "tags": ["Chèo_SUP", "Hoàng_hôn_tím", "Hồ_nước_ngọt"],
        "descShort": "Hồ nước ngọt lớn nhất Đà Lạt được bao quanh bởi rừng thông xanh rì, không gian tĩnh lặng, trong lành tuyệt mỹ.",
        "descLong": "Trải nghiệm chèo thuyền SUP đón hoàng hôn tím buông xuống mặt hồ phẳng lặng như gương hoặc viếng thăm Thiền Viện Trúc Lâm thanh tịnh gần đó.",
        "highlights": ["Chèo thuyền SUP thư giãn đón hoàng hôn", "Cắm trại ven rừng thông phẳng lặng", "Viếng Thiền Viện Trúc Lâm"],
        "bestTime": "Khoảng 16h00 - 17h30 chiều mát ngắm hoàng hôn buông lãng mạn.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Hồ+Tuyền+Lâm+Đà+Lạt", "linkUrl": "", "isDefault": True
    },
    {
        "id": "dalat_dest_3", "name": "Ga Đà Lạt", "category": "history", "rating": "4.4",
        "img1": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "tags": ["Kiến_trúc_Pháp", "Ga_cổ_kính", "Checkin_đẹp"],
        "descShort": "Nhà ga xe lửa cổ kính nhất Đông Dương mang đậm phong cách kiến trúc Pháp cổ điển pha trộn văn hóa bản địa.",
        "descLong": "Nơi lưu giữ các đầu máy hơi nước xưa cũ đầy hoài cổ. Du khách có thể trải nghiệm mua vé tàu chạy ga Trại Mát ngắm đồi dốc lãng mạn.",
        "highlights": ["Chụp hình đầu máy xe lửa hơi nước hoài cổ", "Chiêm ngưỡng kiến trúc ga mái chóp ấn tượng", "Trải nghiệm đi tàu lửa cổ ra Trại Mát"],
        "bestTime": "Nên đi vào ban ngày lúc trời nhiều nắng chụp ảnh rực rỡ.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Ga+Đà+Lạt", "linkUrl": "", "isDefault": True
    },
    {
        "id": "dalat_dest_4", "name": "Chùa Linh Phước (Chùa Ve Chai)", "category": "spiritual", "rating": "4.7",
        "img1": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80",
        "tags": ["Khảm_sành_sứ", "Chùa_Ve_Chai", "Tâm_linh_thiêng"],
        "descShort": "Ngôi chùa độc đáo khảm từ hàng triệu mảnh sành sứ, chai lọ đầy tinh xảo, sở hữu bức tượng Phật hoa bất tử.",
        "descLong": "Kiến trúc khảm sành vô cùng rực rỡ và tráng lệ. Nơi thờ bức tượng Quan Thế Âm làm bằng hàng vạn đóa hoa bất tử ghi dấu kỷ lục Việt Nam.",
        "highlights": ["Chiêm ngưỡng tháp chuông cao nhất Việt Nam", "Viếng tượng Phật Hoa Bất Tử rực rỡ", "Khám phá 18 tầng địa ngục đầy huyền bí"],
        "bestTime": "Nên đi buổi sáng mát mẻ vãn cảnh chùa tôn nghiêm.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Chùa+Linh+Phước+Đà+Lạt", "linkUrl": "", "isDefault": True
    },
    {
        "id": "dalat_dest_5", "name": "Quảng trường Lâm Viên", "category": "nature", "rating": "4.5",
        "img1": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "tags": ["Nụ_hoa_Atiso", "Bông_dã_quỳ", "Trái_tim_phố"],
        "descShort": "Không gian sinh hoạt rộng lớn hướng ra hồ Xuân Hương thơ mộng, mang biểu tượng nụ hoa Atiso khổng lồ.",
        "descLong": "Quảng trường Lâm Viên là trái tim của thành phố ngàn hoa với hai công trình biểu tượng nụ hoa Atiso và đóa dã quỳ bằng kính màu cực kỳ lộng lẫy.",
        "highlights": ["Check-in nụ hoa Atiso bằng kính khổng lồ", "Dạo mát ngắm hồ Xuân Hương phẳng lặng", "Thưởng thức sữa đậu nành nóng hổi ven đường"],
        "bestTime": "Chiều mát lộng gió hoặc buổi tối ngập tràn ánh đèn lung linh.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Quảng+trường+Lâm+Viên+Đà+Lạt", "linkUrl": "", "isDefault": True
    }
]

DALAT_HOTELS = [
    {
        "id": "dalat_hotel_1", "name": "Hotel Colline", "stars": "4", "price": "Từ 1.200.000 VNĐ",
        "address": "10 Phan Bội Châu, Phường 1, Đà Lạt",
        "desc": "Kiến trúc Bắc Âu hiện đại xếp chồng ấn tượng ngay trung tâm chợ Đà Lạt, cực kỳ tiện nghi, sang trọng.",
        "imgUrl": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Hotel+Colline+Dalat", "linkUrl": "", "isDefault": True
    },
    {
        "id": "dalat_hotel_2", "name": "Terracotta Hotel & Resort", "stars": "4", "price": "Từ 1.600.000 VNĐ",
        "address": "KDL Hồ Tuyền Lâm, Phường 3, Đà Lạt",
        "desc": "Khu nghỉ dưỡng ẩn mình dưới rừng thông ven hồ Tuyền Lâm phẳng lặng như gương, không gian thơ mộng, mát lành.",
        "imgUrl": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Terracotta+Hotel+Resort+Dalat", "linkUrl": "", "isDefault": True
    }
]

DALAT_FOOD = [
    {
        "id": "dalat_food_1", "name": "Lẩu Gà Lá É Tao Ngộ", "category": "specialty", "address": "Số 5 Đường 3/4, Phường 3, Đà Lạt",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Lẩu+Gà+Lá+É+Tao+Ngộ+Dalat", "linkUrl": "",
        "desc": "Vị ngọt thanh của thịt gà đồi săn chắc hòa cùng vị the mát độc đáo của lá é nghi ngút khói trong tiết lạnh Đà Lạt.",
        "imgUrl": "https://images.unsplash.com/photo-1548943487-a2e4b43b5930?w=800&q=80", "isDefault": True
    },
    {
        "id": "dalat_food_2", "name": "Bánh mì xíu mại chén Hoàng Diệu", "category": "specialty", "address": "26 Hoàng Diệu, Phường 5, Đà Lạt",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bánh+mì+xíu+mại+Hoàng+Diệu+Dalat", "linkUrl": "",
        "desc": "Bánh mì giòn nóng hổi chấm nước dùng xíu mại ngọt từ xương, viên xíu mại béo ngậy kèm chả huế thơm lừng.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    },
    {
        "id": "dalat_food_3", "name": "Lẩu Bò Ba Toa Nhà Gỗ", "category": "specialty", "address": "29/1 Hoàng Diệu, Phường 5, Đà Lạt",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Lẩu+Bò+Ba+Toa+Nhà+Gỗ+Dalat", "linkUrl": "",
        "desc": "Nồi lẩu bò đầy đặn sườn sụn béo ngậy ngọt nước, rau xà lách nhúng lẩu cực giòn ngọt mát ngọt ngào.",
        "imgUrl": "https://images.unsplash.com/photo-1548943487-a2e4b43b5930?w=800&q=80", "isDefault": True
    },
    {
        "id": "dalat_food_4", "name": "Bánh Căn Lệ", "category": "street", "address": "27/44 Yersin, Phường 10, Đà Lạt",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bánh+Căn+Lệ+Dalat", "linkUrl": "",
        "desc": "Vỏ bánh giòn rụm bên ngoài, nhân trứng cút thơm bùi hoặc thịt bò bằm chấm mắm xíu mại mỡ hành tuyệt hảo.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    }
]

VUNGTAU_DESTS = [
    {
        "id": "vungtau_dest_1", "name": "Tượng Chúa Dang Tay (Chúa Kitô Vua)", "category": "spiritual", "rating": "4.6",
        "img1": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&q=80",
        "tags": ["Biểu_tượng", "Ngắm_toàn_cảnh", "Núi_Nhỏ"],
        "descShort": "Bức tượng Chúa lớn nhất châu Á tọa lạc trên đỉnh núi Nhỏ lộng gió đón sóng vỗ rì rào.",
        "descLong": "Vượt qua 800+ bậc đá rợp mát bóng cây để lên đỉnh, từ cánh tay Chúa thu trọn vào tầm mắt toàn bộ cảnh biển và phố xá Vũng Tàu tuyệt hảo.",
        "highlights": ["Chinh phục 800+ bậc đá rợp mát", "Ngắm toàn cảnh biển từ tay Chúa rộng mở", "Tận hưởng làn gió đại dương lộng mát"],
        "bestTime": "Nên leo vào buổi sáng mát mẻ trước 9h hoặc chiều muộn trước 17h.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Tượng+Chúa+Kitô+Vua+Vũng+Tàu", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vungtau_dest_2", "name": "Ngọn Hải Đăng Vũng Tàu", "category": "history", "rating": "4.5",
        "img1": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "tags": ["Cổ_kính_nhất", "Hoàng_hôn_đẹp", "Yaourt_Cô_Tiên"],
        "descShort": "Một trong những hải đăng cổ nhất Việt Nam, sừng sững trên đỉnh Tao Phùng view ôm trọn biển cả.",
        "descLong": "Cung đường dốc dạo quanh núi rực rỡ hoa giấy rợp sắc hồng. Thưởng thức Yaourt và trứng lòng đào nổi tiếng dưới chân dốc thơ mộng.",
        "highlights": ["Dạo quanh cung đường đèo rợp sắc hoa giấy", "Ghé thưởng thức Yaourt Cô Tiên nức tiếng", "Chụp hình cùng tháp hải đăng trắng cổ kính"],
        "bestTime": "Khoảng 16h30 chiều ngắm hoàng hôn nhuộm đỏ chân trời vịnh biển.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Ngọn+Hải+Đăng+Vũng+Tàu", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vungtau_dest_3", "name": "Mũi Nghinh Phong", "category": "nature", "rating": "4.6",
        "img1": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "tags": ["Đón_gió_biển", "Cổng_trời", "Checkin_siêu_đẹp"],
        "descShort": "Mũi đất lộng gió vươn dài ra đại dương tạo nên cổng trời độc nhất vuông nhị lãng mạn.",
        "descLong": "Phong cảnh hùng vĩ tựa sơn hướng thủy đón đầu những ngọn sóng. Nơi tuyệt mỹ ngắm trọn vẹn đảo Hòn Bà cô độc trên mặt biển.",
        "highlights": ["Chụp ảnh checkin tại Cổng Trời huyền ảo", "Ngắm nhìn đảo nhỏ Hòn Bà xa khơi", "Đón gió biển lộng lộng rì rào sóng vỗ"],
        "bestTime": "Bình minh hoặc hoàng hôn lãng mạn lộng gió đại dương.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Mũi+Nghinh+Phong+Vũng+Tàu", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vungtau_dest_4", "name": "Bạch Dinh (Villa Blanche)", "category": "history", "rating": "4.4",
        "img1": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "tags": ["Kiến_trúc_Pháp_cổ", "Cây_hoa_sứ", "View_Bãi_Trước"],
        "descShort": "Dinh thự cổ phong cách Pháp cuối thế kỷ XIX tráng lệ ẩn hiện dưới rặng hoa sứ cổ thụ nở trắng đồi.",
        "descLong": "Từng là nơi nghỉ ngơi của Toàn quyền Pháp và Vua Thành Thái dấn thân chốn lưu đày. View vịnh biển Bãi Trước từ đây cực kỳ khoáng đạt.",
        "highlights": ["Chiêm ngưỡng kiến trúc tân cổ điển tinh tế", "Chụp ảnh rặng sứ trắng cổ trăm năm tuổi", "Tìm hiểu dấu ấn lịch sử hào hùng xưa cũ"],
        "bestTime": "Nên đi vào ban ngày mát mẻ dạo chơi quanh đồi sứ trắng.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bạch+Dinh+Vũng+Tàu", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vungtau_dest_5", "name": "Bãi Sau (Bãi Thùy Vân)", "category": "beach", "rating": "4.4",
        "img1": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "tags": ["Bãi_tắm_đẹp", "Sóng_vỗ_rì_rào", "Đón_bình_minh"],
        "descShort": "Bãi biển dài sầm uất nhất Vũng Tàu, sóng êm nước mát rượi hoàn hảo tắm bơi đón cát mịn.",
        "descLong": "Kéo dài hơn 5km bãi cát phẳng mịn thoai thoải, nơi hoàn hảo đón bình minh dát vàng mặt biển rực rỡ lộng gió mát lành.",
        "highlights": ["Tắm biển xua tan cái nắng oi bức ngày dài", "Dạo mát ngắm ánh bình minh vàng dịu nhẹ", "Ăn hải sản nướng thơm lừng dọc bờ biển"],
        "bestTime": "Tắm sáng sớm mát 5h30 - 7h30 hoặc bơi chiều muộn lộng gió mát lành.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bãi+Sau+Vũng+Tàu", "linkUrl": "", "isDefault": True
    }
]

VUNGTAU_HOTELS = [
    {
        "id": "vungtau_hotel_1", "name": "The Imperial Hotel Vũng Tàu", "stars": "5", "price": "Từ 2.200.000 VNĐ",
        "address": "159 Thùy Vân, Thắng Tam, Vũng Tàu",
        "desc": "Khách sạn phong cách Phục Hưng hoàng gia sang trọng sát Bãi Sau, hồ bơi vô cực vô cùng lộng lẫy.",
        "imgUrl": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Imperial+Hotel+Vung+Tau", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vungtau_hotel_2", "name": "Marina Bay Vung Tau Resort", "stars": "5", "price": "Từ 1.900.000 VNĐ",
        "address": "115 Trần Phú, Phường 5, Vũng Tàu",
        "desc": "Khu nghỉ dưỡng ven biển Bãi Dâu yên bình, phòng hướng biển ngắm trọn vẹn hoàng hôn buông lãng mạn.",
        "imgUrl": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Marina+Bay+Vung+Tau+Resort", "linkUrl": "", "isDefault": True
    }
]

VUNGTAU_FOOD = [
    {
        "id": "vungtau_food_1", "name": "Bánh Khọt Gốc Vú Sữa", "category": "specialty", "address": "14 Nguyễn Trường Tộ, Phường 2, Vũng Tàu",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bánh+Khọt+Gốc+Vú+Sữa+Vũng+Tàu", "linkUrl": "",
        "desc": "Bánh khọt chiên giòn rụm nóng hổi nhân tôm to bùi ngậy cuốn rau rừng tươi xanh chấm mắm ngòn ngọt tuyệt cú mèo.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    },
    {
        "id": "vungtau_food_2", "name": "Hải sản Gành Hào", "category": "restaurant", "address": "03 Trần Phú, Phường 5, Vũng Tàu",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Hải+sản+Gành+Hào+Vũng+Tàu", "linkUrl": "",
        "desc": "Thưởng thức hải sản tươi ngon phong phú lộng gió bên bờ kè view ôm trọn biển cả lộng gió lộng lẫy tại Gành Hào.",
        "imgUrl": "https://images.unsplash.com/photo-1548943487-a2e4b43b5930?w=800&q=80", "isDefault": True
    },
    {
        "id": "vungtau_food_3", "name": "Lẩu cá đuối Út Mười", "category": "specialty", "address": "16A Trương Công Định, Phường 3, Vũng Tàu",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Lẩu+cá+đuối+Út+Mười+Vũng+Tàu", "linkUrl": "",
        "desc": "Nước dùng lẩu chua cay măng chua đặc sắc quyện cùng thịt cá đuối giòn sần sật béo ngậy thơm ngọt ngào.",
        "imgUrl": "https://images.unsplash.com/photo-1548943487-a2e4b43b5930?w=800&q=80", "isDefault": True
    },
    {
        "id": "vungtau_food_4", "name": "Bông lan trứng muối Gốc Cột Điện", "category": "street", "address": "17B Nguyễn Trường Tộ, Phường 2, Vũng Tàu",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bông+lan+trứng+muối+Gốc+Cột+Điện+Vũng+Tàu", "linkUrl": "",
        "desc": "Cốt bánh xốp mịn thơm lừng mùi bơ sữa quyện cùng lòng đỏ trứng muối mằn mặn béo ngậy cực thích hợp làm quà lưu niệm.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    }
]

VINHHY_DESTS = [
    {
        "id": "vinhhy_dest_1", "name": "Vịnh Vĩnh Hy", "category": "dive", "rating": "4.8",
        "img1": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1584285406087-0b19001bfa54?w=800&q=80",
        "tags": ["Vịnh_biển_đẹp", "Tàu_đáy_kính", "Ngắm_san_hô"],
        "descShort": "Một trong 4 vịnh biển hoang sơ, thơ mộng nhất Việt Nam nép mình bên Núi Chúa tráng lệ.",
        "descLong": "Trải nghiệm đi tàu đáy kính chiêm ngưỡng rạn san hô rực rỡ sắc màu sâu dưới dòng nước trong xanh lấp lánh như pha lê.",
        "highlights": ["Tàu đáy kính ngắm san hô đa dạng", "Tắm mát bơi lội vịnh biển yên bình hoang sơ", "Dùng bữa bè nổi hải sản tuyệt cú mèo"],
        "bestTime": "Nên ghé vịnh đẹp nhất từ tháng 3 đến tháng 9 trời êm sóng lặng.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Vịnh+Vĩnh+Hy+Ninh+Thuận", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vinhhy_dest_2", "name": "Hang Rái", "category": "nature", "rating": "4.6",
        "img1": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1559592413-7cea4ee48083?w=800&q=80",
        "tags": ["Thác_trên_biển", "Bãi_đá_cổ", "Chụp_bình_minh"],
        "descShort": "Tuyệt tác tự nhiên bãi rạn san hô cổ nghìn năm tạo thành thác nước đổ tràn trên đại dương kỳ bí.",
        "descLong": "Nơi sóng xô xối xả vào bãi rạn đá cổ phẳng mịn như lòng chảo tạo nên dòng nước tràn trề kỳ ảo ngỡ ngập chốn tiên cảnh.",
        "highlights": ["Đón bình minh nhuộm hồng thác biển rực rỡ", "Chụp hình bãi rạn đá vôi cổ khổng lồ", "Check-in cầu gỗ ven vách đá tuyệt mỹ"],
        "bestTime": "Khoảng 5h15 sáng đón hoàng kim bình minh dát vàng sóng vỡ kì diệu.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Hang+Rái+Ninh+Thuận", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vinhhy_dest_3", "name": "Đảo Bình Hưng", "category": "nature", "rating": "4.7",
        "img1": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "tags": ["Bãi_nước_ngọt", "Đảo_tôm_hùm", "Trong_vắt"],
        "descShort": "Đảo nhỏ xinh đẹp vịnh Cam Ranh nổi tiếng với dòng nước biển xanh trong veo thấu đáy mát lành.",
        "descLong": "Thả mình bơi lội bãi Nước Ngọt cát trắng mịn như nhung hoang sơ, thưởng thức tôm hùm béo ngậy nuôi lồng ngay tại bè nổi.",
        "highlights": ["Bơi lội bãi Nước Ngọt trong vắt thấu đáy", "Ăn tôm hùm nướng phô mai béo ngậy ngọt ngào", "Ngắm ngọn hải đăng Hòn Chút bao la"],
        "bestTime": "Mùa hè lộng gió biển êm mát tha hồ tắm mát đảo nhỏ.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Đảo+Bình+Hưng", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vinhhy_dest_4", "name": "Vườn Nho Thái An", "category": "nature", "rating": "4.5",
        "img1": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=800&q=80",
        "tags": ["Hái_nho", "Đặc_sản_Ninh_Thuận", "Mật_nho"],
        "descShort": "Vườn nho trĩu quả xanh đỏ sậm rợp bóng mát, thỏa sức tự tay cắt nho hái quả ngọt bùi.",
        "descLong": "Tham quan, nếm thử nho tươi ngọt mọng nước cùng siro mật nho, rượu nho lên men tự nhiên đặc sản Ninh Thuận lừng danh.",
        "highlights": ["Tự tay cắt nho mọng chín quả ngọt lịm", "Thưởng thức ly mật nho mát ngọt thanh khiết", "Mua đặc sản nho tỏi làm quà ý nghĩa"],
        "bestTime": "Nên đi ban ngày đón bóng mát rợp quả xinh xắn.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Vườn+Nho+Thái+An", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vinhhy_dest_5", "name": "Suối Lồ Ồ", "category": "nature", "rating": "4.4",
        "img1": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "tags": ["Suối_trong_rừng", "Cầu_treo", "Hoang_sơ"],
        "descShort": "Dòng suối mát lạnh ngọt lành len lỏi qua đại ngàn Núi Chúa hùng vĩ lộng gió rừng xanh.",
        "descLong": "Trải nghiệm đi cầu treo lắc lư mạo hiểm, lội dòng suối trong vắt ngâm chân sảng khoái xua đi cái nóng gió biển oi bức cực kỳ thư thái.",
        "highlights": ["Trekking lội suối trong rừng mát lạnh sâu lắng", "Check-in chiếc cầu treo đung đưa kịch tính", "Khám phá bản làng Raglai hoang sơ"],
        "bestTime": "Nên đi vào khoảng trưa mát mẻ bóng cây che lộng lộng gió ngàn.", "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Suối+Lồ+Ồ+Vĩnh+Hy", "linkUrl": "", "isDefault": True
    }
]

VINHHY_HOTELS = [
    {
        "id": "vinhhy_hotel_1", "name": "Amanoi Resort", "stars": "6", "price": "Từ 24.000.000 VNĐ",
        "address": "Vịnh Vĩnh Hy, Vĩnh Hải, Ninh Hải, Ninh Thuận",
        "desc": "Khu nghỉ dưỡng 6 sao siêu cao cấp đầu tiên Việt Nam ẩn mình giữa Núi Chúa tráng lệ view ôm trọn vịnh Vĩnh Hy lấp lánh.",
        "imgUrl": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Amanoi+Resort+Vinh+Hy", "linkUrl": "", "isDefault": True
    },
    {
        "id": "vinhhy_hotel_2", "name": "Vĩnh Hy Resort", "stars": "3", "price": "Từ 800.000 VNĐ",
        "address": "Vịnh Vĩnh Hy, Vĩnh Hải, Ninh Hải, Ninh Thuận",
        "desc": "Resort nằm ngay sát bờ vịnh, tiện nghi ấm cúng, hồ bơi lớn lộng gió ôm biển bao la mát mẻ.",
        "imgUrl": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Vịnh+Vĩnh+Hy+Resort", "linkUrl": "", "isDefault": True
    }
]

VINHHY_FOOD = [
    {
        "id": "vinhhy_food_1", "name": "Tôm hùm Bình Hưng", "category": "specialty", "address": "Đảo Bình Hưng, Vịnh Cam Ranh",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Tôm+hùm+Bình+Hưng", "linkUrl": "",
        "desc": "Tôm hùm nuôi tại lồng nước sạch sâu thẳm, thịt tôm dai ngọt ngọt ngào nướng cùng phô mai béo ngậy thơm lừng.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    },
    {
        "id": "vinhhy_food_2", "name": "Hải sản Vịnh Vĩnh Hy", "category": "seafood", "address": "Cảng vịnh Vĩnh Hy, Ninh Thuận",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Hải+sản+Vĩnh+Hy", "linkUrl": "",
        "desc": "Mực lá dày giòn sần sật ngọt thịt, nhum biển nướng thơm phức bùi ngậy vừa đánh bắt khơi lên.",
        "imgUrl": "https://images.unsplash.com/photo-1548943487-a2e4b43b5930?w=800&q=80", "isDefault": True
    },
    {
        "id": "vinhhy_food_3", "name": "Gỏi cá mai Ninh Thuận", "category": "specialty", "address": "Các quán dọc biển Ninh Chữ",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Gỏi+cá+mai+Ninh+Thuận", "linkUrl": "",
        "desc": "Cá mai tươi ngon bóp chua thanh rắc thính gạo thơm phức cuộn bánh tráng chấm tương đậu phộng bùi béo tuyệt cú mèo.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    },
    {
        "id": "vinhhy_food_4", "name": "Bánh xèo Phan Rang", "category": "street", "address": "Bến vịnh Vĩnh Hy",
        "mapsUrl": "https://www.google.com/maps/search/?api=1&query=Bánh+xèo+Phan+Rang", "linkUrl": "",
        "desc": "Chiếc bánh xèo giòn tan nhân mực tươi rói kèm giá hẹ ăn cùng nước mắm chua ngọt hoặc nước mắm nêm đậm đà.",
        "imgUrl": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80", "isDefault": True
    }
]

# Timelines for Tab 2 Preset Timeline
DALAT_TIMELINE = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-bus"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Hành Trình Lên Phố Sương Mù & Đêm Chợ Đà Lạt</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 11:30</div>
                                <div>Di chuyển bằng xe khách Limousine giường nằm từ TP.HCM qua cung đèo Bảo Lộc uốn lượn lộng gió mát ngắm cảnh thông ngút ngàn.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">13:30 - 14:30</div>
                                <div>Check-in nhận phòng tại <strong>Hotel Colline</strong> ngay cạnh chợ Đà Lạt, sắp xếp hành lý đồ đạc và nghỉ ngơi chút.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Dạo bộ quanh <strong>Hồ Xuân Hương</strong> ngắm liễu rủ thơ mộng, check-in đóa hoa Atiso khổng lồ tại Quảng trường Lâm Viên.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 20:00</div>
                                <div>Thưởng thức món nức tiếng <strong>Lẩu Gà Lá É Tao Ngộ</strong> nóng hổi quyện cùng vị the mát độc đáo cực kỳ ấm nồng giữa khí trời se lạnh.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">20:30 - 22:30</div>
                                <div>Khám phá <strong>Chợ Đêm Đà Lạt</strong>, thưởng thức sữa đậu nành nóng hổi cùng bánh tráng nướng lừng danh giòn giòn béo ngậy.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-cloud"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Săn Mây Đỉnh Langbiang & Hoàng Hôn Tuyền Lâm</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">05:00 - 08:30</div>
                                <div>Dậy sớm đi xe Jeep vượt dốc thông mát lạnh lên đỉnh <strong>Langbiang</strong> săn mây bồng bềnh phủ trắng thung lũng đón bình minh vàng rực rỡ.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 10:00</div>
                                <div>Ăn sáng <strong>Bánh mì xíu mại chén Hoàng Diệu</strong> cay cay nóng hổi chấm ổ bánh mì giòn rụm tuyệt vời.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:30</div>
                                <div>Dùng bữa cơm lam gà nướng ống tre đặc sắc Tây Nguyên tại thung lũng thông reo.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Chèo SUP đón hoàng hôn tuyệt tác tím biếc rọi xuống mặt hồ phẳng lặng như gương tại <strong>Hồ Tuyền Lâm</strong> mơ mộng.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-camera"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Di Sản Hoài Cổ Ga Xe Lửa & Chùa Ve Chai</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:30</div>
                                <div>Chụp hình hoài cổ bên những đầu máy xe lửa hơi nước xưa tại <strong>Ga Đà Lạt</strong> kiến trúc mái chóp độc đáo.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">11:00 - 12:30</div>
                                <div>Viếng ngôi <strong>Chùa Linh Phước</strong> (chùa Ve Chai) tráng lệ khảm đầy sành sứ khéo léo bái Phật Quan Âm cầu bình an.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">13:00 - 14:30</div>
                                <div>Thưởng thức món bánh căn giòn rụm nhân trứng cút thơm bùi tại quán <strong>Bánh Căn Lệ</strong> trứ danh.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Hương Sắc Sương Mờ & Trở Về Đất Liền</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 11:00</div>
                                <div>Ghé sạp chợ trung tâm mua dâu tây tươi mọng, mứt hồng sấy dẻo ngọt ngào và trà atiso làm quà kỷ niệm ý nghĩa.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 12:30</div>
                                <div>Check-out trả phòng <strong>Hotel Colline</strong>, sắp xếp đồ đạc lên xe Limousine kết thúc hải trình 4N3Đ trọn vẹn thơ mộng!</div>
                            </li>
                        </ul>
                    </div>"""

VUNGTAU_TIMELINE = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-ship"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Tàu Cánh Ngầm Vượt Sóng & Chinh Phục Núi Nhỏ</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:00</div>
                                <div>Trải nghiệm di chuyển bằng <strong>Tàu cánh ngầm Greenlines</strong> từ Bến Bạch Đằng lướt sóng ôm đại dương mát mẻ hướng về Vũng Tàu.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">10:30 - 11:30</div>
                                <div>Ăn trưa đặc sản lừng danh <strong>Bánh Khọt Gốc Vú Sữa</strong> giòn tan tôm ngọt ngào kèm rau rừng ngập mắm chua ngọt.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Check-in khách sạn 5 sao hoàng gia <strong>The Imperial Hotel Vũng Tàu</strong> ngay sát bãi tắm thư giãn nghỉ ngơi.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Tắm bơi lội đón làn cát mịn, sóng vỗ lộng gió trong lành rì rào Bãi Sau tuyệt vời.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:00 - 19:30</div>
                                <div>Chinh phục 800 bậc đá lên sườn núi Nhỏ viếng <strong>Tượng Chúa Dang Tay</strong> lộng gió đại dương ôm hoàng hôn tím lãng mạn.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-camera"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Dinh Thự Bạch Dinh Cổ & Hoàng Hôn Ngọn Hải Đăng</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 10:30</div>
                                <div>Khám phá dinh thự cổ phong cách Pháp tráng lệ <strong>Bạch Dinh</strong> rợp sắc hoa sứ trắng ngắm trọn vịnh biển Bãi Trước thơ mộng.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Chạy xe máy vượt dốc núi rợp hoa giấy lên đỉnh <strong>Ngọn Hải Đăng</strong> ngắm hoàng hôn rực rỡ và dùng trứng lòng đào yaourt Cô Tiên cực ngon.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Ăn tối hải sản tươi sống đẳng cấp bên bờ kè view ôm trọn biển cả lộng gió lộng lẫy tại <strong>Hải sản Gành Hào</strong>.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-umbrella-beach"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Đi Cáp Treo Hồ Mây & Ngắm Sóng Mũi Nghinh Phong</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:30 - 12:00</div>
                                <div>Trải nghiệm cáp treo lên đỉnh núi vui chơi trọn gói KDL sinh thái <strong>Hồ Mây Park</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Chụp ảnh checkin tại Cổng Trời lộng gió, đón sóng đại dương mênh mông rì rào tại <strong>Mũi Nghinh Phong</strong>.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Tắm Sáng Đón Bình Minh & Quà Tặng Lưu Luyến</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 09:30</div>
                                <div>Tắm mát đón những tia nắng bình minh dịu nhẹ dát vàng óng ánh trên Bãi Sau phẳng mịn.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">10:00 - 11:30</div>
                                <div>Ghé sạp mua bánh bông lan trứng muối <strong>Gốc Cột Điện</strong> nóng hổi thơm phức bơ sữa mang về làm quà.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 12:30</div>
                                <div>Trả phòng khách sạn, thong thả lên tàu cánh ngầm rời bến quay về bến Bạch Đằng kết thúc chuyến đi!</div>
                            </li>
                        </ul>
                    </div>"""

VINHHY_TIMELINE = """                    <!-- Ngày 1 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-car"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 1: Vịnh Vĩnh Hy Bình Yên & Khám Phá Rạn San Hô</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:00 - 11:30</div>
                                <div>Được xe dịch vụ đón từ sân bay Cam Ranh vi vu qua cung đường đèo Núi Chúa ven đại dương tuyệt mỹ hướng vào vịnh biển hoang sơ.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:00</div>
                                <div>Check-in nhận phòng tại <strong>Vĩnh Hy Resort</strong> nép mình sát mép biển vịnh bình yên, ăn trưa nạp năng lượng.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">14:30 - 17:30</div>
                                <div>Lên tàu đáy kính ngắm nhìn rạn san hô đa màu sắc rực rỡ lộng lẫy dưới dòng nước trong veo như pha lê thấu đáy tại <strong>Vịnh Vĩnh Hy</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">18:30 - 21:00</div>
                                <div>Dùng bữa tối hải sản tươi sống vừa đánh bắt lên như mực lá dày giòn sần sật ngọt thịt, nhum biển nướng thơm phức bùi ngậy tại <strong>Hải sản Vịnh Vĩnh Hy</strong>.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 2 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-camera"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 2: Đón Bình Minh Hang Rái & Ghé Vườn Nho Thái An</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">05:00 - 08:30</div>
                                <div>Đón những vệt bình minh dát vàng óng ánh trên bãi rạn san hô cổ FLAT phẳng mịn tuyệt tác thác tràn đại dương hoang sơ tại <strong>Hang Rái</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 11:00</div>
                                <div>Khám phá hái những chùm nho chín ngọt tươi rói mát lạnh, chụp hình rợp bóng xinh đẹp tại <strong>Vườn Nho Thái An</strong> lừng danh.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">15:00 - 17:30</div>
                                <div>Trekking ngắm cầu treo Raglai đung đưa, lội nước suối trong mát rượi tại <strong>Suối Lồ Ồ</strong> xuyên đại ngàn hoang sơ Núi Chúa.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 3 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-umbrella-beach"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 3: Hải Đảo Bình Hưng Trong Vắt & Ăn Tôm Hùm Bè</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">08:30 - 15:30</div>
                                <div>Thỏa thích tắm mát chèo SUP giữa bãi cát trắng mịn Bãi Nước Ngọt trong veo thấu đáy như pha lê ở <strong>Đảo Bình Hưng</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">12:00 - 13:30</div>
                                <div>Thưởng thức đại tiệc đặc sản <strong>Tôm hùm Bình Hưng</strong> nướng bơ tỏi ngọt lịm béo ngậy thơm nức lòng ngay trên bè nổi lồng bè đại dương.</div>
                            </li>
                        </ul>
                    </div>

                    <!-- Ngày 4 -->
                    <div class="timeline-item">
                        <div class="timeline-icon"><i class="fa-solid fa-bag-shopping"></i></div>
                        <h3 class="text-xl font-bold text-gray-800 bg-[#f5f5dc] inline-block px-4 py-1 rounded-md mb-4 shadow-sm">Ngày 4: Thưởng Thức Bánh Xèo Phan Rang & Tạm Biệt Vịnh Biển</h3>
                        <ul class="space-y-4 text-gray-600 text-sm md:text-base leading-relaxed">
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">07:30 - 08:30</div>
                                <div>Ăn sáng món bánh xèo đổ lò mực tươi rói giòn rụm ngập tương đậu phộng bùi béo <strong>Bánh xèo Phan Rang</strong>.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">09:00 - 11:00</div>
                                <div>Ghé sạp mua đặc sản mật nho mọng ngọt lịm, tỏi Phan Rang thơm cay mang về làm quà.</div>
                            </li>
                            <li class="flex items-start bg-gray-50/50 p-3 rounded-xl border border-gray-100 hover:border-teal-200 transition-colors">
                                <div class="bg-teal-100 text-teal-700 font-bold px-2 py-1 rounded text-xs mr-3 h-fit whitespace-nowrap">11:30 - 12:30</div>
                                <div>Check-out trả phòng resort <strong>Vĩnh Hy Resort</strong>, tạm biệt vịnh biển trong lành kết thúc hành trình 4N3Đ trọn vẹn xúc cảm!</div>
                            </li>
                        </ul>
                    </div>"""

# Templates for loadDefaultTemplate() javascript function replacement
DALAT_TEMPLATE_JS = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "dl1", time: "07:30 - 11:30", dest: "Đỉnh Langbiang", note: "Di chuyển lên Đà Lạt bằng xe khách giường nằm từ TP.HCM" },
                { id: "dl2", time: "13:30 - 14:30", dest: "Hotel Colline", note: "Nhận phòng khách sạn, sắp xếp đồ đạc nghỉ ngơi" },
                { id: "dl3", time: "15:00 - 17:30", dest: "Quảng trường Lâm Viên", note: "Dạo quanh Hồ Xuân Hương và ngắm hoàng hôn Atiso" },
                { id: "dl4", time: "18:30 - 20:00", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Thưởng thức lẩu gà lá é nóng hổi cực ngon" },
                { id: "dl5", time: "20:30 - 22:30", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Dạo chơi, ăn quà chợ đêm Đà Lạt se lạnh" }
            ],
            day2: [
                { id: "dl6", time: "05:00 - 08:30", dest: "Đỉnh Langbiang", note: "Đi xe Jeep săn mây Langbiang lúc sáng sớm" },
                { id: "dl7", time: "09:00 - 10:00", dest: "Bánh mì xíu mại chén Hoàng Diệu", note: "Ăn sáng bánh mì xíu mại chén nổi tiếng" },
                { id: "dl8", time: "12:00 - 13:30", dest: "Lẩu Bò Ba Toa Nhà Gỗ", note: "Ăn trưa lẩu bò béo ngậy ngọt ngào" },
                { id: "dl9", time: "15:00 - 17:30", dest: "Hồ Tuyền Lâm", note: "Chèo SUP ngắm hoàng hôn lãng mạn trên mặt hồ" }
            ],
            day3: [
                { id: "dl10", time: "08:00 - 10:30", dest: "Ga Đà Lạt", note: "Tham quan nhà ga cổ kính, chụp hình hơi nước xưa" },
                { id: "dl11", time: "11:00 - 12:30", dest: "Chùa Linh Phước (Chùa Ve Chai)", note: "Viếng chùa khảm sành sứ rực rỡ ấn tượng" },
                { id: "dl12", time: "13:00 - 14:30", dest: "Bánh Căn Lệ", note: "Dùng bữa trưa nhẹ bánh căn nóng giòn rụm" },
                { id: "dl13", time: "15:00 - 17:30", dest: "Hồ Tuyền Lâm", note: "Ghé các quán cà phê ngắm cảnh sương mù thung lũng" }
            ],
            day4: [
                { id: "dl14", time: "07:30 - 08:30", dest: "Bánh Căn Lệ", note: "Ăn sáng bún riêu, ngắm sương mù ven đồi" },
                { id: "dl15", time: "09:00 - 11:00", dest: "Lẩu Gà Lá É Tao Ngộ", note: "Mua đặc sản hồng sấy dẻo và trà atiso tại chợ Đà Lạt" },
                { id: "dl16", time: "12:00 - 12:30", dest: "Hotel Colline", note: "Check-out trả phòng khách sạn, kết thúc chuyến đi" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

VUNGTAU_TEMPLATE_JS = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "vt1", time: "08:00 - 10:00", dest: "Tượng Chúa Dang Tay (Chúa Kitô Vua)", note: "Trải nghiệm đi tàu cao tốc Greenlines từ Bạch Đằng ra Vũng Tàu" },
                { id: "vt2", time: "10:30 - 11:30", dest: "Bánh Khọt Gốc Vú Sữa", note: "Thưởng thức bánh khọt giòn rụm tôm to ngọt lịm" },
                { id: "vt3", time: "12:00 - 13:00", dest: "The Imperial Hotel Vũng Tàu", note: "Check-in khách sạn, nhận phòng và cất hành lý" },
                { id: "vt4", time: "15:00 - 17:30", dest: "Bãi Sau (Bãi Thùy Vân)", note: "Tắm biển Bãi Sau sóng vỗ mát rượi đón hoàng hôn" },
                { id: "vt5", time: "18:00 - 19:30", dest: "Tượng Chúa Dang Tay (Chúa Kitô Vua)", note: "Chinh phục bậc đá ngắm nhìn vịnh biển lộng gió chiều muộn" }
            ],
            day2: [
                { id: "vt6", time: "08:00 - 10:30", dest: "Bạch Dinh (Villa Blanche)", note: "Khám phá dinh thự cổ và vườn hoa sứ trắng thời Pháp" },
                { id: "vt7", time: "15:00 - 17:30", dest: "Ngọn Hải Đăng Vũng Tàu", note: "Lên đỉnh ngọn hải đăng cổ đón hoàng hôn, ăn yaourt cô tiên dưới chân núi" },
                { id: "vt8", time: "18:30 - 21:00", dest: "Hải sản Gành Hào", note: "Ăn tối hải sản tươi sống ngắm sóng vỗ tuyệt đẹp" }
            ],
            day3: [
                { id: "vt9", time: "08:30 - 12:00", dest: "KDL Hồ Mây Park", note: "Đi cáp treo lên đỉnh núi vui chơi trọn gói" },
                { id: "vt10", time: "15:00 - 17:30", dest: "Mũi Nghinh Phong", note: "Chụp ảnh tại Cổng Trời đón từng cơn gió lộng" }
            ],
            day4: [
                { id: "vt11", time: "07:30 - 09:30", dest: "Bãi Sau (Bãi Thùy Vân)", note: "Tắm biển sáng sớm thư giãn đón bình minh rực rỡ" },
                { id: "vt12", time: "10:00 - 11:30", dest: "Bông lan trứng muối Gốc Cột Điện", note: "Mua bông lan trứng muối Gốc Cột Điện nóng hổi về làm quà" },
                { id: "vt13", time: "12:00 - 12:30", dest: "The Imperial Hotel Vũng Tàu", note: "Check-out trả phòng khách sạn kết thúc chuyến đi" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

VINHHY_TEMPLATE_JS = """function loadDefaultTemplate() {
    if (confirm("Nạp lịch trình mẫu 4N3Đ? Lịch trình hiện tại của bạn sẽ bị thay thế.")) {
        customPlan = {
            day1: [
                { id: "vh1", time: "08:00 - 11:30", dest: "Vịnh Vĩnh Hy", note: "Di chuyển xe đèo từ sân bay Cam Ranh vượt cung đèo vịnh biển tuyệt tác" },
                { id: "vh2", time: "12:00 - 13:00", dest: "Vĩnh Hy Resort", note: "Check-in resort nhận phòng nghỉ ngơi nạp năng lượng" },
                { id: "vh3", time: "14:30 - 17:30", dest: "Vịnh Vĩnh Hy", note: "Lên tàu đáy kính ngắm san hô nhiều màu sắc và tắm biển vịnh" },
                { id: "vh4", time: "18:30 - 21:00", dest: "Hải sản Vịnh Vĩnh Hy", note: "Ăn tối hải sản tươi sống ngọt bùi tại cảng vịnh" }
            ],
            day2: [
                { id: "vh5", time: "05:00 - 08:30", dest: "Hang Rái", note: "Dậy sớm ngắm bình minh trên thác biển cổ nghìn năm tuyệt mỹ" },
                { id: "vh6", time: "09:00 - 11:00", dest: "Vườn Nho Thái An", note: "Ghé hái nho tươi chín mọng ngọt ngào và thử mật nho thơm lừng" },
                { id: "vh7", time: "15:00 - 17:30", dest: "Suối Lồ Ồ", note: "Trekking đi bộ mát mẻ lội suối xuyên rừng Núi Chúa" }
            ],
            day3: [
                { id: "vh8", time: "08:30 - 15:30", dest: "Đảo Bình Hưng", note: "Thuê cano lặn ngắm san hô Bãi Nước Ngọt, ngắm biển trong như gương" },
                { id: "vh9", time: "12:00 - 13:30", dest: "Tôm hùm Bình Hưng", note: "Thưởng thức tôm hùm nướng béo ngậy ngọt lịm trên bè nổi đảo" }
            ],
            day4: [
                { id: "vh10", time: "07:30 - 08:30", dest: "Hải sản Vịnh Vĩnh Hy", note: "Ăn sáng bánh xèo hải sản Phan Rang giòn tan thơm ngon" },
                { id: "vh11", time: "09:00 - 11:00", dest: "Amanoi Resort", note: "Mua đặc sản nho khô và tỏi Ninh Thuận mang về làm quà" },
                { id: "vh12", time: "11:30 - 12:30", dest: "Vĩnh Hy Resort", note: "Check-out trả phòng resort xếp hành lý rời vịnh bình yên" }
            ]
        };
        savePlanToStorage();
        renderCustomTimeline();
    }
}"""

# Tab 3 Transportation Channel segments
DALAT_TAB3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-plane-departure mr-2"></i> Kênh Di Chuyển Lên Lâm Đồng</h3>
                    
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

VUNGTAU_TAB3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-ferry mr-2"></i> Kênh Di Chuyển Đến Vũng Tàu</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-2"><i class="fa-solid fa-ship text-teal-600 mr-2"></i> Bằng Tàu Cánh Ngầm (Greenlines DP)</h4>
                        <p class="text-gray-600 text-sm mb-2">Hải trình vượt vịnh sông biển tuyệt đẹp kết nối trực tiếp quận 1 TP.HCM với cảng Cầu Đá Vũng Tàu.</p>
                        <ul class="list-disc pl-5 text-gray-600 text-sm space-y-1">
                            <li><strong>Thời gian di chuyển:</strong> Khoảng 2 tiếng, lướt êm dịu mát mát lộng gió sông lòng hồ.</li>
                            <li><strong>Giá vé tham khảo:</strong> ECO: 290.000đ - 350.000đ/lượt; VIP: 450.000đ/lượt.</li>
                        </ul>
                    </div>

                    <div>
                        <h4 class="font-bold text-lg text-gray-800 flex items-center mb-3"><i class="fa-solid fa-bus text-teal-600 mr-2"></i> Bằng Xe Khách Limousine</h4>
                        <p class="text-gray-600 text-sm mb-4">Các hãng limousine cao cấp đón trả khách tận nơi trong nội thành thành phố nhanh gọn:</p>

                        <div class="space-y-4">
                            <div class="bg-gray-50/50 hover:bg-teal-50/20 border border-gray-100 hover:border-teal-200 p-4 rounded-xl transition-all duration-300 shadow-sm hover:shadow-md">
                                <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
                                    <h5 class="font-extrabold text-gray-800 text-base flex items-center gap-2"><i class="fa-solid fa-bus text-teal-600"></i> Toàn Thắng / Hoa Mai Limousine</h5>
                                    <span class="bg-teal-600 text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase">Khoảng 2 - 2.5 tiếng</span>
                                </div>
                                <p class="text-sm text-gray-600 mb-3">Tần suất chạy liên tục mỗi 15 - 30 phút, đưa đón tận nơi tận hưởng dòng xe Vip 9 chỗ êm ái.</p>
                                <div class="bg-white p-3 rounded-lg border border-gray-100 text-sm">
                                    <p class="font-semibold text-teal-700 mb-1 border-b pb-1">Bảng giá tham khảo:</p>
                                    <ul class="space-y-1.5 text-gray-600 mt-2">
                                        <li class="flex justify-between"><span>Vé ghế Vip Limousine:</span> <span class="font-bold text-gray-800">180.000 - 200.000 VNĐ</span></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="mt-4 bg-amber-50/80 border border-amber-100 p-4 rounded-xl flex gap-3 shadow-xs">
                                <div class="text-amber-500 text-lg shrink-0 mt-0.5"><i class="fa-solid fa-lightbulb"></i></div>
                                <div>
                                    <h6 class="font-bold text-amber-800 text-sm">Lưu ý khi đi Vũng Tàu</h6>
                                    <p class="text-amber-900/80 text-xs mt-1 leading-relaxed">Nên đặt vé khứ hồi sớm vào cuối tuần vì dòng xe Limousine và vé Tàu cánh ngầm cực kỳ dễ hết chỗ hoặc tắc đường cao tốc.</p>
                                </div>
                            </div>
                        </div>
                    </div>"""

VINHHY_TAB3 = """                    <h3 class="text-2xl font-bold text-teal-700 mb-6 border-b pb-2"><i class="fa-solid fa-plane-departure mr-2"></i> Kênh Di Chuyển Đến Vịnh Vĩnh Hy</h3>
                    
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

def process_page(filename, prefix, viet_name, title_suffix, bg_url, dests, hotels, foods, timeline_html, template_js, tab3_html, transport_clean, select_options_clean):
    path = f"d:\\VSCode\\Some_stuff_case\\condao\\{filename}"
    print(f"Processing and overwriting {filename}...")
    
    # 1. Fresh copy from condao.html to completely wipe out any corruptions
    shutil.copy("d:\\VSCode\\Some_stuff_case\\condao\\condao.html", path)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 2. Localize KEYS prefix (Decouple storage completely!)
    content = content.replace("condao_admin_destinations", f"{prefix}_admin_destinations")
    content = content.replace("condao_admin_hotels", f"{prefix}_admin_hotels")
    content = content.replace("condao_admin_food", f"{prefix}_admin_food")
    content = content.replace("condao_memories", f"{prefix}_memories")
    content = content.replace("condao_memory_pass", f"{prefix}_memory_pass")
    content = content.replace("condao_github_token", f"{prefix}_github_token")
    content = content.replace("condao_github_config", f"{prefix}_github_config")
    content = content.replace("condao_db_initialized", f"{prefix}_db_initialized")
    content = content.replace("condao_custom_plan", f"{prefix}_custom_plan")
    
    # 3. Replace DEFAULT arrays using robust count-based parser
    dests_json = json.dumps(dests, ensure_ascii=False, indent=4)
    hotels_json = json.dumps(hotels, ensure_ascii=False, indent=4)
    foods_json = json.dumps(foods, ensure_ascii=False, indent=4)
    
    content = replace_variable_declaration(content, "DEFAULT_DESTINATIONS", dests_json)
    content = replace_variable_declaration(content, "DEFAULT_HOTELS", hotels_json)
    content = replace_variable_declaration(content, "DEFAULT_FOOD", foods_json)
    
    # 4. Replace loadDefaultTemplate() function cleanly
    content = replace_js_function(content, "loadDefaultTemplate", template_js)
    
    # 5. Inject populatePlannerDestinations() in DOMContentLoaded (ONLY if not already present)
    if "populatePlannerDestinations();" not in content:
        dom_target = """  loadPlanFromStorage();
  renderCustomTimeline();"""
        dom_replacement = """  populatePlannerDestinations();
  loadPlanFromStorage();
  renderCustomTimeline();"""
        content = content.replace(dom_target, dom_replacement)
    
    # 6. Inject populatePlannerDestinations() function before loadPlanFromStorage() (ONLY if not already present)
    if "function populatePlannerDestinations()" not in content:
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
    
    # 7. Replace Hero style background image
    old_bg = "background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.55)), url('./media__1779859942968.jpg');"
    new_bg = f"background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.55)), url('{bg_url}');"
    content = content.replace(old_bg, new_bg)
    
    # 8. Replace Title Tag
    content = content.replace(
        "<title>Khám Phá Côn Đảo - Thiên Đường Nơi Hạ Giới</title>",
        f"<title>Khám Phá {viet_name} - {title_suffix}</title>"
    )
    
    # 9. Global Text Substitutions to clear Côn Đảo references
    content = content.replace("Khám Phá Côn Đảo", f"Khám Phá {viet_name}")
    content = content.replace("danh thắng Côn Đảo", f"danh thắng {viet_name}")
    content = content.replace("địa điểm đẹp nhất Côn Đảo", f"địa điểm đẹp nhất {viet_name}")
    content = content.replace("Cẩm Nang Ẩm Thực & Cà Phê Côn Đảo", f"Cẩm Nang Ẩm Thực & Cà Phê {viet_name}")
    content = content.replace("Quán Ngon Côn Đảo", f"Quán Ngon {viet_name}")
    content = content.replace("chuyến hành trình Côn Đảo", f"chuyến hành trình {viet_name}")
    content = content.replace("Admin Dashboard — Côn Đảo", f"Admin Dashboard — {viet_name}")
    content = content.replace("hành trình khám phá Côn Đảo", f"hành trình khám phá {viet_name}")
    content = content.replace("for Côn Đảo", f"for {viet_name}")
    content = content.replace("LỊCH TRÌNH DU LỊCH CÔN ĐẢO CỦA BẠN", f"LỊCH TRÌNH DU LỊCH {viet_name.upper()} CỦA BẠN")
    content = content.replace("Ngày đầu tiên ở Côn Đảo", f"Ngày đầu tiên ở {viet_name}")
    content = content.replace("Lich_Trinh_Con_Dao_Cua_Toi.txt", f"Lich_Trinh_{prefix}.txt")
    
    # Premium password localization
    content = content.replace("DEFAULT_MEM_PASSWORD = 'ConDao2026';", f"DEFAULT_MEM_PASSWORD = '{prefix.capitalize()}2026';")
    
    # 10. Replace Preset Timeline in Tab 2
    start_timeline = content.find('<div class="timeline-container space-y-2">')
    end_timeline = content.find('<!-- 2. Custom Planner View -->')
    if start_timeline != -1 and end_timeline != -1:
        prefix_html = content[:start_timeline + len('<div class="timeline-container space-y-2">\n')]
        suffix_html = content[end_timeline:]
        content = prefix_html + timeline_html + "\n</div>\n</div>\n</div>\n\n" + suffix_html
        print(f"  Preset timeline replaced in {filename}!")
    else:
        print(f"  WARNING: Timeline boundary elements NOT found in {filename}!")
        
    # 11. Replace Tab 3 Transport Channel
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
    
    content = content.replace(tab3_target, tab3_html)
    print(f"  Transport channel replaced in {filename}!")
    
    # 12. Localize the static "Phương tiện chính" bar below Hero section
    old_transport_line = '<i class="fa-solid fa-ferry animate-bounce"></i> Phương tiện chính: Tàu cao tốc chất lượng cao (Vũng Tàu - Côn Đảo)'
    content = content.replace(old_transport_line, transport_clean)
    print(f"  Static transport indicator replaced in {filename}!")
    
    # 13. Localize the static select options inside HTML
    content = re.sub(
        r'<select id="planner-dest-select"\s+class="[^"]+">([\s\S]*?)</select>',
        f'<select id="planner-dest-select" class="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 text-gray-700 shadow-inner font-semibold">\n{select_options_clean}\n</select>',
        content,
        count=1
    )
    print(f"  Static HTML planner select options replaced in {filename}!")
    
    # 14. Add local destMeta metadata for premium visual matching!
    local_meta_items = []
    for d in dests:
        local_meta_items.append(f'    "{d["name"]}": {{ icon: "{"fa-water" if d["category"] in ["beach","dive"] else "fa-mountain-sun" if d["category"]=="nature" else "fa-landmark" if d["category"]=="history" else "fa-gopuran"}", badge: "{d["tags"][0] if d["tags"] else "#Điểm_đến"}", color: "bg-teal-50 text-teal-700 border-teal-100" }}')
    for h in hotels:
        local_meta_items.append(f'    "{h["name"]}": {{ icon: "fa-hotel", badge: "#{h["stars"]}★", color: "bg-blue-50 text-blue-700 border-blue-100" }}')
    for f in foods:
        local_meta_items.append(f'    "{f["name"]}": {{ icon: "fa-bowl-food", badge: "#Đặc_sản", color: "bg-orange-50 text-orange-700 border-orange-100" }}')
        
    if prefix == "vungtau":
        local_meta_items.append('    "Tàu cánh ngầm Greenlines DP": { icon: "fa-ship", badge: "#Greenlines", color: "bg-blue-50 text-blue-700 border-blue-100" }')
    elif prefix == "vinhhy":
        local_meta_items.append('    "Đường đèo ven biển": { icon: "fa-car", badge: "#Trung_chuyển", color: "bg-blue-50 text-blue-700 border-blue-100" }')
        
    local_destmeta_block = "const destMeta = {\n" + ",\n".join(local_meta_items) + "\n};"
    
    content = replace_variable_declaration(content, "destMeta", "{}")
    content = content.replace("const destMeta = {};", local_destmeta_block)
    print(f"  Premium visual destMeta replaced in {filename}!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully processed and localized {filename}!\n")

def process_condao_dynamic():
    path = "d:\\VSCode\\Some_stuff_case\\condao\\condao.html"
    print("Making condao.html planner fully dynamic...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Inject populatePlannerDestinations in DOMContentLoaded if not present
    if "populatePlannerDestinations();" not in content:
        dom_target = """  loadPlanFromStorage();
  renderCustomTimeline();"""
        dom_replacement = """  populatePlannerDestinations();
  loadPlanFromStorage();
  renderCustomTimeline();"""
        content = content.replace(dom_target, dom_replacement)
        
    # Inject populatePlannerDestinations() function definition before loadPlanFromStorage()
    if "function populatePlannerDestinations()" not in content:
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
        print("  populatePlannerDestinations successfully injected in condao.html!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success condao.html dynamic integration!\n")

if __name__ == "__main__":
    # Make condao dynamic first
    process_condao_dynamic()
    
    # Static option lists for clean-up
    dalat_select = """                                    <option value="Đỉnh Langbiang">1. Đỉnh Langbiang (#Nóc_nhà_Đà_Lạt)</option>
                                    <option value="Hồ Tuyền Lâm">2. Hồ Tuyền Lâm (#Chèo_SUP)</option>
                                    <option value="Ga Đà Lạt">3. Ga Đà Lạt (#Ga_cổ_kính)</option>
                                    <option value="Chùa Linh Phước (Chùa Ve Chai)">4. Chùa Linh Phước (Chùa Ve Chai) (#Chùa_khảm_sành)</option>
                                    <option value="Quảng trường Lâm Viên">5. Quảng trường Lâm Viên (#Nụ_hoa_Atiso)</option>"""
                                    
    vungtau_select = """                                    <option value="Tượng Chúa Dang Tay (Chúa Kitô Vua)">1. Tượng Chúa Dang Tay (Chúa Kitô Vua) (#Biểu_tượng)</option>
                                    <option value="Ngọn Hải Đăng Vũng Tàu">2. Ngọn Hải Đăng Vũng Tàu (#Ngắm_hoàng_hôn)</option>
                                    <option value="Mũi Nghinh Phong">3. Mũi Nghinh Phong (#Cổng_trời)</option>
                                    <option value="Bạch Dinh (Villa Blanche)">4. Bạch Dinh (Villa Blanche) (#Kiến_trúc_Pháp_cổ)</option>
                                    <option value="Bãi Sau (Bãi Thùy Vân)">5. Bãi Sau (Bãi Thùy Vân) (#Bãi_tắm_rộng)</option>"""
                                    
    vinhhy_select = """                                    <option value="Vịnh Vĩnh Hy">1. Vịnh Vĩnh Hy (#Tuyệt_tác_vịnh_biển)</option>
                                    <option value="Hang Rái">2. Hang Rái (#Thác_trên_biển)</option>
                                    <option value="Đảo Bình Hưng">3. Đảo Bình Hưng (#Nước_biển_trong_vắt)</option>
                                    <option value="Vườn Nho Thái An">4. Vườn Nho Thái An (#Hái_nho)</option>
                                    <option value="Suối Lồ Ồ">5. Suối Lồ Ồ (#Suối_mát_trong_rừng)</option>"""
    
    # Process and fully localize Da Lat
    process_page(
        "dalat.html", "dalat", "Đà Lạt", "Thành Phố Sương Mù", "./images/dalat-bg.JPG",
        DALAT_DESTS, DALAT_HOTELS, DALAT_FOOD,
        DALAT_TIMELINE, DALAT_TEMPLATE_JS, DALAT_TAB3,
        '<i class="fa-solid fa-bus animate-bounce"></i> Phương tiện chính: Xe giường nằm Limousine & Máy bay',
        dalat_select
    )
    
    # Process and fully localize Vung Tau
    process_page(
        "vungtau.html", "vungtau", "Vũng Tàu", "Sóng Vỗ Rì Rào", "./images/vungtau-bg.jpg",
        VUNGTAU_DESTS, VUNGTAU_HOTELS, VUNGTAU_FOOD,
        VUNGTAU_TIMELINE, VUNGTAU_TEMPLATE_JS, VUNGTAU_TAB3,
        '<i class="fa-solid fa-ship animate-bounce"></i> Phương tiện chính: Tàu cánh ngầm Greenlines DP & Xe Limousine',
        vungtau_select
    )
    
    # Process and fully localize Vinh Hy
    process_page(
        "vinhhy.html", "vinhhy", "Vĩnh Hy", "Tuyệt Tác Thiên Nhiên", "./images/vinhhy-bg.JPG",
        VINHHY_DESTS, VINHHY_HOTELS, VINHHY_FOOD,
        VINHHY_TIMELINE, VINHHY_TEMPLATE_JS, VINHHY_TAB3,
        '<i class="fa-solid fa-car animate-bounce"></i> Phương tiện chính: Xe khách ven biển & Máy bay (đến Cam Ranh)',
        vinhhy_select
    )
    
    print("ALL RUN-TIME LOCALIZATIONS EXECUTED FLAWLESSLY!")
