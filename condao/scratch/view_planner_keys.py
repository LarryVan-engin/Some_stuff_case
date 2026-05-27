# -*- coding: utf-8 -*-
files = ["dalat.html", "vinhhy.html", "vungtau.html"]
report = []
for filename in files:
    report.append(f"\n===== Planner Keys in {filename} =====")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "localStorage" in line:
            report.append(f"Line {idx+1}: {line.strip()}")

with open("scratch/planner_keys_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("Wrote planner_keys_results.txt successfully!")
