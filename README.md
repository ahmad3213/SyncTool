# SyncTool
Tools to sync between two analysis frameworks

## Installation

```sh
git clone https://github.com/cms-hh-bbtautau/SyncTool.git
```

## Environment

Should work in a python environment with ROOT. For example, on lxplus, one can use the LCG environment:
```sh
# lxplus 7
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_102 x86_64-centos7-gcc11-opt
# lxplus 8
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_102 x86_64-centos8-gcc11-opt
```

## EventSync

Synchronise on an event-by-event basis. Output contains:
- number of events and unique events for each group
- list of duplicated events (if any) for each group
- number of common events
- comparison between variables defined in the config:
  - common events with discrepancies above the threshold are listed in the log
  - plots in PDF format:
    - 1D plot with a comparison of distributions for all events
    - 1D plot with a comparison of distributions for the common events
    - 1D plot with a comparison of distributions for the different events
    - 2D distribution for the common events: x=var_group2, y=(var_group2-var_group1)/var_group2

How to run
```sh
python EventSync.py --config MY_CONFIG --channel MY_CHANNEL --sample MY_SAMPLE --group GROUP1 --file FILE1.root --tree TREE1 --group GROUP2 --file FILE2.root --tree TREE2 &> sync.log
```

Example:
```sh
python EventSync.py --config config/PI_LLR.cfg --channel tauTau --sample TT --group PI --file TT_PI.root --tree Events --group LLR --file TT_LLR.root --tree HTauTauTree &> sync.log
```

## ShapeSync

Synchronise on output shapes used for the limit extraction.

How to run
```sh
python ShapeSync.py --config MY_CONFIG --input INPUT1.root --input INPUT2.root --output OUTPUT.pdf &> shape_sync.log
```

Example:
```sh
python ShapeSync.py --config config/PI_LLR_shape.cfg --input PI_shapes.root --input LLR_shapes.root --output shape_sync.pdf &> shape_sync.log
```