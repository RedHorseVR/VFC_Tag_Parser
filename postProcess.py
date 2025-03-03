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
						VFCline =f'set({code.strip()});{VFCsplitter }>>>> {comment.strip()} '
						
					print( VFCline  )
					write_file.write(VFCline + '\n')  # generic:168:
									
				
			
	except FileNotFoundError:
		print(f"The file {filename} does not exist.")
	except Exception as e:
		print(f"An error occurred: {e}")
		
		
	return
if __name__ == '__main__':

	
#  Export  Date: 02:46:57 PM - 02:Mar:2025.

