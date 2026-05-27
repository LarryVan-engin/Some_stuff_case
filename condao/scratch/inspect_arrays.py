# -*- coding: utf-8 -*-
import re

filenames = ["dalat.html", "vungtau.html", "vinhhy.html"]
report = []

for filename in filenames:
    report.append(f"=== {filename} ===")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    for var in ["DEFAULT_DESTINATIONS", "DEFAULT_HOTELS", "DEFAULT_FOOD"]:
        pattern = r"const\s+" + var + r"\s*=\s*\[([\s\S]*?)\];"
        m = re.search(pattern, content)
        if m:
            names = re.findall(r'"name":\s*"([^"]+)"', m.group(1))
            if not names:
                names = re.findall(r"'name':\s*'([^']+)'", m.group(1))
            report.append(f"  {var} (count={len(names)}):")
            for name in names[:8]:
                report.append(f"    - {name}")
        else:
            report.append(f"  {var} NOT FOUND")

with open("scratch/inspect_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("Wrote inspect_report.txt successfully!")
