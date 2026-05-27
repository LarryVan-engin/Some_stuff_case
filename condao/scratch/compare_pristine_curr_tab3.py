import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Read pristine tab3
with open('pristine_tab3_segment.html', 'r', encoding='utf-8') as f:
    pristine = f.read()

# Read current tab3 in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

t3_start = html.find('id="tab3"')
t4_start = html.find('id="tab4"')
curr_tab3 = html[t3_start:t4_start]

print("Pristine length:", len(pristine))
print("Current tab3 length:", len(curr_tab3))

# Check if 'six senses' is in both
print("Six Senses in Pristine:", 'Six Senses' in pristine)
print("Six Senses in Current:", 'Six Senses' in curr_tab3)

# Check for differences or differences in the number of hotels
print("Hotel occurrences in pristine:", pristine.lower().count('khách sạn') + pristine.lower().count('resort') + pristine.lower().count('nhà nghỉ'))
print("Hotel occurrences in current:", curr_tab3.lower().count('khách sạn') + curr_tab3.lower().count('resort') + curr_tab3.lower().count('nhà nghỉ'))
