# -*- coding: utf-8 -*-
import re

def find_unbalanced_parenthesis(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
    for idx, script in enumerate(scripts):
        if "tailwind.config" in script or len(script.strip()) < 50:
            continue
            
        round_br = 0
        in_string = False
        string_char = None
        in_line_comment = False
        in_block_comment = False
        
        i = 0
        while i < len(script):
            char = script[i]
            
            if in_block_comment:
                if char == "*" and i + 1 < len(script) and script[i+1] == "/":
                    in_block_comment = False
                    i += 2
                    continue
                i += 1
                continue
                
            if in_line_comment:
                if char == "\n":
                    in_line_comment = False
                i += 1
                continue
                
            if in_string:
                if char == "\\":
                    i += 2
                    continue
                if char == string_char:
                    in_string = False
                i += 1
                continue
                
            if char == "/" and i + 1 < len(script):
                if script[i+1] == "/":
                    in_line_comment = True
                    i += 2
                    continue
                elif script[i+1] == "*":
                    in_block_comment = True
                    i += 2
                    continue
                    
            if char in ['"', "'", "`"]:
                in_string = True
                string_char = char
                i += 1
                continue
                
            if char == "(":
                round_br += 1
            elif char == ")":
                round_br -= 1
                if round_br < 0:
                    print(f"Unbalanced ')' at position {i}:")
                    start = max(0, i - 100)
                    end = min(len(script), i + 100)
                    print(script[start:end].encode('ascii', 'backslashreplace').decode('ascii'))
                    return
            i += 1
            
        if round_br != 0:
            print(f"Parenthesis count is unbalanced at end: count={round_br}")

if __name__ == "__main__":
    find_unbalanced_parenthesis("condao.html")
