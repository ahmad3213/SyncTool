import os
import ROOT

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, type=str)
    parser.add_argument('--channel', required=True, type=str)
    parser.add_argument('--sample', required=True, type=str)
    parser.add_argument('--group', action='append', type=str)
    parser.add_argument('--file', action='append', type=str)
    parser.add_argument('--tree', action='append', type=str)
    parser.add_argument('--preSelection', action='append', type=str)
    parser.add_argument('--badThreshold', type=float, required=False, default=0.01)
    args = parser.parse_args()

    if len(args.group) != 2:
        raise RuntimeError("two groups should be provided to perform a synchronization")
    if len(args.group) != len(args.file) or len(args.group) != len(args.tree):
        raise RuntimeError("group, file, and tree should be provided consistently")
    preSelection = args.preSelection if args.preSelection else []
    if len(preSelection) > len(args.group):
        raise RuntimeError("number of pre-selection exceeds the number of groups")
    while len(preSelection) < len(args.group):
        preSelection.append("")

    ROOT.gROOT.SetBatch(True)
    ROOT.TH1.AddDirectory(False)
    ROOT.TH2.AddDirectory(False)
    ROOT.gROOT.SetMustClean(False)

    cxx_file = 'EventSync.h'
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'include')
    if ROOT.gROOT.ProcessLine(f'.include {base_path}') != 0:
        raise RuntimeError('Failed to include base path')
    if not ROOT.gInterpreter.Declare(f'#include "{cxx_file}"'):
        raise RuntimeError(f'Failed to include {cxx_file}')

    cpp_args = ROOT.Arguments()
    cpp_args.config = args.config
    cpp_args.channel = args.channel
    cpp_args.sample = args.sample
    cpp_args.badThreshold = args.badThreshold
    for i in range(len(args.group)):
        cpp_args.group.push_back(args.group[i])
        cpp_args.file.push_back(args.file[i])
        cpp_args.tree.push_back(args.tree[i])
        cpp_args.preSelection.push_back(preSelection[i])

    event_sync = ROOT.analysis.EventSync(cpp_args)
    event_sync.Run()
    del event_sync
