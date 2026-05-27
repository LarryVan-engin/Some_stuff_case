import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's print index.html from 201000 to 201200
print(html[201000:201200])
