import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/tab4_content.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("Cơm Niêu Sài Gòn Côn Đảo")
if idx != -1:
    print(text[idx-50:idx+1500])
else:
    print("Cơm Niêu Sài Gòn Côn Đảo not found in tab4")
