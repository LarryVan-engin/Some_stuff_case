import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '3N2Đ' in line or '3 ngày 2 đêm' in line.lower():
        print(f"{i+1}: {line.strip()}")
