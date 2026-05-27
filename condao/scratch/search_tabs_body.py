import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'switchtab' in line.lower() or 'tab1' in line.lower() or 'tab2' in line.lower() or 'tab3' in line.lower() or 'tab4' in line.lower():
        if i < 3100: # before javascript
            print(f"{i+1}: {line.strip()}")
