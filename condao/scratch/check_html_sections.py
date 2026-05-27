import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find sections and count tags inside each section to see if tags are balanced within each section.
# We will look at sections with id='tab1', id='tab2', id='tab3', id='tab4'
# To do this cleanly, we can find the start of each section and check div balancing.

sections = [
    ('tab1', html.find('id="tab1"')),
    ('tab2', html.find('id="tab2"')),
    ('tab3', html.find('id="tab3"')),
    ('tab4', html.find('id="tab4"')),
    ('end_main', html.find('</main>'))
]

sections.sort(key=lambda x: x[1])

for i in range(len(sections) - 1):
    name, start = sections[i]
    next_name, end = sections[i+1]
    sec_content = html[start:end]
    
    # count opening and closing divs
    open_divs = sec_content.count('<div')
    close_divs = sec_content.count('</div>')
    open_sec = sec_content.count('<section')
    close_sec = sec_content.count('</section>')
    
    print(f"Section {name}:")
    print(f"  Length: {len(sec_content)}")
    print(f"  Opening <div: {open_divs}, Closing </div>: {close_divs}")
    print(f"  Opening <section: {open_sec}, Closing </section>: {close_sec}")
