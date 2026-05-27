# -*- coding: utf-8 -*-
import re

def show_context(filename, char_pos):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
    for idx, script in enumerate(scripts):
        if "tailwind.config" in script or len(script.strip()) < 50:
            continue
            
        print(f"Context in {filename} around position {char_pos}:")
        start = max(0, char_pos - 100)
        end = min(len(script), char_pos + 100)
        
        # print safe slice
        context_slice = script[start:end].encode('ascii', 'backslashreplace').decode('ascii')
        print(f"--- START SLICE ---")
        print(context_slice)
        print(f"--- END SLICE ---")
        
        # Highlight position
        pos_in_slice = char_pos - start
        print(f"Pointer at index in slice: {pos_in_slice}")
        if pos_in_slice >= 0 and pos_in_slice < len(context_slice):
            print(f"Character at pointer is: '{script[char_pos]}'")

if __name__ == "__main__":
    show_context("dalat.html", 16577)
    show_context("vungtau.html", 16760)
    show_context("vinhhy.html", 16403)
