import argparse  # event
import os  # event
import re  # event
import sys  # event


# ----- Phase 2: Discriminate & Map Tags Using tagMapper() and a Stack -----
def phase2_map_tags(lines, comment_marker, lang):
    """
    Process lines marked with a generic tag.
    For header lines:
      - If a line contains "tag-header", remove that marker and call lang.tagMapper() with isIndent=True
        on the header's content. Replace the marker with the refined tag and push the expected closure (via lang.closureMapping)
        onto a local stack.
      - For the following line marked "tag-brace", simply replace its marker with " path".
      - For normal header lines (ending with "{ tag"), process similarly.
    For closing lines (lines starting with "}" with " tag"), call lang.tagMapper() with isIndent=False to get the refined closing tag.
    """
    new_lines = []
    stack = []  # local stack for expected closures
    line_num = 0

    def remove_marker(line, marker):
        return re.sub(r"\s*" + re.escape(comment_marker) + r"\s*" + re.escape(marker), "", line)

    for line in lines:
        line_num += 1
        # Process header line with "tag-header".
        if comment_marker + " tag-header" in line:
            header_line = line
            cleaned = remove_marker(header_line, "tag-header").rstrip()
            refined = lang.tagMapper(cleaned, True, line_num)
            new_header = re.sub(r"\s*" + re.escape(comment_marker) + r"\s*tag-header", " " + comment_marker + " " + refined, header_line)
            new_lines.append(new_header)
            expected = lang.closureMapping.get(refined, refined)
            stack.append(expected)
            continue

        # Process the following brace line marked "tag-brace".
        if comment_marker + " tag-brace" in line:
            new_brace = re.sub(r"\s*" + re.escape(comment_marker) + r"\s*tag-brace", " " + comment_marker + " path", line)
            new_lines.append(new_brace)
            continue
        # Process normal header lines with generic "tag".
        if comment_marker + " tag" in line:
            stripped = line.strip()
            if stripped.endswith("{ " + comment_marker + " tag"):
                header_line = line
                cleaned = remove_marker(header_line, "tag").rstrip()
                if cleaned.endswith("{"):
                    header_content = cleaned[:-1].strip()
                else:
                    header_content = cleaned.strip()

                refined = lang.tagMapper(header_content, True, line_num)
                new_line = re.sub(r"\s*" + re.escape(comment_marker) + r"\s*tag", " " + comment_marker + " " + refined, line)
                new_lines.append(new_line)
                expected = lang.closureMapping.get(refined, refined)
                stack.append(expected)
                continue

            # Process closing lines marked with generic "tag".
            if stripped.startswith("}") and (comment_marker + " tag") in stripped:
                base_line = re.sub(r"\s*" + re.escape(comment_marker) + r"\s*tag", "", line).rstrip()
                refined = lang.tagMapper(base_line, False, line_num)
                new_line = base_line + " " + comment_marker + " " + refined
                new_lines.append(new_line)
                continue
        # Lines without any generic marker pass through.
        new_lines.append(line)

    return new_lines


def main():

    parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
    parser.add_argument("file", help="Source file to tag")
    args = parser.parse_args()

    # Load language module.
    lang = None
    try:
        lang = load_language_module(args.language.lower())
    except Exception as e:
        sys.exit("Error loading language module: " + str(e))
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        sys.exit(f"Error reading source file: {e}")

    # Use the language module's pretty_print() function to format the code.
    formatted = lang.pretty_print(source)
    # Convert any spaces to tabs.
    formatted = convert_spaces_to_tabs(formatted, spaces_per_tab=4)
    lines = formatted.splitlines()

    # Reset the language module's tag stack.
    lang.reset_tag_stack()

    # Phase 1: Reindent and mark block headers/closers.
    phase1_lines = phase1_reindent(lines, lang.comment_marker)
    # Phase 2: Discriminate and map tags using the language module's tagMapper().
    final_lines = phase2_map_tags(phase1_lines, lang.comment_marker, lang)

    output_file = os.path.basename(args.file) + ".txt"
    try:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(f"{lang.comment_marker} TAGGED FOR VFC\n")
            out.write(f"{lang.comment_marker} TAGGED FOR VFC\n")
            for l in final_lines:
                out.write(l + "\n")
    except Exception as e:
        sys.exit(f"Error writing output file: {e}")

    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    # endif----------------
    # endif----------------
    # endif----------------
    main()
