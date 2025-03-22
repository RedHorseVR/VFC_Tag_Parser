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
		
	

#  Export  Date: 01:55:59 PM - 22:Mar:2025.

