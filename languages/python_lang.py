import sys
import black
import re
import black
import os


def pretty_print(source):
	
	try:
	
		os.system( f'black -l 500 -S -C  { source }'  )
	except :
		print(" black made no changes")
		
	
language = 'python'
commentmarker = '#'
multiline_comment_start = '"""'
multiline_comment_end = '"""'
literals =  ["'", '"', '`']

path_types = [ 'else', 'elif' ,'except', 'catch', 'case' ]
branch_types = [ 'if', 'with', 'try', 'switch'  ]
loop_types = [ 'for ', 'while ', 'do ', 'until '  ]
input_types = [ 'class', 'def'  ]
event_types = [ 'from ',  'import '  ]
output_types = [ 'print(', 'continue', '.write' ]
end_types = [ 'return ', 'return ' , 'exit(' ]

def  lang_check_path( line ):
	if any(word in line for word in path_types )  :
	
		newline  =  '\t' + line
	else:
		newline  =   line
		
	return newline
def  lang_filter( line ,  marked_file ):
	if scanTok( line , path_types )  :
	
		
		newline  =  '\t' + line + f'{ commentmarker } path '
	elif  scanTok( line,  branch_types  )   :
		push( 'bend' )
		marked_file.append(    line + f'{ commentmarker } branch  '  )
		newline =   '\n' + f'{ commentmarker } path'
	elif  scanTok( line, loop_types  ) :
		push( 'lend' )
		newline  =  line + f'{ commentmarker } loop '
	elif  scanTok( line, input_types  ) :
		if  'class' in line  :
		
			
			push( 'bend' )
			marked_file.append(  line + f'{ commentmarker } input ' )
			marked_file.append(  f'{ commentmarker } branch ' )
			marked_file.append(   f'{ commentmarker } path ' )
			
			newline  =   f'{ commentmarker } path '
		else:
			push( 'end' )
			
			
			newline  =  line + f'{ commentmarker } input '
			
	elif  scanTok( line, event_types  ) :
		newline  =  line + f'{ commentmarker } event '
	elif  scanTok( line, output_types  ) :
		newline  =  line + f'{ commentmarker } output '
	elif  scanTok( line, end_types  ) :
		newline  =  line + f'{ commentmarker } end '
	else:
		
		newline  =  line + f'{ commentmarker } set '
		
	return newline
stack = []
def  pop( ):
	global stack
	if len( stack) >0  :
	
		item = stack.pop()
		
		return item
	else:
		print( '--------------------empty stack----------------------------')
		return ""
		
	
def  push(  item ):
	global stack
	stack.append( item )
	
def  scanTok( line, toklist ):
	sub_list = [item for item in toklist if item.startswith('.')]
	subtok = any(f"{word}" in line for word in sub_list )
	if len(sub_list) > 0  and subtok  :
	
		return True
		
	return  any(line.lstrip().startswith(word) for word in toklist )
def  footer( exportname  ):
	
	ENVTOK = 'INSECTA'
	foot = f';{ENVTOK} EMBEDDED SESSION INFORMATION'
	foot+= '; 255 16777215 65280 16777088 16711680 13158600 13158600 0 255 255 9895835 6946660 16384'
	foot+= f';    { exportname } . '
	foot+='; notepad.exe'
	foot+=f';{ENVTOK} EMBEDDED ALTSESSION INFORMATION'
	foot+='; 389 43 901 2029 59 89   344   63    python.key  0'
	return foot
#  Export  Date: 06:56:51 PM - 25:Mar:2025.

