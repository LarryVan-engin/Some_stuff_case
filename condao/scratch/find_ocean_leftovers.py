# -*- coding: utf-8 -*-
files = ["dalat.html", "vinhhy.html", "vungtau.html"]
keywords = ["vượt sóng", "đại dương", "biển đảo", "tàu cao tốc", "tâm linh", "lịch sử", "cảng", "đại dương"]

report = []
for filename in files:
    report.append(f"\n===== SCANNING {filename} =====")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        found = [kw for kw in keywords if kw in line_lower]
        if found:
            report.append(f"Line {idx+1}: {line.strip()} (Matched: {found})")

with open("scratch/ocean_leftovers_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("Wrote ocean_leftovers_results.txt successfully!")
