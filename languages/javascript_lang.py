import sys
import re
import subprocess

language = "JavaScript"
comment_marker = "//"
multiline_comment_start = "/*"
multiline_comment_end = "*/"

blockTypeRules = [
	{"type": "input", "regex": r"(async|function)\b\("},
	{"type": "branch", "regex": r"^if\s*\("},
	{"type": "path",   "regex": r"(else|catch|finally)\b"},
	{"type": "loop",   "regex": r"^(for\s*\(|while\s*\("}
	]
closureMapping = {
	"input": "end",
	"branch": "bend",
	"path": "bend",
	"loop": "lend"
	}
outputRules = [
	{"regex": r"\bconsole\.(log|info|error|warn)\s*\(", "tag": "output"},
	
	]
	
singleLineExpansions = [
{
	"name": "singleIf",
	"regex": r"^\s*if\s*\((.*?)\)\s*(?!\{)(.*);$",
	"replacement": [
	"if ($1) {",
	"\t$2;",
	"}"
	]
	},
{
	"name": "singleElse",
	"regex": r"^\s*else\s+(.*);$",
	"replacement": [
	"else {",
	"\t$1;",
	"}"
	]
	},
{
	"name": "singleFor",
	"regex": r"^\s*for\s*\((.*?)\)\s*(?!\{)(.*);$",
	"replacement": [
	"for ($1) {",
	"\t$2;",
	"}"
	]
	},
{
	"name": "singleWhile",
	"regex": r"^\s*while\s*\((.*?)\)\s*(?!\{)(.*);$",
	"replacement": [
	"while ($1) {",
	"\t$2;",
	"}"
	]
	}
	]
_tag_stack = []

def pretty_print(source):
	"""
	Format JavaScript source code using Prettier.
	This function calls 'npx prettier --use-tabs --stdin-filepath dummy.js'
	to read the source from STDIN and return the formatted code from STDOUT.
	"""
	try:
	
		result = subprocess.run(
		["npx", "prettier", "--use-tabs", "--print-width", "500", "--stdin-filepath", "dummy.js"],
		input=source.encode("utf-8"),
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		shell=True,
		check=True
		)
		tabbed_source = result.stdout.decode("utf-8")
	except subprocess.CalledProcessError as e:
		print("Error in pretty_print:", e.stderr.decode("utf-8"))
		return source
		
	return insert_comment_after_empty_if(tabbed_source)

def replace_match(match):
	if_part = match.group(1)
	whitespace = match.group(2)
	closing_brace = match.group(3)
	
	indent = re.match(r'\n(\s*)}', closing_brace).group(1)
	
	return f"{if_part}{whitespace}// tagA\n{indent}\t{closing_brace}"
def insert_comment_after_empty_if(source):
	pattern = r'(if\s*\([^)]*\)\s*{)(\s*)(\n\s*})'
	
	return re.sub(pattern, replace_match, source)




def reset_tag_stack():
	
	# Reset the language module's internal tag stack.
	
	global _tag_stack
	_tag_stack = []
	
i = 0
def tagMapper(line, indentTag, lineNumber):
	global i
	
	
	
	global _tag_stack
	cleaned = line.strip()
	print(f"DEBUG: Line {lineNumber} {i} ({ indentTag  }): {line} ")
	if indentTag == 'tagA'  or indentTag == 'tagX'    :
	
		if re.match(r"^(if\s*\()", cleaned, re.IGNORECASE):
		
			print( "--------->",  line  )
			_tag_stack.append("bend")
			rtnval =  "branch"
		elif re.match(r"^try", cleaned, re.IGNORECASE):
			_tag_stack.append("bend")
			rtnval =  "branch"
		elif re.match(r"^(for\s*\(|while\s*\()", cleaned, re.IGNORECASE):
			_tag_stack.append("lend")
			rtnval =  "loop"
		elif "async" in line :
			_tag_stack.append("end")
			rtnval =  "input---"
		elif re.match(r"function", line , re.IGNORECASE):
			_tag_stack.append("end")
			rtnval =  "input"
		elif re.match(r"(\}\s*else|\}\s*catch|finally)", cleaned, re.IGNORECASE):
			
			
			
			print( '------------------------------------------------')
			rtnval =  "path..."
		elif re.match(r"^(return|continue)", cleaned, re.IGNORECASE):
			rtnval =  "end"
		else:
			_tag_stack.append("tag")
			rtnval =  "process"
			
	else:
		if _tag_stack  and  indentTag == 'tagB' :
		
			i -=1
			rtnval =  _tag_stack.pop()
		else:
			if  re.match( r"^if\b", cleaned ) :
			
				_tag_stack.append("bend")
				rtnval =  "branch"
			else:
				rtnval =  "process"
				
			
		
	return rtnval

if __name__ == "__main__":
	if len(sys.argv) > 1:
	
		with open(sys.argv[1], "r", encoding="utf-8") as f:
		
			source = f.read()
			
		pretty = pretty_print(source)
		print(");   // === Final Pretty Printed Code ===")   # output ////
		print(pretty)
	else:
		print("Usage: python javascript_lang.py <source_file>")
		
	


#  Export  Date: 04:50:05 PM - 06:Mar:2025.

