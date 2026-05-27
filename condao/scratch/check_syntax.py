# -*- coding: utf-8 -*-
import re
import sys

def check_file(filename):
    print(f"Checking {filename}...")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all <script> blocks that are not linking to external files
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
    for idx, script in enumerate(scripts):
        # Skip Tailwind config scripts or small CDN scripts
        if "tailwind.config" in script or len(script.strip()) < 50:
            continue
            
        try:
            compile(script, f"{filename}_script_{idx}", "exec")
            print(f"  Script block {idx}: Syntax OK")
        except SyntaxError as e:
            print(f"  [SYNTAX ERROR] Script block {idx} in {filename} at line {e.lineno}:")
            print(f"    Line content: {e.text}")
            print(f"    Error: {e.msg}")

if __name__ == "__main__":
    for f in ["condao.html", "dalat.html", "vungtau.html", "vinhhy.html"]:
        check_file(f)
