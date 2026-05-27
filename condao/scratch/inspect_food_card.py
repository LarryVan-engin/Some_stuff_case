import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/tab4_content.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for "Cơm Niêu Sài Gòn Côn Đảo" and print until the next card
start_idx = text.find("Cơm Niêu Sài Gòn Côn Đảo")
# Let's find the next card comment
next_comment = text.find("<!-- Card:", start_idx + 10)
if start_idx != -1 and next_comment != -1:
    print(text[start_idx-100:next_comment])
else:
    print(text[start_idx-100:start_idx+1500])
