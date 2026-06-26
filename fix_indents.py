import os
import glob
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    changed = False
    inside_func = False
    
    for i in range(len(lines)):
        line = lines[i]
        
        if line.startswith("def "):
            inside_func = True
            continue
            
        if inside_func:
            if line.strip() == "":
                continue
                
            indent = len(line) - len(line.lstrip())
            if indent == 0 and not line.startswith("if __name__"):
                # Found a line with 0 indentation right after a function def!
                lines[i] = "    " + line
                changed = True
            
            # Stop checking after we find the first non-empty line
            inside_func = False

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print("Fixed indentation in " + filepath)

def main():
    for root, dirs, files in os.walk(r"f:\rhino-plugins"):
        for file in files:
            if file.endswith(".py"):
                fix_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
