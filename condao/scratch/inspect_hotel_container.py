import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for "Six Senses Côn Đảo" and print its parent div
idx = html.find("Six Senses Côn Đảo")
if idx != -1:
    # Find the nearest <div class="..." id="..."> before it
    # We can print the 800 characters before it
    print(html[idx-1000:idx])
