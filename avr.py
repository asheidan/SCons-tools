from os import environ
from SCons.Builder import Builder

# Why can't I have env.Program? =(

def generate(env, **kwargs):
	setup_environment(env)
	setup_tools(env)
	add_flags(env)
	add_builders(env)

def exists(env):
	return 1

def setup_environment(env):
	if env.has_key('AVRPATH'):
		env.AppendENVPath('PATH',env['AVRPATH'])

def setup_tools(env):
	assert env.has_key('MCU'), "You need to specify processor (MCU=<cpu>)"
	
	if not env.has_key('PREFIX'):
		env['PREFIX'] = 'avr-'
	
	if not env.has_key('HEXFORMAT'):
		env['HEXFORMAT'] = 'ihex'
	
	gnu_tools = ['gcc','g++','ar',]
	for tool in gnu_tools:
		env.Tool(tool)
	
	env.Replace(CC=env['PREFIX']+'gcc')
	env.Replace(CXX=env['PREFIX']+'g++')
	env.Replace(AR=env['PREFIX']+'ar')
	env.Replace(RANLIB=env['PREFIX']+'ranlib')
	env.Replace(OBJCOPY=env['PREFIX']+'objcopy')
	env.Replace(OBJDUMP=env['PREFIX']+'objdump')
	env.Replace(SIZE=env['PREFIX']+'size')
	
	if None == env.WhereIs(env['CC']):
		print '%s not found on PATH'%(env['CC'])
	
	env['PROGSUFFIX'] = '.elf'

def add_flags(env):
	assert(env['MCU'])
	env.Append(CFLAGS='-mmcu='+env['MCU'])
	env.Append(LINKFLAGS='-mmcu='+env['MCU'])

def add_builders(env):
	def generate_elf(source, target, env, for_signature):
		sources = ' '.join([str(s) for s in source])
		result = '$CC $CFLAGS'
		result += ' -o %s %s'%(target[0],sources)
		if(env.has_key('LIBPATH')):
			result += include_string('-L',env['LIBPATH'])
		if(env.has_key('LIBS')):
			result += include_string('-l',env['LIBS'])
		return result
	
	def display_disasm(source, target, env, for_signature):
		assert(len(source)==1)
		return '$OBJDUMP -d %s'%(source[0])
	
	def display_sizes(source, target, env, for_signature):
		assert(len(source)>=1)
		result = '$SIZE'
		if env.has_key('TOTALS') and env['TOTALS']:
			result += ' --totals'
		result += include_string(elements=source)
		return result
	
	def generate_hex(source, target, env, for_signature):
		assert(len(source)==1)
		assert(len(target)==1)
		result = '$OBJCOPY -O $HEXFORMAT -j .text -j .data -j .bss'
		result += ' %s %s'%(source[0],target[0])
		return result
	
	def generate_eep(source, target, env, for_signature):
		assert(len(source)==1)
		assert(len(target)==1)
		result = '$OBJCOPY -O $HEXFORMAT -j .eeprom'
		# result += ' --set-section-flags=.eeprom="alloc,load"'
		# result += ' --change-section-lma .eeprom=0'
		result += ' %s %s'%(source[0],target[0])
		return result
	
	env.Append(BUILDERS={
		# 'Program': Builder(
		#	 generator=generate_elf,
		#	 suffix=env['PROGSUFFIX'],
		#	 src_suffix='.o'),
		'DisplayASM': Builder(
			generator=display_disasm,
			src_suffix=env['PROGSUFFIX']),
		'DisplaySizes': Builder(generator=display_sizes),
		'HexFile': Builder(
			generator=generate_hex,
			suffix='.hex',
			src_suffix='.elf'),
		'EepFile': Builder(
			generator=generate_eep,
			suffix='.eep',
			src_suffix='.elf')})
	


def include_string(prefix='',elements=[]):
	"""Creates a list for inclusion on the commandline"""
	if len(elements)>0:
		return ' '+' '.join(['%s%s'%(prefix,element) for element in elements])
	else:
		return ''
