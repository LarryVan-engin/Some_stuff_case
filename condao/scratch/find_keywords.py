import re
import sys

# Reconfigure stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

keywords = ["Tri Kỷ", "Cơm niêu", "Bến Đầm", "Khách sạn", "Resort", "Six Senses"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, html)]
    print(f"Keyword '{kw}': found {len(matches)} times")
    if matches:
        idx = matches[0]
        start = max(0, idx - 150)
        end = min(len(html), idx + 250)
        print(f"Context:\n{html[start:end]}\n")
        print("-" * 80)
