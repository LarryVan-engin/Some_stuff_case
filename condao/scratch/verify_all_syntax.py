# -*- coding: utf-8 -*-
import subprocess
import re
import os

files = ["index.html", "dalat.html", "vinhhy.html", "vungtau.html"]

for filename in files:
    if not os.path.exists(filename):
        print(f"{filename} not found!")
        continue
    
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Find all <script> blocks (excluding external ones)
    # Using a regex that captures everything inside <script>...</script> except tags with src
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
    
    print(f"\n===== Checking syntax for {filename} =====")
    for idx, script_content in enumerate(scripts):
        # Skip empty script blocks or scripts with external source (which have no content)
        if not script_content.strip():
            continue
            
        # Write to a temp file
        temp_js = f"scratch_temp_{filename}_{idx}.js"
        with open(temp_js, "w", encoding="utf-8") as tf:
            tf.write(script_content)
        
        # Run node to compile and check syntax
        try:
            res = subprocess.run(["node", "-c", temp_js], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  Script block {idx+1}: OK")
            else:
                print(f"  Script block {idx+1}: SYNTAX ERROR!")
                print(res.stderr)
        except Exception as e:
            print(f"  Could not run Node for script block {idx+1}: {e}")
        finally:
            # Clean up temp file
            if os.path.exists(temp_js):
                os.remove(temp_js)
