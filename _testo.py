import argparse
import os
import re
import sys


def load_language_module(lang_name):
	lang_name = lang_name.lower()
	if lang_name == "javascript":
	
		import languages.javascript_lang as mod
	elif lang_name == "python":
		import languages.python_lang as mod
	elif lang_name == "perl":
		import languages.perl_lang as mod
	else:
		sys.exit("Unsupported language: " + lang_name)
		
		
	return mod



def convert_spaces_to_tabs(text, spaces_per_tab=4):
	return re.sub(" {" + str(spaces_per_tab) + r"}", "\t", text)



def phase1_reindent(lines, comment_marker):
	"""
	Assumes the source has been pretty printed.
	Reindent the code using a simple brace counter.
	Every line that ends with "{" or starts with "}" is appended with the generic tag " tag".
	Additionally, if a control statement does not end with "{" but the following line is a lone "{",
	then mark the control statement with " tag-header" and the brace line with " tag-brace".
	"""
	indent_level = 0
	new_lines = []
	i = 0
	while i < len(lines):
		line = lines[i].rstrip()
		
		if i < len(lines) - 1 and not line.rstrip().endswith("{"):
		
			next_line = lines[i + 1].rstrip()
			if next_line.strip() == "{" or next_line.strip().startswith("{" + " " + comment_marker + " tag"):
			
				new_indent = "\t" * indent_level
				
				if comment_marker + " tag-header" not in line:
				
					new_lines.append(new_indent + line.strip() + " " + comment_marker + " tag-header")
				else:
					new_lines.append(new_indent + line.strip())
					
					
				indent_level += 1
				new_indent = "\t" * indent_level
				
				if comment_marker + " tag-brace" not in next_line:
				
					new_lines.append(new_indent + next_line.strip() + " " + comment_marker + " tag-brace")
				else:
					new_lines.append(new_indent + next_line.strip())
					
					
				i += 2
				continue
				
				
				
			
			
		
		stripped = line.strip()
		if stripped.startswith("}"):
		
			indent_level = max(0, indent_level - 1)
			
			
		new_indent = "\t" * indent_level
		if stripped.endswith("{") or stripped.startswith("}"):
		
			if comment_marker + " tag" not in stripped:
			
				new_lines.append(new_indent + stripped + " " + comment_marker + " tag")
			else:
				new_lines.append(new_indent + stripped)
				
			
		else:
			new_lines.append(new_indent + stripped)
			if stripped.endswith("{"):
			
				indent_level += 1
				
				
			i += 1
			
			
		return new_lines
		
	
	
	
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
	stack = []
	line_num = 0
	
	
	def remove_marker(line, marker):
		return re.sub(r"\s*" + re.escape(comment_marker) + r"\s*" + re.escape(marker), "", line)
		
	
		for line in lines:
			line_num += 1
			
			if comment_marker + " tag-header" in line:
			
				header_line = line
				cleaned = remove_marker(header_line, "tag-header").rstrip()
				refined = lang.tagMapper(cleaned, True, line_num)
				new_header = re.sub(
				r"\s*" + re.escape(comment_marker) + r"\s*tag-header",
				" " + comment_marker + " " + refined,
				header_line,
				
				
				)
				new_lines.append(new_header)
				expected = lang.closureMapping.get(refined, refined)
				stack.append(expected)
				continue
				
				
			
			if comment_marker + " tag-brace" in line:
			
				new_brace = re.sub(
				r"\s*" + re.escape(comment_marker) + r"\s*tag-brace",
				" " + comment_marker + " path",
				line,
				
				
				)
				new_lines.append(new_brace)
				continue
				
			
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
					new_line = re.sub(
					r"\s*" + re.escape(comment_marker) + r"\s*tag",
					" " + comment_marker + " " + refined,
					line,
					
					
					)
					new_lines.append(new_line)
					expected = lang.closureMapping.get(refined, refined)
					stack.append(expected)
					continue
					
				
				if stripped.startswith("}") and (comment_marker + " tag") in stripped:
				
					base_line = re.sub(r"\s*" + re.escape(comment_marker) + r"\s*tag", "", line).rstrip()
					refined = lang.tagMapper(base_line, False, line_num)
					new_line = base_line + " " + comment_marker + " " + refined
					new_lines.append(new_line)
					continue
					
				
				
			
			new_lines.append(line)
			
			
		
		return new_lines
		
	
	
def main():
	parser = argparse.ArgumentParser(description="VFCtagger: Pretty print and tag code with structure.")
	parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
	parser.add_argument("file", help="Source file to tag")
	args = parser.parse_args()
	
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
			
		
		formatted = lang.pretty_print(source)
		
		formatted = convert_spaces_to_tabs(formatted, spaces_per_tab=4)
		lines = formatted.splitlines()
		
		lang.reset_tag_stack()
		
		phase1_lines = phase1_reindent(lines, lang.comment_marker)
		
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

	main()
	
#  Export  Date: 03:04:59 PM - 08:Mar:2025.

