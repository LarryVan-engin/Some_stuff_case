# -*- coding: utf-8 -*-
with open("dalat.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

report = []
for i, line in enumerate(lines):
    if "Côn Đảo" in line:
        report.append(f"Line {i+1}: {line.strip()}")

with open("scratch/leftovers_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("Wrote leftovers report successfully!")
