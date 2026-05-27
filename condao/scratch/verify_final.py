import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\VSCode\Some_stuff_case\condao\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Check JS braces
script_start = html.find('<script>')
script_end = html.find('</script>')
if script_start != -1 and script_end != -1:
    js = html[script_start:script_end]
    open_braces = js.count('{')
    close_braces = js.count('}')
    print(f"JS Braces: Open {open_braces}, Close {close_braces}")
    if open_braces != close_braces:
        print("WARNING: JS Braces are NOT balanced!")
    else:
        print("SUCCESS: JS Braces are balanced!")

# 2. Check HTML tags
# Let's count divs and sections
div_opens = html.count('<div')
div_closes = html.count('</div')
print(f"HTML Divs: Open {div_opens}, Close {div_closes}")
if div_opens != div_closes:
    print("WARNING: HTML Divs are NOT balanced!")
else:
    print("SUCCESS: HTML Divs are balanced!")
    
sec_opens = html.count('<section')
sec_closes = html.count('</section')
print(f"HTML Sections: Open {sec_opens}, Close {sec_closes}")
if sec_opens != sec_closes:
    print("WARNING: HTML Sections are NOT balanced!")
else:
    print("SUCCESS: HTML Sections are balanced!")
