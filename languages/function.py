def add_block_end_comments(code_str):

	lines = code_str.split('\n')
	result = []
	
	# Define end comments for each block type
	end_comments = {
		"if": "#endif----------------",
		#"elif": "#endif----------------",
		#"else": "#endif--------------",
		"for": "#endfor--------------",
		"while": "#endwhile--------------",
		"def": "#enddef-------------- ",
		"try": "#endtry--------------",
		#"except": "#endexcept--------------",
		#"finally": "#endfinally--------------",
		#"with": "#endwith--------------",
		"class": "#endclass--------------"
	}
	
	paths = ["else", "elif", "except", "finally", "with"]
	
	# Track previous indentation level
	prev_indent = None
	
	stack = []
	def pop():
		if len(stack) == 0:
			return "Stack is empty"
		return stack.pop()
	def push( item ):
		stack.append(item)
	
	# Process each line
	i = 0
	while i < len(lines):
		line = lines[i]
		
		# Calculate current indentation
		stripped = line.strip()
		if stripped:  # Only process non-empty lines
			current_indent = len(line) - len(stripped)
			
			# Check if indentation decreased by one level (4 spaces or 1 tab)
			if prev_indent is not None and current_indent < prev_indent:
				# Add dash line when indentation decreases
				indent_level=0
				if i>0 : indent_level = len(line) - len(line.lstrip('\t')) 
				if( not any(word in line for word in paths ) ) :  # not a path so we tag it
					result.append('\t' * (current_indent) + '<' + pop() + f'> [{indent_level}]')
				
			
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
						result.append('\t' * indent + end_comments[first_word])
						push( first_word )
						break
					
					j += 1
				
				# If we reached the end of the file
				if j == len(lines):
					result.append('/t.' * indent + end_comments[first_word])
		
		i += 1
	
	return '\n'.join(result)