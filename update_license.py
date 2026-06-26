import os
import subprocess

LICENSE_HEADER = """# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def should_keep_comment(comment_text):
    text = comment_text.lower()
    return "spacio techtonics" in text or "keshava narayan" in text


def refactor_file(filepath):
    try:
        # Use ruff to fix unused imports/variables and format the code
        subprocess.run(
            ["ruff", "check", "--fix", filepath],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["ruff", "format", filepath],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print(
            "Warning: 'ruff' not found. Skipping auto-refactoring. To enable, run: pip install ruff"
        )


def process_file(filepath):
    # First, refactor and remove unused code using ruff
    refactor_file(filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Could not read {filepath} as utf-8. Skipping.")
        return

    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Full line comment
        if stripped.startswith("#"):
            if (
                should_keep_comment(stripped)
                or "GNU General Public License" in line
                or "This program is free software" in line
            ):
                new_lines.append(line)
        # Inline comment
        elif "#" in line and not line.strip().startswith(('"', "'")):
            parts = line.split("#", 1)
            code_part = parts[0]
            comment_part = parts[1]
            if should_keep_comment(comment_part):
                new_lines.append(line)
            else:
                new_lines.append(code_part.rstrip() + "\n")
        else:
            new_lines.append(line)

    content = "".join(new_lines)
    # Ensure license header is added at top
    if "GNU General Public License" not in content:
        content = LICENSE_HEADER + "\n" + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    root_dir = r"f:\rhino-plugins"
    for subdir, _, files in os.walk(root_dir):
        if ".git" in subdir:
            continue
        for file in files:
            if file.endswith(".py") and file != "update_license.py":
                filepath = os.path.join(subdir, file)
                process_file(filepath)
                print(f"Processed: {filepath}")


if __name__ == "__main__":
    main()
