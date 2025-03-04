import sys
import black
import re
import black


def pretty_print(source):
	"""
	Format Python source code using Black.
	This function uses Black's API to format the code.
	Then, it replaces every group of 4 spaces with a tab to enforce tab-only indentation.
	The pretty printed code is printed for verification.
	"""
	
	mode = black.FileMode(line_length=500, target_versions={black.TargetVersion.PY38})
	try:
	
		formatted = black.format_str(source, mode=mode)
		formatted = re.sub(r"( {4})", "\t", formatted)
		print(");   // pretty printed code:")                    # output ////
		print(formatted)
		return formatted
	except black.NothingChanged:
		print(" black made no changes")
		return source
		
	
language = "python"
comment_marker = "#"
blockTypeRules = [
	{"type": "input",  "regex": r"^def\s+\w+\s*\(.*\):"},
	{"type": "branch", "regex": r"^if\s+.*:"},
	{"type": "path",   "regex": r"^(elif|else)\b.*:"},
	{"type": "loop",   "regex": r"^(for|while)\s+.*:"},
	{"type": "try",    "regex": r"^try\s*:"},
	{"type": "except", "regex": r"^except\b.*:"},
	{"type": "finally","regex": r"^finally\s*:"},
	{"type": "with",   "regex": r"^with\s+.*:"}
	]
closureMapping = {
	"input": "end",
	"branch": "bend",
	"path": "bend",
	"loop": "lend",
	"try": "end",
	"except": "end",
	"finally": "end",
	"with": "end"
	}
outputRules = [
	{"regex": r"print\s*\(", "tag": "output"},
	{"regex": r"^\s*return\b", "tag": "output"}
	]
	

singleLineExpansions = []
global _tag_stack
_tag_stack = []
def reset_tag_stack():
	"""
	Reset the language module's internal tag stack.
	"""
	
i = 0
def tagMapper(line, indentTag, lineNumber):
	global i
	global _tag_stack
	
	
	
	cleaned = re.sub(r"\s*"+re.escape(comment_marker)+r"\s*tag.*", "", line).strip()
	
	print(f"DEBUG: Line {lineNumber} {i} ({ indentTag  }): {line} ")
	if indentTag == 'tagA'  or indentTag == 'tagX'    :
	
		if re.match(r"^if\s+", cleaned, re.IGNORECASE):
		
			_tag_stack.append("bend")
			return "branch"
		elif re.match(r"^(for|while)\s+", cleaned, re.IGNORECASE):
			_tag_stack.append("lend")
			return "loop"
		elif re.match(r"^def\s+\w+\s*\(.*\):", cleaned):
			_tag_stack.append("end")
			return "input"
		elif re.match(r"^(elif|else)\b", cleaned, re.IGNORECASE):
			return "path"
		elif re.match(r"^try\s*:", cleaned):
			_tag_stack.append("bend")
			return "branch"
		elif re.match(r"^except\b", cleaned, re.IGNORECASE):
			return "path"
		elif re.match(r"^finally\s*:", cleaned, re.IGNORECASE):
			return "path"
		elif re.match(r"^with\s+", cleaned, re.IGNORECASE):
			_tag_stack.append("bend")
			return "branch"
		else:
			_tag_stack.append("tag")
			return "tag"
			
	else:
		if _tag_stack:
		
			return _tag_stack.pop()
		else:
			return "tag"
			
		
	
if __name__ == "__main__":
	if len(sys.argv) > 1:
	
		with open(sys.argv[1], "r", encoding="utf-8") as f:
		
			source = f.read()
			
		pretty = pretty_print(source)
		print(pretty)
	else:
		print("\nUsage: python python_lang.py <source_file>")
		
	
	
#  Export  Date: 02:04:14 PM - 04:Mar:2025.

