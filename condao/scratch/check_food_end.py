import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for the pattern near the end of tab4
tab4_end = html.find('</section>', html.find('<section id="tab4"'))
if tab4_end != -1:
    print("End of tab4 context:")
    print(html[tab4_end-300:tab4_end+50])
