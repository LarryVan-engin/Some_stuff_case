import sys

# Reconfigure stdout to use utf-8 so printing Vietnamese characters won't crash on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i >= 3100: # let's search from line 3100 to end
        if any(term in line.lower() for term in ['switchtab', 'tab-content', 'document.queryselector', 'btn', 'active']):
            print(f"{i+1}: {line.strip()}")
