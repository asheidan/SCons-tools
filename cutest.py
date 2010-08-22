import re
from SCons.Builder import Builder
from SCons.Scanner import Scanner

def generate(env,**kwargs):
	setup_environment(env)
	add_builders(env)
	add_scanners(env)


def exists(env):
	return 1

def setup_environment(env):
	env.AppendUnique(TEST_CASES=[])

def add_scanners(env):
	test_case_re = re.compile(r'^\s*void (Test[^\(\s]+)',re.M)
	def testfile_scan(node, env, path, arg=None):
		print "scanning %s ..."%(str(node))
		contents = node.get_text_contents()
		test_cases = test_case_re.findall(contents)
		env.Append(TEST_CASES=test_cases)
		return []
	env.Append(SCANNERS=Scanner(function=testfile_scan,skeys=['.c']))

def add_builders(env):
	from string import Template
	template = Template("""
/* This is auto-generated code. Edit at your own peril. */

#include <stdio.h>
#include "CuTest.h"

$EXTTESTS

void RunAllTests(void) 
{
	CuString *output = CuStringNew();
	CuSuite* suite = CuSuiteNew();

$ADDTESTS

	CuSuiteRun(suite);
	CuSuiteSummary(suite, output);
	CuSuiteDetails(suite, output);
	printf("%s\\n", output->buffer);
}

int main(void)
{
	RunAllTests();
	return 0;
}
""")
	def generate_all_tests(source, target, env, for_signature):
		# print "generate tests %s %s"%(str(target[0]),str(source))
		assert(len(source)>=1)
		assert(len(target)<=1)
		if(target == None):
			target[0] = 'AllTests.c'
		source_files = [str(f) for f in source]
		f = open(str(target[0]),'w')
		f.write(template.substitute(
			EXTTESTS='\n'.join(["extern void %s(CuTest*);"%(case) for case in env['TEST_CASES']]),
			ADDTESTS='\n'.join(["\tSUITE_ADD_TEST(suite, %s);"%(case) for case in env['TEST_CASES']])))
		f.flush()
		f.close()
		return ''
		
	env.Append(BUILDERS={
		'GenerateAllTests': Builder(
			generator=generate_all_tests)})
		