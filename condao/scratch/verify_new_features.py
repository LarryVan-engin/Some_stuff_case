import sys, re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check key elements exist
checks = {
    'tab5 section': 'id="tab5"',
    'admin-modal': 'id="admin-modal"',
    'admin-login-screen': 'id="admin-login-screen"',
    'admin-panel': 'id="admin-panel"',
    'btn-tab5': 'id="btn-tab5"',
    'btn-admin': 'id="btn-admin"',
    'mem-gate': 'id="mem-gate"',
    'mem-content': 'id="mem-content"',
    'lightbox-overlay': 'id="lightbox-overlay"',
    'site-footer': 'class="site-footer"',
    'footer-bottom': 'class="footer-bottom"',
    'admin-sec-dest': 'id="admin-sec-dest"',
    'admin-sec-hotel': 'id="admin-sec-hotel"',
    'admin-sec-food': 'id="admin-sec-food"',
    'admin-sec-mem': 'id="admin-sec-mem"',
    'admin-sec-settings': 'id="admin-sec-settings"',
}

all_ok = True
for name, pattern in checks.items():
    found = any(pattern in line for line in lines)
    status = '✓' if found else '✗ MISSING!'
    print(f"  {status} {name}")
    if not found: all_ok = False

print(f"\n{'All checks PASSED!' if all_ok else 'SOME CHECKS FAILED!'}")
print(f"Total lines: {len(lines)}")
