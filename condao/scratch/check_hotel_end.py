import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for the pattern near the end of tab3
tab3_end = html.find('</section>', html.find('<section id="tab3"'))
if tab3_end != -1:
    print("End of tab3 context:")
    print(html[tab3_end-300:tab3_end+50])
