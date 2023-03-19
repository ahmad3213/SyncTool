import os
import sys
import ROOT

cxx_file = 'ShapeSync.h'
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'include')
if ROOT.gROOT.ProcessLine(f'.include {base_path}') != 0:
    raise RuntimeError('Failed to include base path')
if not ROOT.gInterpreter.Declare(f'#include "{cxx_file}"'):
    raise RuntimeError(f'Failed to include {cxx_file}')

arg_str = 'static std::string _ARGV[] = {'
for arg in sys.argv[1:]:
    arg_str += f'"{arg}",'
arg_str += '}; static char* ARGV[] = {';
for n in range(len(sys.argv[1:])):
    arg_str += f'_ARGV[{n}].data(),'
arg_str += f'}}; static const int ARGC = {len(sys.argv[1:])};'
if not ROOT.gInterpreter.Declare(arg_str):
    raise RuntimeError('Failed to declare arguments')

ROOT.gROOT.ProcessLine('main(ARGC, ARGV);')