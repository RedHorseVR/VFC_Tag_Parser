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
#  Export  Date: 12:20:59 AM - 07:Mar:2025.

