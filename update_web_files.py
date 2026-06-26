import os
import re

def process_web_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Preserve the existing GPL v3 license header
    license_pattern = re.compile(r'(/\*[\s\S]*?Copyright[\s\S]*?Spacio Techtonics[\s\S]*?\*/)', re.IGNORECASE)
    license_match = license_pattern.search(content)
    
    if license_match:
        placeholder = "@@LICENSE_PLACEHOLDER@@"
        content = content.replace(license_match.group(1), placeholder)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove JS single line comments (but not URL http:// or https://)
    # The negative lookbehind ensures we don't match the // in https://
    content = re.sub(r'(?<!:)//.*', '', content)
    
    # Remove CSS/JS multi-line comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    
    # Restore the license header
    if license_match:
        content = content.replace("@@LICENSE_PLACEHOLDER@@", license_match.group(1))

    # Clean up excessive empty lines left behind by comment removal
    content = re.sub(r'\n\s*\n', '\n', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed and cleaned comments in: {filepath}")

def main():
    files_to_process = [
        r'f:\rhino-plugins\BlueWhale\assets\map_selector.html',
        r'f:\rhino-plugins\Peacock\www\index.html'
    ]
    
    for file in files_to_process:
        process_web_file(file)

if __name__ == "__main__":
    main()
