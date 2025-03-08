def match_tok( tok , string  ):
	pattern = r'^[^\w]*' + re.escape(tok)
	match = re.match(pattern, string)
	return match is not None
def  postProcess( filename , comment_marker ):
	try:
	
		with open(filename, 'r') as file:
		
			VFCsplitter = '//' ;
			with open( f'{filename}.vfc' , 'w' ) as write_file :
			
				for line in file:
					code = line.strip()
					comment = ""
					VFCobj = 'event'
					if comment_marker in line:
					
						
						code, comment = code.split(comment_marker, 1)
						if 'input' in comment   :
						
							VFCobj = 'input' ;
						elif  match_tok( 'branch' , comment )  :
							VFCobj = 'branch' ;
						elif  match_tok(  'loop' , comment ) :
							VFCobj = 'loop' ;
						elif  match_tok( 'output' , comment )  :
							VFCobj = 'output' ;
						elif  match_tok( 'event' , comment )  :
							VFCobj = 'event' ;
						elif  match_tok( 'path' , comment )  :
							VFCobj = 'path' ;
						elif  match_tok( 'lend' , comment )  :
							VFCobj = 'lend' ;
						elif  match_tok( 'bend' , comment )  :
							VFCobj = 'bend' ;
						elif  match_tok( 'end' , comment )  :
							VFCobj = 'end' ;
						else:
							VFCobj = 'process' ;
							
						
						pattern = r'\b' + re.escape( VFCobj ) + r'\b'
						comment = re.sub(pattern, '', comment, count=1).strip()
						VFCline =  f'{VFCobj}( {code} );{VFCsplitter}   {comment.strip()} '
						
						
					else:
						if  len(comment.strip()) > 0  :
						
							VFCline =f'{ match_GENERIC_type(code.strip()) }({ code.strip() });{VFCsplitter }  {comment_marker} -----> {comment.strip()} '
						else:
							VFCline =f'{ match_GENERIC_type(code.strip()) }({ code.strip() });{VFCsplitter}'
							
						
					print( VFCline  )
					if  "def " in VFCline and VFCobj == 'input' :
					
						write_file.write( f'end();{VFCsplitter}   <-- inserted by postProcess.py'  + '\n' )
						write_file.write(VFCline + '\n')
					else:
						write_file.write(VFCline + '\n')
						
									
				
			
	except FileNotFoundError:
		print(f"The file {filename} does not exist.")
	except Exception as e:
		print(f"An error occurred: {e}")
		
		
	return
import re
def match_GENERIC_type(  search_str ):
	genericTypes = { "end" : [ "return", "end" , "continue" , "break" ] , "output" : ["alert", "throw", "console", "print", "echo" , "write" ] ,  "set" : ["=", "var const"] ,  "event": ["import", "include",  "module"]    }
	
	for key, value in genericTypes.items():
		for tok  in  value:
			pattern = r'^[^\w]*' + re.escape(tok)
			match = re.match(pattern, search_str )
			if match  :
			
				return key
				
					
			
	return 'set'

if __name__ == '__main__':

	postProcess(  'testo.js_tagged.txt'  , '//' )
	postProcess(  'testo.py_tagged.txt' , '#'  )
	postProcess(  'function.py_tagged.txt' , '#'  )
	





#  Export  Date: 10:51:15 PM - 07:Mar:2025.

