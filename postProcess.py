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
						elif  'branch' in comment  :
							VFCobj = 'branch' ;
						elif   'loop' in comment :
							VFCobj = 'loop' ;
						elif  'output' in comment  :
							VFCobj = 'output' ;
						elif  'path' in comment  :
							VFCobj = 'path' ;
						elif  'lend' in comment  :
							VFCobj = 'lend' ;
						elif 'bend' in comment  :
							VFCobj = 'bend' ;
						elif  'end' in comment  :
							VFCobj = 'end' ;
						else:
							VFCobj = 'process' ;
							
						VFCline =  f'{VFCobj}( {code} );{VFCsplitter}   {comment.strip()} '
						
						
					else:
						VFCline =f'{ match_GENERIC_type(code.strip()) }({ code.strip() });  {VFCsplitter }   ----->>>> {comment.strip()} '
						
					print( VFCline  )
					write_file.write(VFCline + '\n')  # generic:168:
									
				
			
	except FileNotFoundError:
		print(f"The file {filename} does not exist.")
	except Exception as e:
		print(f"An error occurred: {e}")
		
		
	return
def match_GENERIC_type(  search_str ):
	genericTypes = { "end" : "return end continue;" , "output" : "alert throw console print echo" ,  "set" : "= var const" }
	
	for key, value in genericTypes.items():
		value_words = set(value.split())
		for tok  in  value_words:
			if tok in  search_str :
			
				return key
				
					
			
	return 'set'

if __name__ == '__main__':

	postProcess(  'testo.js_indented.txt'  , '//' )
	postProcess(  'testo.py_indented.txt' , '#'  )
	





#  Export  Date: 01:30:20 PM - 04:Mar:2025.

