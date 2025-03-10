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
					if tag == TAG_CLOSE and self.lang.comment_marker == "#" :
					
						new_lines.append(f"{ tab *indent_level }{self.lang.comment_marker} {refined}")
						new_lines.append(f"{ tab *indent_level }{cleaned}")
					else:
						new_lines.append(new_line)
						
					mapped = True
					break
					
				
				
				
			
			if not mapped:
			
				new_lines.append(line)
				
			
		
		return new_lines
		
		
	
		
	def insert_indentation_tags(self, lines: List[str]) -> List[str]:
		
		
		
		
		
		
		
		new_lines = []
		prev_indent = 0
		InsideMultiLineComment = False
		for i, line in enumerate(lines):
			stripped = line.lstrip()
			if not stripped:
			
				new_lines.append(line)
				continue
				
			indent_level = len(line) - len(stripped)
			
			if stripped.startswith(self.lang.multiline_comment_start) and not InsideMultiLineComment:
			
				
				InsideMultiLineComment = True
			else:
				if stripped.endswith(self.lang.multiline_comment_end):
				
					
					InsideMultiLineComment = False
					
				
			
			
			
			
			if InsideMultiLineComment or stripped.startswith(self.lang.multiline_comment_end):
			
				new_lines.append(line.rstrip())
				continue
				
			
			next_indent = 0
			if i + 1 < len(lines):
			
				next_line = lines[i + 1].lstrip()
				if next_line and not next_line.startswith(self.lang.comment_marker):
				
					next_indent = len(lines[i + 1]) - len(next_line)
					
				
				
			
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
		
	
def main():
	parser = argparse.ArgumentParser(description="Indentation Validator and Marker")
	parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
	parser.add_argument("file", help="Source file to process")
	parser.add_argument("--skip", action="store_true", help="Skip language processing and only perform indentation tagging")
	parser.add_argument("--output", help="Output file (default: {input}_indented.txt)")
	args = parser.parse_args()
	try:
	
		lang_module = importlib.import_module(f"languages.{args.language.lower()}_lang")
	except ImportError as e:
		sys.exit(f"Error loading language module: {e}")
		
	try:
	
		tagger = VFCTagger(lang_module)
		result = tagger.process_file(args.file, args.skip)
		output_file = args.output if args.output else os.path.basename(args.file) + ".tag"
		with open(output_file, "w", encoding="utf-8") as out:
		
			out.write(result)
			
		print(f"Output written to: {output_file}")
	except Exception as e:
		sys.exit(f"Error: {e}")
		
	
	
if __name__ == "__main__":

	main()
	

#  Export  Date: 12:49:28 AM - 10:Mar:2025.

