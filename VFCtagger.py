import argparse
import os
import re
import sys
import importlib
from typing import List, Dict, Any, Optional


TAG_OPEN = "tagA"
TAG_CLOSE = "tagB"
TAG_BRIDGE = "tagX"


class VFCTagger:
	
	
	def __init__(self, language_module):
		self.lang = language_module
		
	def convert_spaces_to_tabs(self, text: str, spaces_per_tab: int = 4) -> str:
		text = re.sub(f"( {{{spaces_per_tab}}})", "\t", text)
		
		return re.sub(r"(?m)^[\n]+", "", text)
	def process_file(self, source_file: str, skip_mapping: bool = False) -> str:
		
		try:
		
			with open(source_file, "r", encoding="utf-8") as f:
			
				source = f.read()
				
			
		except Exception as e:
			raise IOError(f"Error reading source file: {e}")
			
		
		formatted = self.lang.pretty_print(source)
		formatted = self.convert_spaces_to_tabs(formatted)
		
		lines = formatted.splitlines()
		tagged_lines = self.insert_indentation_tags(lines)
		
		if not skip_mapping:
		
			tagged_lines = self.map_language_tags(tagged_lines)
			
		return "\n".join(tagged_lines)
		
	def map_language_tags(self, lines: List[str]) -> List[str]:
		new_lines = []
		tags = [TAG_OPEN, TAG_CLOSE, TAG_BRIDGE]
		for i, line in enumerate(lines):
			mapped = False
			for tag in tags:
				tag_marker = f"{self.lang.comment_marker} {tag}"
				if tag_marker in line:
				
					cleaned = line.replace(tag_marker, "").strip()
					refined = self.lang.tagMapper(cleaned, tag, i + 1)
					new_line = line.replace(tag_marker, f"{self.lang.comment_marker} {refined}")
					indent_level = len(line) - len(line.lstrip("\t"))
					tab = "\t"
					if tag == TAG_CLOSE and self.lang.language == "python" :
					
						new_lines.append(f"{ tab *indent_level }{self.lang.comment_marker} {refined}")
						new_lines.append(f"{ tab *indent_level }{cleaned}")
					else:
						new_lines.append(new_line)
						
					mapped = True
					break
					
				
				
				
			
			if not mapped:
			
				new_lines.append(line)
				
			
		
		return new_lines
		
		
	
	def count_tabs(self, line):
		#try-catch-exception
		try:
			match = re.match(r'^(\t*)', line)
			return len(match.group(1))
		except :
			return 0
			
		
	def insert_indentation_tags(self, lines: List[str]) -> List[str]:
		
		
		
		
		
		
		
		new_lines = []
		prev_indent = 0
		InsideMultiLineComment = False
		for i, line in enumerate(lines):
			stripped = line.lstrip()
			if not stripped:
			
				new_lines.append(line)
				continue
				
			indent_level = self.count_tabs(line)
			
			if stripped.startswith(self.lang.multiline_comment_start) and not InsideMultiLineComment:
			
				
				InsideMultiLineComment = True
			else:
				if stripped.endswith(self.lang.multiline_comment_end):
				
					
					InsideMultiLineComment = False
					
				
			
			
			
			
			if InsideMultiLineComment or stripped.startswith(self.lang.multiline_comment_end):
			
				new_lines.append(line.rstrip())
				continue
				
			
			print( i , len(lines) )
			next_indent = 0
			indent_level = thisLevel = self.count_tabs( line )
			prev_indent = prevLevel = 0  if i == 0 else self.count_tabs( lines[ i-1] )
			next_indent = nextLevel = 0 if i >= len(lines)-1 else  self.count_tabs( lines[ i+1] )
			
			
			if indent_level > prev_indent + 1:
			
				
				for bridge_level in range(prev_indent + 1, indent_level):
					new_lines.append("\t" * bridge_level + f"{self.lang.comment_marker} {TAG_BRIDGE}")
					
				
				
			
			
			if prev_indent > indent_level + 1:
			
				
				for step in range(prev_indent - 1, indent_level, -1):
					new_lines.append("\t" * step + f"{self.lang.comment_marker} {TAG_CLOSE}")
					
				
				
			
			
			if prev_indent == 1 and indent_level == 0 and next_indent > 0:
			
				new_lines.append(f"{self.lang.comment_marker} {TAG_CLOSE}")
				
			
			if indent_level < prev_indent and indent_level < next_indent:
			
				
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_BRIDGE} ")
				
			elif indent_level < next_indent:
				
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_OPEN} ")
				
			elif indent_level < prev_indent:
				
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_CLOSE} ")
				
			else:
				
				new_lines.append(line.rstrip())
				
				
			prev_indent = indent_level
			
					
		return new_lines
		
	
def get_main_args():
	parser = argparse.ArgumentParser(description="Indentation Validator and Marker")
	parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
	parser.add_argument("file", help="Source file to process")
	parser.add_argument("--skip", action="store_true", help="Skip language processing and only perform indentation tagging")
	parser.add_argument("--output", help="Output file (default: {input}_indented.txt)")
	args = parser.parse_args()
	return args
def print_file(filename):
	filename = filename.strip()
	print( '------------------------------------------------')
	print( filename )
	try:
	
		LINE = ' '
		TABS =0
		with open(filename, 'r') as file:
		
			IN_COMMENT_BLOCK = False;
			for line in file:
				if  not IN_COMMENT_BLOCK   :
				
					IN_COMMENT_BLOCK = line.startswith(('"""', "'''"))
					if IN_COMMENT_BLOCK   :
					
						print( f' ... { '#' }  { LINE  }' )
					else:
						linet = line.replace('    ', '\t').strip( "\n" )
						TABS = len( linet ) - len( linet.lstrip('\t') )
						LINE = line.replace('    ', '\t.').strip( "\n" )
						print( f' ... { TABS }  { LINE  }' )
						
				else:
					if line.endswith(('"""', "'''"))  :
					
						IN_COMMENT_BLOCK = False;
						print( f' ... { '#' }  { LINE  }' )
					else:
						linet = line.replace('    ', '\t').strip( "\n" )
						TABS = len( linet ) - len( linet.lstrip('\t') )
						LINE = line.replace('    ', '\t.').strip( "\n" )
						print( f' ... { TABS }  { LINE  }' )
						
					
				
			
			
	except FileNotFoundError:
		print(f"The file '{filename}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")
		
	
def import_language( LANGUAGE ):
	try:
	
		FORMATTER  = importlib.import_module(f"languages.{  LANGUAGE  }_lang")
	except ImportError as e:
		sys.exit(f"Error loading FORMATTER module: {e}")
		
	return FORMATTER
def main():
	
	LANGUAGE = "python"
	FORMATTER = import_language( LANGUAGE  )
	CODEFILE = "TEST2\python1.py"
	print( CODEFILE )
	
	print_file( CODEFILE )
	
	print( '----------DONE----------')
	exit
''' --------------------------------------------
tagger = VFCTagger( FORMATTER )
result = tagger.process_file(args.file, args.skip)
output_file = args.output if args.output else os.path.basename(args.file) + ".tag"
with open(output_file, "w", encoding="utf-8") as out:

	out.write(result)
	
print(f"Output written to: {output_file}")
-------------------------------------------- '''

if __name__ == "__main__":

	main()
	

#  Export  Date: 09:03:20 PM - 20:Mar:2025.

