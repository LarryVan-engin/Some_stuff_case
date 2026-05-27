# -*- coding: utf-8 -*-
import re

with open("dalat.html", "r", encoding="utf-8") as f:
    content = f.read()

report = []
for var in ["DEFAULT_DESTINATIONS", "DEFAULT_HOTELS", "DEFAULT_FOOD"]:
    pattern = r"const\s+" + var + r"\s*=\s*\[([\s\S]*?)\];"
    m = re.search(pattern, content)
    if m:
        report.append(f"=== {var} ===")
        report.append(m.group(0))
    else:
        report.append(f"{var} NOT FOUND")

with open("scratch/view_defaults_report.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(report))
print("Wrote view_defaults_report.txt successfully!")
