import argparse
import os
import re
import sys
import importlib
from typing import List, Dict, Any, Optional

import postProcess

# Constants for tag types
TAG_OPEN = "tagA"	# Opening block tag
TAG_CLOSE = "tagB"   # Closing block tag
TAG_BRIDGE = "tagX"  # Bridge/intermediate tag

class VFCTagger:
	def __init__(self, language_module):
		self.lang = language_module
		
	def process_file(self, source_file: str, skip_mapping: bool = False) -> str:
		"""Process a source file and add structure tags."""
		try:
			with open(source_file, "r", encoding="utf-8") as f:
				source = f.read()
		except Exception as e:
			raise IOError(f"Error reading source file: {e}")
			
		# Format the source code consistently for both modes
		formatted = self.lang.pretty_print(source)
		formatted = self.convert_spaces_to_tabs(formatted)
		
		# Process the source with the same tagging rules for both modes
		lines = formatted.splitlines()
		tagged_lines = self.insert_indentation_tags(lines)
		
		# Only map tags if not in skip mode
		if not skip_mapping:
			tagged_lines = self.map_language_tags(tagged_lines)
		
		return '\n'.join(tagged_lines)
	
	@staticmethod
	def convert_spaces_to_tabs(text: str, spaces_per_tab: int = 4) -> str:
		"""Convert groups of spaces to tabs and clean empty lines."""
		# First convert spaces to tabs
		text = re.sub(f"( {{{spaces_per_tab}}})", "\t", text)
		# Then remove empty lines
		return re.sub(r"(?m)^[\n]+", "", text)
	
	def insert_indentation_tags(self, lines: List[str]) -> List[str]:
		"""
		Add tags based on strict indentation rules:
		- TAG_OPEN (tagA): Added to line before +1 indent
		- TAG_CLOSE (tagB): Added to line after -1 indent
		- TAG_BRIDGE (tagX): Added when a line is both an entry and exit point
		- Enforce indentation "speed limit" of +1, 0, -1 per line
		"""
		new_lines = []
		prev_indent = 0
		
		InsideMultiLineComment = False
		
		for i, line in enumerate(lines):
			stripped = line.lstrip()
			if not stripped:  # Skip empty lines
				new_lines.append(line)
				continue
				
			indent_level = len(line) - len(stripped)
			
			# skip the multi line comments
			if stripped.startswith(self.lang.multiline_comment_start) and not InsideMultiLineComment :
				#input( f"break {i} on start : {stripped}" )
				InsideMultiLineComment = True
			else:
				if stripped.endswith(self.lang.multiline_comment_end):
					#input( f"break {i} on end : {stripped}" )
					InsideMultiLineComment = False 
				
			# Skip comment-only lines
			#if stripped.startswith(self.lang.comment_marker) or InsideMultiLineComment or stripped.startswith(self.lang.multiline_comment_end):
			if InsideMultiLineComment or stripped.startswith(self.lang.multiline_comment_end):
				new_lines.append(line.rstrip())
				continue
						
			# Get next indentation level
			next_indent = 0
			if i + 1 < len(lines):
				next_line = lines[i + 1].lstrip()
				if next_line and not next_line.startswith(self.lang.comment_marker):
					next_indent = len(lines[i + 1]) - len(next_line)
			
			# Handle multi-level indentation increases (enforce speed limit)
			if indent_level > prev_indent + 1:
				# Insert bridge lines for jumps >1 level
				for bridge_level in range(prev_indent + 1, indent_level):
					new_lines.append("\t" * bridge_level + f"{self.lang.comment_marker} {TAG_BRIDGE}")
				
			# Handle multi-level indentation decreases
			if prev_indent > indent_level + 1:
				# Process decrease in steps
				for step in range(prev_indent - 1, indent_level, -1):
					new_lines.append("\t" * step + f"{self.lang.comment_marker} {TAG_CLOSE}")
			
			# Insert blank line when going from level 1 to 0 if next line would indent
			if prev_indent == 1 and indent_level == 0 and next_indent > 0:
				new_lines.append(f"{self.lang.comment_marker} {TAG_CLOSE}")
			
			# Apply tags based on precise indentation patterns
			if indent_level < prev_indent and indent_level < next_indent:
				# Line is both an exit and entry point - use TAG_BRIDGE (tagX)
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_BRIDGE} |+++++++++++++ BRIDGE ")
			elif indent_level < next_indent:
				# Line before +1 indent gets TAG_OPEN (tagA)
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_OPEN} |+++++++++++++ OPEN ")
			elif indent_level < prev_indent:
				# Line after -1 indent gets TAG_CLOSE (tagB)
				new_lines.append(line.rstrip() + f" {self.lang.comment_marker} {TAG_CLOSE} |+++++++++++++ CLOSE ")
			else:
				# No indentation change
				new_lines.append(line.rstrip())
			
			prev_indent = indent_level
			
		return new_lines
	
	def map_language_tags(self, lines: List[str]) -> List[str]:
		"""Map generic tags to language-specific tags using the language module."""
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
					indent_level = len(line)- len(line.lstrip('\t'))
					tab = '\t';
									
					if tag == TAG_CLOSE and self.lang.comment_marker == "#" :  #<-------------------------lang dependent fix !!!!
						new_lines.append(f"{ tab *indent_level }{self.lang.comment_marker} {refined}")
						new_lines.append(f"{ tab *indent_level }{cleaned}")
					else:
						new_lines.append(new_line)
						
					mapped = True
					break
			
			if not mapped:
				new_lines.append(line)
				
		return new_lines


def main():
	parser = argparse.ArgumentParser(description="Indentation Validator and Marker")
	parser.add_argument("language", help="Language (e.g., javascript, python, perl)")
	parser.add_argument("file", help="Source file to process")
	parser.add_argument("--skip", action="store_true", help="Skip language processing and only perform indentation tagging")
	parser.add_argument("--output", help="Output file (default: {input}_indented.txt)")
	args = parser.parse_args()

	# Import language module
	try:
		lang_module = importlib.import_module(f"languages.{args.language.lower()}_lang")
	except ImportError as e:
		sys.exit(f"Error loading language module: {e}")
	
	# Process the file
	try:
		tagger = VFCTagger(lang_module)
		result = tagger.process_file(args.file, args.skip)
		
		# Determine output file
		output_file = args.output if args.output else os.path.basename(args.file) + "_indented.txt"
		
		# Write the output
		with open(output_file, "w", encoding="utf-8") as out:
			out.write(result)
			
		print(f"Output written to: {output_file}")
	except Exception as e:
		sys.exit(f"Error: {e}")


if __name__ == "__main__":
	main()