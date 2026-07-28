import os

with open(r'f:\M_100184\templates\employees.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")

for idx, script in enumerate(scripts):
    print(f"\n--- Checking Script Block {idx+1} (Length: {len(script)}) ---")
    open_braces = 0
    lines = script.split('\n')
    error_line = -1
    for line_idx, line in enumerate(lines):
        for char in line:
            if char == '{':
                open_braces += 1
            elif char == '}':
                open_braces -= 1
                if open_braces < 0 and error_line == -1:
                    error_line = line_idx + 1
                    print(f"UNEXPECTED '}}' at line {line_idx+1}: {line}")
    print(f"Final open_braces count: {open_braces}")
    if error_line != -1:
        print(f"First unexpected closing brace at line {error_line}")





