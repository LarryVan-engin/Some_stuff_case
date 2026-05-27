# -*- coding: utf-8 -*-
import re

files = ["dalat.html", "vinhhy.html", "vungtau.html"]
keywords = ["côn đảo", "con dao", "six senses", "hàng dương", "đầm trầu", "bãi nhát", "phú hải", "đầm tre", "trần đề", "hòn bà", "chùa núi một"]

report = []
for filename in files:
    report.append(f"\n===== SCANNING {filename} =====")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.splitlines()
    match_count = 0
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        found = []
        for kw in keywords:
            if kw in line_lower:
                found.append(kw)
        if found:
            report.append(f"Line {idx+1}: {line.strip()} (Matched keywords: {found})")
            match_count += 1
    
    report.append(f"Total lines matched in {filename}: {match_count}")

with open("scratch/scan_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("Wrote scan_results.txt successfully!")
