# SCons tools

A few helpers for different tasks which I do quite often when using SCons as
a build-system.

## Usage

Put the file containing the helpers you want to use somewhere in your path or
provide path as well as toolname.

	env = Environment(
		# Supply the names of the tools you want to use ( you might want to add
		# 'default' to the list as well ).
		tools = ['cutest'],
		# This is where you might need to supply a path to where your
		# helper-files
		toolpath = ['sconslib']
	)

And you are good to go.

Your milage may wary...

## Documentation

Look in the files for the different functionality implemented. Better
documentation might appear here, but don't count on it.
