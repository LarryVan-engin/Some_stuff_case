import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Let's check what's inside index.html for tab3
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tab3_idx = html.find('id="tab3"')
tab4_idx = html.find('id="tab4"')
tab3_block = html[tab3_idx:tab4_idx]

print("Tab3 block length:", len(tab3_block))
print("Tab3 block first 500 chars:")
print(tab3_block[:500])
print("\nTab3 block last 500 chars:")
print(tab3_block[-500:])

# Let's count how many times 'destination-card' appears in index.html
print("\nNumber of times 'destination-card' appears in index.html:", html.count('destination-card'))
print("Number of times 'Six Senses' appears in index.html:", html.count('Six Senses'))
