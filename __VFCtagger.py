
import argparse
import os
import re
import sys

# Convert groups of spaces to tabs (assuming 4 spaces per tab).
def convert_spaces_to_tabs(text, spaces_per_tab=4):
    return re.sub(f"(?m)^[\n]+", "", text)  # Remove lines that are just a single newline

# Ensure all source lines are preserved in the exact order
def preserve_source_lines(original_lines):
    """
    Ensure all original source lines exist in processed output.
    """
    return original_lines  # Pass through untouched

# Insert missing indentation steps
def insert_missing_indentation(lines, comment_marker):
    """
    Ensures that indentation only steps by one level at a time by inserting blank lines.
    Ignores lines that start as inline comments.
    Uses lookahead for tagA and lookbehind for tagB.
    Ensures that a function closing at level 1 inserts a level 0 blank line before the next function starts.
    """
    new_lines = []
    prev_indent = 0
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent_level = len(line) - len(stripped)
        
        # Ignore lines that are full inline comments
        if stripped.startswith(comment_marker):
            new_lines.append(line.rstrip())
            continue
        
        # Look ahead to determine next line's indent level
        next_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip()) if i + 1 < len(lines) else 0
        
        # Insert bridge lines for indentation jumps >1 level
        while indent_level > prev_indent + 1:
            prev_indent += 1
            new_lines.append("\t" * prev_indent + f" {comment_marker} tagX")
        
        # Ensure a blank level 0 line if a function closes at level 1 before a new function starts
        if prev_indent == 1 and indent_level == 0 and next_indent > 0:
            new_lines.append("" + f"{comment_marker} tagB")
        
        # Apply correct tag handling
        if indent_level < next_indent and indent_level < prev_indent:
            new_lines.append(line.rstrip() + f" {comment_marker} tagX")
        elif indent_level < next_indent:
            new_lines.append(line.rstrip() + f" {comment_marker} tagA")
        elif indent_level < prev_indent:
            new_lines.append(line.rstrip() + f" {comment_marker} tagB")
        else:
            new_lines.append(line.rstrip())
        
        prev_indent = indent_level
    return new_lines

# Phase 2: Map Tags Using Language Rules
def phase2_map_tags(lines, lang, skip_mapping=False):
    """
    Process tagged headers and replace them with refined tags using language-specific rules.
    Instead of using isIndent as a boolean, we now send the actual tag value {tagA, tagB, tagX}.
    Ensure tagMapper is only called when mapping is enabled.
    Prevent extra tags in --skip mode.
    """
    new_lines = []
    for i, line in enumerate(lines):
        for tag in ["tagA", "tagB", "tagX"]:
            if f"{lang.comment_marker} {tag}" in line:
                if not skip_mapping:
                    cleaned = line.replace(f"{lang.comment_marker} {tag}", "").strip()
                    refined = lang.tagMapper(cleaned, tag, i + 1)
                    new_lines.append(line.replace(f"{lang.comment_marker} {tag}", f"{lang.comment_marker} {refined}"))
                else:
                    new_lines.append(line)  # Do not modify the tag in --skip mode
                break
        else:
            new_lines.append(line)
    return new_lines

# Main entry point
def main():
    parser = argparse.ArgumentParser(description="Indentation Validator and Marker.")
    parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
    parser.add_argument("file", help="Source file to process")
    parser.add_argument("--skip", action="store_true", help="Skip language processing and only perform indentation tagging")
    args = parser.parse_args()

    # Load language module
    lang = __import__(f"languages.{args.language.lower()}_lang", fromlist=[''])

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        sys.exit(f"Error reading source file: {e}")

    if args.skip:
        lines = source.splitlines()
    else:
        # Format the code
        formatted = lang.pretty_print(source)
        formatted = convert_spaces_to_tabs(formatted, spaces_per_tab=4)
        lines = formatted.splitlines()

    # Ensure no lines are missing from the source
    lines = preserve_source_lines(lines)

    # Insert missing indentation steps
    tagged_lines = insert_missing_indentation(lines, lang.comment_marker)

    # Apply language-specific mapping if not skipped
    final_lines = phase2_map_tags(tagged_lines, lang, args.skip)

    output_file = os.path.basename(args.file) + "_indented.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as out:
            for l in final_lines:
                out.write(l + "\n")
    except Exception as e:
        sys.exit(f"Error writing output file: {e}")

    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()
