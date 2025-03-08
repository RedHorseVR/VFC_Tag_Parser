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
		
		formatted = add_block_end_comments( formatted )
		with open( 'pretty.py' , 'w' ) as write_file :
		
			write_file.write( formatted )
			
		return formatted
	except black.NothingChanged:
		print(" black made no changes")
		return source
		
	
import sys

stack = []
def pop():
	if len(stack) == 0:
	
		return "Stack is empty"
		
	return stack.pop()

def push(item):
	stack.append(item)
	
def add_block_end_comments(code_str):
	lines = code_str.split("\n")
	result = []
	end_comments = {
	
		"def": "#enddef-------------- ",
		"if": "#endif----------------",
		"for": "#endfor--------------",
		"while": "#endwhile--------------",
		"try": "#endtry--------------",
		"class": "#endclass--------------"
		}
	
	paths = ["else", "elif", "except", "finally", "with"]
	heads = ["def", "if", "for", "while", "try", "class"]
	
	prev_indent = None
	
	i = 0
	prev_indent = 0
	prevline = ""
	while i < len(lines):
		line = lines[i]
		if len(lines) - 1 > i:
		
			nextline = lines[i + 1]
			
		if i > 0:
		
			prevline = lines[i - 1]
			
		
		stripped = line.strip()
		if stripped:
		
			current_indent = len(line) - len(stripped)
			
			if current_indent < prev_indent:
			
				
				prev_level = 0
				if i > 0:
				
					prev_level = len(lines[i - 1]) - len(lines[i - 1].lstrip("\t"))
					
				
				this_level = len(line) - len(line.lstrip("\t"))
				diff_level = prev_level - this_level
				for lev in range(0, diff_level):
					if any(word in line for word in heads) and not any(tok in line for tok in paths):
					
						
						result.append("\t" * (current_indent) + f" ")
					else:
						if not any(word in prevline for word in paths):
						
							pass
							
						
					
					if not any(word in line for word in paths):
					
						result.append("\t" * (current_indent + diff_level - lev) + " ")
						
									
				
			
			
			
			prev_indent = current_indent
			
		
		result.append(line)
		
		if stripped.endswith(":"):
		
			first_word = stripped.split()[0]
			
			if first_word in end_comments:
			
				
				indent = len(line) - len(stripped)
				j = i + 1
				while j < len(lines):
					next_line = lines[j]
					next_stripped = next_line.strip()
					
					if not next_stripped:
					
						j += 1
						continue
						
					next_indent = len(next_line) - len(next_stripped)
					
					if next_indent <= indent:
					
						
						
						push(first_word)
						break
						
					j += 1
									
				
				if j == len(lines):
				
					result.append("/t." * indent + end_comments[first_word])
					
				
				
			
		
		
		i += 1
			
	
	return "\n".join(result)
if __name__ == "__main__":

	if len(sys.argv) > 1:
	
		
		with open(sys.argv[1], "r", encoding="utf-8") as f:
		
			source = f.read()
			
		pretty = pretty_print(source)
		if   pretty == None  :
		
			print( "pretty was None " )
		else:
			with open( 'pretty.py' , 'w' ) as write_file :
			
				write_file.write(pretty)
				
			
		#  // output //
	else:
		print("\nUsage: python python_lang.py <source_file>")
		
else:
	from languages.function import add_block_end_comments
	


language = "python"
comment_marker = "#"
multiline_comment_start = '"""'
multiline_comment_end = '"""'
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
			return "tag-----<<<"
			
	else:
		if _tag_stack:
		
			return _tag_stack.pop()
		else:
			return "tag"
			
		
	
#  Export  Date: 02:57:58 PM - 08:Mar:2025.

