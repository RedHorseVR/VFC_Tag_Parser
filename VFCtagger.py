import argparse
import os
import re
import sys
import importlib

lang = None

def  process_tabbed_file( tabfile ):
	TABS =0
	last_TAB = 0
	marked_file = []
	marked_line =  f'{ lang.commentmarker } set '
	
	marked_file.append( marked_line );
	marked_file.append( marked_line );
	i = 0
	for i in range ( 0 , len(tabfile) - 1 )  :
		line = tabfile[ i ]
		
		if  not  line.strip().startswith( lang.commentmarker )  :
		
			line = lang.lang_filter( line , marked_file )
			last_TAB = TABS
			TABS = len( line ) - len( line.lstrip('\t') )
			nextline = lang.lang_check_path( tabfile[i+1] )
			next_TABS = len( nextline  ) - len( nextline.lstrip('\t') )
			tabrate = last_TAB-TABS
			next_tabrate = TABS - next_TABS
			if   next_tabrate == 1  :
			
				popObj = lang.pop().split('+')
				
				marked_line =  f'\t' * (TABS) + f'{line} { lang.commentmarker } { popObj[0] } '
				marked_file.append( marked_line );
				if  len(popObj) >1:
				
					marked_line =  f'\t' * (TABS) + f'#class end { lang.commentmarker } { popObj[1] } '
					marked_file.append( marked_line );
					
					
				
			else:
				marked_line =  f'{line}'
				marked_file.append( marked_line );
				
			
			for rate in range( 2, next_tabrate ):
				marked_line =  f'\t' * (TABS) + f'{ lang.commentmarker } { lang.pop() } '
				marked_file.append( marked_line );
							
		else:
			newline = line.replace( "\t" , "" )
			marked_line =  f'{ newline  } {lang.commentmarker} set --'
			marked_file.append( marked_line );
			
			
			
	line = tabfile[ i+1 ]
	line = lang.lang_filter( line  , marked_file  )
	marked_file.append( line );
	TYPE = lang.pop()
	while len(TYPE) > 0  :
		marked_file.append(  f'{lang.commentmarker } {TYPE}'  );
		TYPE = lang.pop()
			
	
	marked_file.append( f'{lang.commentmarker } end' );
	
	
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
				
					if  not IN_COMMENT_BLOCK and not line.startswith('\n')  and not line.lstrip().startswith(  lang.commentmarker ) :
					
						i +=1
						IN_COMMENT_BLOCK = line.strip().startswith( lang.multiline_comment_start )
						if IN_COMMENT_BLOCK   :
						
							tabbed_file.append( lang.commentmarker  + line )
						else:
							last_TAB = TABS
							TABS = len( linet ) - len( linet.lstrip('\t') )
							LINE2 = line.replace('    ', '\t').strip( "\n" )
							
							LINE = line.replace('    ', '\t.').strip( "\n" )
							
							diff = TABS - last_TAB
							if  diff < 0    :
							
								for tabs in range(  last_TAB , TABS , -1 ) :
									
									FillLINE2 = '\t' * tabs
									
									tabbed_file.append( FillLINE2  )
																	
								
							
							tabbed_file.append( LINE2  )
							
					else:
						if  IN_COMMENT_BLOCK   :
						
							tabbed_file.append( lang.commentmarker  + line.strip('\n') )
							
						if line.strip().endswith( lang.multiline_comment_end )  :
						
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

def split_line_on_comment(line, comment_marker , literals ) :
	in_literal = None
	codeline = []
	comment = []
	for i, char in enumerate(line):
		
		if char in literals:
		
			if in_literal is None:
			
				in_literal = char
			elif in_literal == char:
				in_literal = None
				
		elif char == comment_marker[0] and line[i:i+len(comment_marker)] == comment_marker and in_literal is None:
			comment.append(line[i:])
			return ''.join(codeline).rstrip(), ''.join(comment).strip()
			
		codeline.append(char)
		
	
	return ''.join(codeline).rstrip(), ''
def  mark2flow( marked_line ):
	codeline , comment  =  split_line_on_comment( marked_line ,  lang.commentmarker , lang.literals )
	VFC_DIVIDER = '//'
	keytoks = [ 'input' , 'event' , 'output' , 'set', 'process' , 'branch', 'path', 'bend' , 'loop' ,'lend' , 'end'  ]
	result = extract_rightmost_pattern( comment , keytoks , lang.commentmarker )
	result =result.lstrip( lang.commentmarker )
	flowline = f'{ result }({ codeline.strip() });{VFC_DIVIDER}  {comment }'
	return flowline
def  writeout( filename, list ) :
	with open( filename , "w", encoding="utf-8") as out:
	
		for line  in  list :
			out.write( line + '\n'  )
					
		
	
## MAIN
print( '------------------------------------------------')
PRINTFLOW = False
CODEFILE = "TEST2\MonGPU.py"
LANG = "python"
if __name__ == "__main__":

	if len( sys.argv ) > 1 :
	
		if len( sys.argv ) > 2 :
		
			CODEFILE = sys.argv[2]
			LANG = sys.argv[1]
		else:
			CODEFILE = sys.argv[1]
			name, extension = os.path.splitext( CODEFILE )
			if extension.lower() == '.py'  :
			
				LANG = 'python'
			elif  extension.lower() == '.js' :
				LANG = 'javascript'
				
			
		lang = import_language( LANG  )
		lang.commentmarker = lang.commentmarker
	else:
		pass
		print( "NO ARGUMENTS GIVEN.  CODEFILE IN .py or .js EXPECTED."  )
		print( '------------------------------------------------')
		exit()
		

	DEBUG = False;
	lang.pretty_print( CODEFILE )
	tabfile = gettabbed_file( CODEFILE )
	if(DEBUG) : writeout( 'tabs.txt' ,  tabfile )
	markfile = process_tabbed_file( tabfile ) ;
	if(DEBUG) : writeout( 'marks.txt' ,  markfile )
	for line  in  markfile :
		print( line )
			
	output_file = CODEFILE + '.vfc'
	with open(output_file, "w", encoding="utf-8") as out:
	
		for line in markfile :
			vfcline =  mark2flow( line )
			if  vfcline.startswith( 'input' )   :
			
				if PRINTFLOW : print( 'end();'  )
				out.write( 'end();'+ '\n' )
				
			if PRINTFLOW :print( vfcline  )
			out.write( vfcline + '\n' )
					
		out.write( lang.footer( os.path.basename(CODEFILE)  ) )
		out.close()
		
	
	print( 'Opening ...' , output_file  )
	
	os.system( f"start VFC2000 { output_file} -Reload" )
	

#  Export  Date: 03:17:56 PM - 12:Apr:2025.

