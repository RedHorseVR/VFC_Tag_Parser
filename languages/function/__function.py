import sys #event

stack = []
def pop():
	if len(stack) == 0:
		return "Stack is empty"
	return stack.pop()

def push( item ):
	stack.append(item)
	

def add_block_end_comments(code_str):

	lines = code_str.split('\n')
	result = []
	
	# Define end comments for each block type
	end_comments = {
		"def": "#enddef-------------- ",
		"if": "#endif----------------",
		"for": "#endfor--------------",
		"while": "#endwhile--------------",
		"try": "#endtry--------------",
		"class": "#endclass--------------"
	}
	
	paths = ["else", "elif", "except", "finally", "with"]
	heads = [ "def", "if", "for", "while", "try", "class"]
	
	# Track previous indentation level
	prev_indent = None
	

	# Process each line
	i = 0
	prev_indent = 0
	prevline = ''
	while i < len(lines):
		line = lines[i]
		if len(lines)-1 > i : nextline = lines[i+1]
		if i>0 : prevline = lines[i-1]
		
		# Calculate current indentation
		stripped = line.strip()
		if stripped:  # Only process non-empty lines
			current_indent = len(line) - len(stripped)
			
			# Check if indentation decreased by one level (4 spaces or 1 tab)
			if current_indent < prev_indent:
				# line indentation decreasing
				
				prev_level=0
				if i>0 : prev_level = len(lines[i-1]) - len(lines[i-1].lstrip('\t'))
				this_level = len(line)- len(line.lstrip('\t'))	
				diff_level = prev_level - this_level
				
					
				for lev in range(0,diff_level) : #iterate over drop in indentation 
					if( any(word in line for word in heads )  and not any(tok in line for tok in paths)  ) :  
						# head tag coming so lets prep a line for it unless a bridge coming.	 
						result.append('\t' * (current_indent) + f' ')#<-function.py-h')#
					else:
						if( not any(word in prevline for word in paths ) ) :  # not a path so we tag it
							pass #result.append('\t' * (current_indent+diff_level-lev) + '<-function.py-p') # + '#<' + pop() + f'> [{prev_level, this_level }]')
						
						
					if( not any(word in line for word in paths ) ) :  # not a path so we tag it
						result.append('\t' * (current_indent+diff_level-lev) + ' ')#<--function.py-n') # + '#<' + pop() + f'> [{prev_level, this_level }]')
					 
			 
			# Update previous indentation for next iteration
			prev_indent = current_indent
		
		# Add the current line
		result.append(line)
		
		# Check if this is a block start
		if stripped.endswith(':'):
			first_word = stripped.split()[0]
			
			# If this is a recognized block type
			if first_word in end_comments:
				# Find where this block ends
				indent = len(line) - len(stripped)
				j = i + 1
				while j < len(lines):
					next_line = lines[j]
					next_stripped = next_line.strip()
					
					# Skip empty lines
					if not next_stripped:
						j += 1
						continue
					
					next_indent = len(next_line) - len(next_stripped)
					
					# If next non-empty line has same or less indentation, we found the end of block
					if next_indent <= indent:
						# Add end comment before this line
						#result.append('\t' * indent + end_comments[first_word])
						push( first_word )
						break
					
					j += 1
				
				# If we reached the end of the file
				if j == len(lines):
					result.append('/t.' * indent + end_comments[first_word])
		
		i += 1
	
	return '\n'.join(result)