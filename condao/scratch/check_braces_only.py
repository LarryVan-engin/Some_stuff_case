# -*- coding: utf-8 -*-
import re

def check_braces(filename):
    print(f"Verifying braces in {filename}...")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
    for idx, script in enumerate(scripts):
        if "tailwind.config" in script or len(script.strip()) < 50:
            continue
            
        # Count braces and brackets
        curly = 0
        square = 0
        round_br = 0
        
        # We also want to make sure we ignore comments or strings if they contain unbalanced characters, 
        # but a simple scan will give us a quick indication. Let's do a smart character scan:
        in_string = False
        string_char = None
        in_line_comment = False
        in_block_comment = False
        
        i = 0
        while i < len(script):
            char = script[i]
            
            # Handle block comments
            if in_block_comment:
                if char == "*" and i + 1 < len(script) and script[i+1] == "/":
                    in_block_comment = False
                    i += 2
                    continue
                i += 1
                continue
                
            # Handle line comments
            if in_line_comment:
                if char == "\n":
                    in_line_comment = False
                i += 1
                continue
                
            # Handle strings
            if in_string:
                if char == "\\":
                    i += 2 # skip escaped char
                    continue
                if char == string_char:
                    in_string = False
                i += 1
                continue
                
            # Check comment starts
            if char == "/" and i + 1 < len(script):
                if script[i+1] == "/":
                    in_line_comment = True
                    i += 2
                    continue
                elif script[i+1] == "*":
                    in_block_comment = True
                    i += 2
                    continue
                    
            # Check string starts
            if char in ['"', "'", "`"]:
                in_string = True
                string_char = char
                i += 1
                continue
                
            # Count braces
            if char == "{":
                curly += 1
            elif char == "}":
                curly -= 1
                if curly < 0:
                    print(f"  [ERROR] Unbalanced closing curly brace '}}' at character {i} in block {idx}")
                    return False
            elif char == "[":
                square += 1
            elif char == "]":
                square -= 1
                if square < 0:
                    print(f"  [ERROR] Unbalanced closing square bracket ']' at character {i} in block {idx}")
                    return False
            elif char == "(":
                round_br += 1
            elif char == ")":
                round_br -= 1
                if round_br < 0:
                    print(f"  [ERROR] Unbalanced closing round parenthesis ')' at character {i} in block {idx}")
                    return False
            i += 1
            
        if curly != 0:
            print(f"  [ERROR] Unbalanced curly braces in block {idx}: count={curly}")
            return False
        if square != 0:
            print(f"  [ERROR] Unbalanced square brackets in block {idx}: count={square}")
            return False
        if round_br != 0:
            print(f"  [ERROR] Unbalanced round parentheses in block {idx}: count={round_br}")
            return False
            
        print(f"  Block {idx}: All brackets and braces are PERFECTLY BALANCED!")
    return True

if __name__ == "__main__":
    success = True
    for f in ["condao.html", "dalat.html", "vungtau.html", "vinhhy.html"]:
        if not check_braces(f):
            success = False
            print(f"--- FAILURE in {f} ---\n")
        else:
            print(f"--- SUCCESS in {f} ---\n")
            
    if success:
        print("ALL SUBPAGES HAVE 100% PERFECTLY BALANCED SYNTAX!")
    else:
        print("SOME SUBPAGES CONTAIN SYNTAX ERROR BREAKS!")
