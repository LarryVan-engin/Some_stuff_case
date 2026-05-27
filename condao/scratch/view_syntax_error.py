# -*- coding: utf-8 -*-
import re

with open("dalat.html", "r", encoding="utf-8") as f:
    content = f.read()

scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
for idx, script in enumerate(scripts):
    if "tailwind.config" in script or len(script.strip()) < 50:
        continue
        
    lines = script.split("\n")
    # Let's search for "populatePlannerDestinations" and print its context
    for i, line in enumerate(lines):
        if "populatePlannerDestinations" in line:
            print(f"--- MATCH AT LINE {i+1} ---")
            start = max(0, i - 10)
            end = min(len(lines), i + 15)
            for j in range(start, end):
                safe_line = lines[j].encode('ascii', 'backslashreplace').decode('ascii')
                print(f"  {j+1}: {safe_line}")
