# -*- coding: utf-8 -*-
files = ["dalat.html", "vinhhy.html", "vungtau.html"]
for filename in files:
    print(f"\n===== KEYS in {filename} =====")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "const KEYS =" in line:
            for offset in range(-1, 10):
                print(f"Line {idx+1+offset}: {lines[idx+offset].strip()}")
