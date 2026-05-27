# -*- coding: utf-8 -*-
import re

with open("condao.html", "r", encoding="utf-8") as f:
    content = f.read()

print("--- Hero Background ---")
bg_match = re.search(r'background-image:[^;]+', content)
if bg_match:
    print(bg_match.group(0))

print("--- Document Title ---")
title_match = re.search(r'<title>([^<]+)</title>', content)
if title_match:
    print(title_match.group(0))

print("--- Main Headers in HTML ---")
headers = [
    "Côn Đảo - Thiên đường nhiệt đới",
    "Khám Phá Côn Đảo",
    "danh thắng Côn Đảo",
    "địa điểm đẹp nhất Côn Đảo",
    "Cẩm Nang Ẩm Thực & Cà Phê Côn Đảo",
    "Lịch Trình Du Lịch Côn Đảo",
    "LỊCH TRÌNH DU LỊCH CÔN ĐẢO CỦA BẠN",
    "Kênh Di Chuyển Ra Đảo"
]
for h in headers:
    count = content.count(h)
    print(f"'{h}': count = {count}")
