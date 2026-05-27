import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/tab3_content.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("Six Senses Côn Đảo")
if idx != -1:
    print(text[idx-150:idx+800])
else:
    print("Six Senses Côn Đảo not found in tab3")
