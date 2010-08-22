
from SCons.Script import Builder

def generate(env, **kwargs):
	setup_environment(env)
	setup_tools(env)
	add_flags(env)
	add_commands(env)

def exists(env):
	return 1

def setup_environment(env):
	if env.has_key('AVRPATH'):
		env.AppendENVPath('PATH',env['AVRPATH'])

def setup_tools(env):
	if None != env.WhereIs('avrdude'):
		env['AVRDUDE'] = 'avrdude'
	else:
		print "ERROR: avrdude not found on path"

def add_flags(env):
	env['DUDEFLAGS'] = env['PROGRAMMER'] + ' -p $MCU'

def add_commands(env):
	def read_fuse(env,source=None):
		env.Command('read_fuses',None,'$AVRDUDE $DUDEFLAGS -qq -U lfuse:r:/dev/stdout:h -U efuse:r:/dev/stdout:h -U hfuse:r:/dev/stdout:h')
	
	def flash(env,source):
		assert(len(source)==1)
		env.Command('flash',source,'$AVRDUDE $DUDEFLAGS -qq -U flash:w:$SOURCE:i')
	
	def erase_device(env,source=None):
		env.Command('erase',None,'$AVRDUDE $DUDEFLAGS -e')
	
	env.AddMethod(read_fuse, "ReadFuses")
	env.AddMethod(flash, "Flash")
	env.AddMethod(erase_device, "Erase")