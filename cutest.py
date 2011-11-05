import re
from SCons.Builder import Builder
from SCons.Scanner import Scanner

def generate(env,**kwargs):
	setup_environment(env)
	add_builders(env)


def exists(env):
	return 1

def setup_environment(env):
	env.AppendUnique(TEST_CASES=[])

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
	def GenerateAllTests(env, target, source, test_case = re.compile(r'^\s*void (Test[^\(\s]+)',re.M)):
		if not isinstance(target,list):
			target = [target]
		print ":: Generate tests %s < %s"%(str(target[0]),' '.join([str(s) for s in source]))
		assert(len(source)>=1)
		assert(len(target)<=1)
		if env.GetOption('clean'):
			return ''
		if(target == None):
			target[0] = 'AllTests.c'
		TEST_CASES = []
		for node in source:
			print "\tscanning %s ..."%(str(node))
			contents = node.get_text_contents()
			test_cases = test_case.findall(contents)
			TEST_CASES.extend(test_cases)
		f = open(str(target[0]),'w')
		f.write(template.substitute(
			EXTTESTS='\n'.join(["extern void %s(CuTest*);"%(case) for case in TEST_CASES]),
			ADDTESTS='\n'.join(["\tSUITE_ADD_TEST(suite, %s);"%(case) for case in TEST_CASES])))
		f.flush()
		f.close()
		return target[0]
		
	env.AddMethod(GenerateAllTests)
		
