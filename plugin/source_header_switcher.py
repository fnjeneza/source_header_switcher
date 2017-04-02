#!/usr/bin/env python3

import vim
import os

headers_extension = [".hxx", ".h", ".hh", ".hpp"]
sources_extension = [".cxx", ".c", ".cc", ".cpp"]

include_directories = []
source_directories = []

alternate_source_directories = [
	"../src", 
	"../source", 
	"../sources",
]

alternate_include_directories = [
	"../inc",
	"../include",
	"../includes",
]


def file_info(file_path):

	# current directory
	directory = os.path.dirname(file_path)

	# filename
	filename = os.path.basename(file_path)
	#suffix_filename = filename.split('.')[0]
	_, extension = os.path.splitext(filename)
	return (directory, filename, extension)

def all_include_directories(include_dirs, alternate_include_dir, current_dir):
	for alt_dir in alternate_include_dir:
		include_dirs.append(os.path.join(current_dir, alt_dir))
	# add current directory
	include_dirs.append(current_dir)
	return include_dirs
	
def all_source_directories(source_dirs, alternate_source_dir, current_dir):
	for alt_dir in alternate_source_dir:
		source_dirs.append(os.path.join(current_dir, alt_dir))
	# add current directory
	source_dirs.append(current_dir)
	return source_dirs

def is_header(extension, headers_ext):
	ext = extension.lower()
	return ext in headers_ext

def is_source(extension, headers_ext):
	ext = extension.lower()
	return ext in headers_ext

def source_files(source_directories, filename, sources_ext):
	files_found = []
	_suffix = filename.split('.')[0]
	for source_dir in source_directories:
		for ext in sources_ext:
			_filename  = _suffix + ext
			_filename = os.path.join(source_dir, _filename)
			if os.path.exists(_filename):
				files_found.append(_filename)
	return files_found

def header_files(include_directories, filename, headers_ext):
	files_found = []
	_suffix = filename.split('.')[0]
	for header_dir in include_directories:
		for ext in headers_ext:
			_filename = _suffix + ext
			_filename = os.path.join(header_dir, _filename)
			if os.path.exists(_filename):
				files_found.append(_filename)
	return files_found

if __name__ == '__main__':
	# get full file path
	file_path = vim.eval("expand('%:p')")
	directory, filename, extension = file_info(file_path)
	
	source_directories = all_source_directories(source_directories, 
				alternate_source_directories,
				directory
				)
	include_directories = all_include_directories(include_directories, 
				alternate_include_directories,
				directory
				)

	# multiple files can be found
	files_found = []

	if is_header(extension, headers_extension):
		files_found = source_files(source_directories, filename, sources_extension)
	
	if is_source(extension, sources_extension):
		files_found = header_files(include_directories, filename, headers_extension)

	# open the file
	vim.command(":edit %s" %files_found[0])
