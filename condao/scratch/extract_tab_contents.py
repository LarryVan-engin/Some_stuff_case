import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's write out the content of section tab3 and tab4 to helper files so we can read them easily
tab3_start = html.find('<section id="tab3"')
tab4_start = html.find('<section id="tab4"')
tab5_start = html.find('<section id="tab5"')

with open('scratch/tab3_content.html', 'w', encoding='utf-8') as f:
    f.write(html[tab3_start:tab4_start])

with open('scratch/tab4_content.html', 'w', encoding='utf-8') as f:
    f.write(html[tab4_start:tab5_start])

print("Wrote scratch/tab3_content.html and scratch/tab4_content.html")
