import argparse
import os
import re
import sys
import importlib

lang = None
lang_commentmarker = ''

def  process_tabbed_file( tabfile ):
	TABS =0
	last_TAB = 0
	marked_file = []
	marked_line =  f'{ lang_commentmarker } set '
	
	marked_file.append( marked_line );
	marked_file.append( marked_line );
	for i in range ( 0 , len(tabfile) - 2 )  :
		line = tabfile[ i ]
		
		if  not  line.strip().startswith( lang_commentmarker )  :
		
			line = lang.lang_filter( line )
			last_TAB = TABS
			TABS = len( line ) - len( line.lstrip('\t') )
			nextline = lang.lang_check_path( tabfile[i+1] )
			next_TABS = len( nextline  ) - len( nextline.lstrip('\t') )
			tabrate = last_TAB-TABS
			next_tabrate = TABS - next_TABS
			if   next_tabrate == 1  :
			
				marked_line =  f'\t' * (TABS) + f'{ lang_commentmarker } { lang.pop() } '
				marked_file.append( marked_line );
				
			else:
				marked_line =  f'{line}'
				marked_file.append( marked_line );
				
			
			for rate in range( 2, next_tabrate ):
				marked_line =  f'\t' * (TABS) + f'{ lang_commentmarker } { lang.pop() } '
				marked_file.append( marked_line );
							
		else:
			newline = line.replace( "\t" , "" )
			marked_line =  f'{ newline  } {lang_commentmarker} set'
			marked_file.append( marked_line );
			
			
			
	
	return marked_file
def gettabbed_file(filename):
	filename = filename.strip()
	print( '------------------------------------------------')
	print( filename )
	tabbed_file = []
	try:
	
		LINE = ' '
		TABS =0
		with open(filename, 'r') as file:
		
			IN_COMMENT_BLOCK = False;
			i = 0
			last_TAB = 0
			for line in file:
				linet = line.replace('    ', '\t').strip( "\n" )
				LINE2 = line.replace('    ', '\t').strip( "\n" )
				if  not linet.strip() == ''    :
				
					if  not IN_COMMENT_BLOCK and not line.startswith('\n')  and not line.lstrip().startswith('#') :
					
						i +=1
						IN_COMMENT_BLOCK = line.strip().startswith( '"""'  )
						if IN_COMMENT_BLOCK   :
						
							pass
							tabbed_file.append( lang_commentmarker  + line )
						else:
							last_TAB = TABS
							TABS = len( linet ) - len( linet.lstrip('\t') )
							LINE2 = line.replace('    ', '\t').strip( "\n" )
							
							LINE = line.replace('    ', '\t.').strip( "\n" )
							
							diff = TABS - last_TAB
							if  diff < 0   :
							
								for tabs in range(  last_TAB , TABS , -1 ) :
									FillLINE = '\t.' * tabs
									FillLINE2 = '\t' * tabs
									
									tabbed_file.append( FillLINE2  )
																	
								
							
							tabbed_file.append( LINE2  )
							
					else:
						if  IN_COMMENT_BLOCK   :
						
							tabbed_file.append( lang_commentmarker  + line )
							
						if line.strip().endswith( '"""'  )  :
						
							IN_COMMENT_BLOCK = False;
							
						
						
				else:
					print( '------------------------------------------------')
					
				
			
			
	except FileNotFoundError:
		print(f"The file '{filename}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")
		
	return tabbed_file
def import_language( LANG ):
	try:
	
		lang  = importlib.import_module(f"languages.{  LANG  }_lang")
	except ImportError as e:
		sys.exit(f"Error loading lang module: {e}")
		
	return lang
def extract_rightmost_pattern(string, words, marker):
	patterns = [f"{marker} {word}" for word in words]
	matches = [pattern for pattern in patterns if pattern in string]
	return max(matches, key=string.rfind) if matches else ' generic'

def split_line_on_comment(line, comment_marker ) :
	in_literal = None
	codeline = []
	comment = []
	for i, char in enumerate(line):
		
		if char in ["'", '"', '`']:
		
			if in_literal is None:
			
				in_literal = char
			elif in_literal == char:
				in_literal = None
				
		elif char == comment_marker and in_literal is None:
			
			comment.append(line[i:])
			return ''.join(codeline), ''.join(comment)
			
		codeline.append(char)
		
		
	
	return ''.join(codeline), ''
	
def  mark2flow( marked_line ):
	codeline , comment  =  split_line_on_comment( marked_line ,  lang_commentmarker )
	VFC_DIVIDER = '//'
	keytoks = [ 'input' , 'event' , 'output' , 'set', 'process' , 'branch', 'path', 'bend' , 'loop' ,'lend' , 'end'  ]
	result = extract_rightmost_pattern( comment , keytoks , lang_commentmarker )
	result =result[1:].strip()
	flowline = f'{ result }({ codeline.strip() });{VFC_DIVIDER}  {comment.replace( result, "").replace( lang_commentmarker, "")  }'
	return flowline
if __name__ == "__main__":

	if len( sys.argv ) > 2 :
	
		CODEFILE = sys.argv[1]
		LANG = sys.argv[2]
	else:
		CODEFILE = "TEST2\python1.py"
		LANG = "python"
		
	lang = import_language( LANG  )
	lang_commentmarker = lang.lang_commentmarker

	lang.pretty_print( CODEFILE )
	tabfile = gettabbed_file( CODEFILE )
	marked_file = process_tabbed_file( tabfile ) ;
	output_file = CODEFILE + '.vfc'
	with open(output_file, "w", encoding="utf-8") as out:
	
		for line in marked_file :
			vfcline =  mark2flow( line )
			if  vfcline.startswith( 'input' )   :
			
				print( 'end();'  )
				out.write( 'end();'+ '\n' )
				
			print( vfcline  )
			out.write( vfcline + '\n' )
			if  vfcline.startswith( 'branch' )   :
			
				print( 'path();'  )
				out.write( 'path();'+ '\n' )
				
					
		exit
		
	

#  Export  Date: 05:15:45 PM - 22:Mar:2025.

