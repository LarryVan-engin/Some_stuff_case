import sys, re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract script content
script_matches = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
for i, script in enumerate(script_matches):
    # Check for unmatched braces
    open_b = script.count('{')
    close_b = script.count('}')
    open_p = script.count('(')
    close_p = script.count(')')
    open_sq = script.count('[')
    close_sq = script.count(']')
    print(f"Script {i+1}: len={len(script)}, {{}} = {open_b}/{close_b}, () = {open_p}/{close_p}, [] = {open_sq}/{close_sq}")
    if open_b != close_b:
        print(f"  WARNING: UNMATCHED BRACES")
    if open_p != close_p:
        print(f"  WARNING: UNMATCHED PARENS")

print("\nKey function checks:")
key_funcs = ['switchTab', 'openAdminPanel', 'checkAdminPass', 'checkMemPass', 'renderMemoryAlbums', 'openLightbox', 'saveDestination', 'saveHotel', 'saveFood']
for fn in key_funcs:
    print(f"  {fn}: {'FOUND' if fn in html else 'MISSING!'}")
