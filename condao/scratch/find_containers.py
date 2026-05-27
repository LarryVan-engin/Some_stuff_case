import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. destinations-container
idx1 = html.find('id="destinations-container"')
if idx1 != -1:
    print("Start of destinations-container:")
    print(html[idx1-50:idx1+150])
    
# Find where destinations-container ends
# It should end before </section> and before the start of Tab 2
# Let's find </section> after destinations-container
tab2_start = html.find('<section id="tab2"')
print("\nEnd of tab1 destinations (before tab2_start):")
print(html[tab2_start-300:tab2_start])

# 2. Scrollable list of hotels
idx3 = html.find('<!-- Scrollable list of hotels -->')
if idx3 != -1:
    print("\nStart of scrollable list of hotels:")
    print(html[idx3:idx3+250])
    
# It ends before the closing divs of tab3
tab4_start = html.find('<section id="tab4"')
print("\nEnd of tab3 (before tab4_start):")
print(html[tab4_start-300:tab4_start])

# 3. food-container
idx4 = html.find('id="food-container"')
if idx4 != -1:
    print("\nStart of food-container:")
    print(html[idx4-50:idx4+150])
    
tab5_start = html.find('<section id="tab5"')
print("\nEnd of tab4 (before tab5_start):")
print(html[tab5_start-300:tab5_start])
