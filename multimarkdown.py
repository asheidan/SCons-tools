from SCons.Script import Builder

def generate(env, **kwargs):
	setup_environment(env)
	setup_tools(env)
	add_builders(env)

def exists(env):
	return 1

def setup_environment(env):
	pass

def setup_tools(env):
	if not env.has_key('MMD'):
		env['MMD'] = 'multimarkdown'


def generate_builder(fmt):
	return Builder(
			action = "$MMD -o $TARGET -t %s $SOURCE" % fmt,
			suffix = '.%s' % fmt,
			src_suffix = ['.txt','.md','.markdown']
			)

def add_builders(env):
	env.Append(BUILDERS = {
		'LaTeX' : generate_builder('latex'),
		'HTML'  : generate_builder('html')
		})
