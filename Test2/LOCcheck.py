

import os
import argparse
def count_lines_in_file(file_path):
	try:
	
		with open(file_path, 'r', encoding='utf-8') as file:
		
			return sum(1 for _ in file)
			
		
	except UnicodeDecodeError:
		try:
		
			with open(file_path, 'r', encoding='latin-1') as file:
			
				return sum(1 for _ in file)
				
			
		except Exception as e:
			print(f"Error reading {file_path}: {e}")
			return 0
			
		
	except Exception as e:
		print(f"Error reading {file_path}: {e}")
		return 0
		
	
def scan_directory(directory_path):
	
	
	
	total_lines = 0
	file_count = 0
	file_details = []
	for root, _, files in os.walk(directory_path):
		for file in files:
			if file.endswith(('.vfc', '.ins')):
			
				file_path = os.path.join(root, file)
				line_count = count_lines_in_file(file_path)
				total_lines += line_count
				file_count += 1
				file_details.append({'path': file_path, 'lines': line_count})
				
			
		
		
	
	return total_lines, file_count, file_details

def main():
	parser = argparse.ArgumentParser(description='Count lines in .vfc and .ins files.')
	parser.add_argument('directory', help='Directory to scan recursively')
	args = parser.parse_args()
	if not os.path.isdir(args.directory):
	
		print(f"Error: {args.directory} is not a valid directory")
		return
		
	print(f"Scanning {args.directory} for .vfc and .ins files...")
	total_lines, file_count, file_details = scan_directory(args.directory)
	file_details.sort(key=lambda x: x['lines'], reverse=True)
	print("\nFile Details:")
	for file_info in file_details:
		print(f"{file_info['lines']:8,d} lines - {file_info['path']}")
		
	
	print("\nSummary:")
	print(f"Total files found: {file_count}")
	print(f"Total lines: {total_lines:,}")
	
if __name__ == "__main__":

	main()
	

#  Export  Date: 06:55:23 PM - 25:Mar:2025.

