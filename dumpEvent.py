import ROOT
import numpy


def toString(value, type):
    if type.startswith("ROOT::VecOps::RVec"):
        values = []
        for n in range(value.size()):
            values.append(str(value[n]))
        return '[' + ', '.join(values) + ']'
    return value

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputFile', required=True, type=str)
    parser.add_argument('--evtId', type=str, required=True)
    parser.add_argument('--treeName', type=str, default='Events')
    parser.add_argument('--id_branches', type=str, default='run:luminosityBlock:event')
    args = parser.parse_args()

    evt_id = args.evtId.split(":")
    id_branches = args.id_branches.split(":")
    df = ROOT.RDataFrame(args.treeName, args.inputFile)
    for evt_idx in range(len(evt_id)):
        df = df.Filter(f"{id_branches[evt_idx]}=={evt_id[evt_idx]}")
    all_columns = sorted([ str(c) for c in df.GetColumnNames() ])
    column_types = { c : str(df.GetColumnType(c)) for c in all_columns }
    known_types = {'UInt_t', 'Double_t', 'ULong64_t', 'Bool_t', 'Float_t', 'ROOT::VecOps::RVec<Float_t>', 'Int_t', 'ROOT::VecOps::RVec<Bool_t>', 'ROOT::VecOps::RVec<Int_t>'}
    #column_types = {str(df.GetColumnType(c)) for c in all_columns}
    #print(column_types)
    col_to_print = [ c for c in all_columns if column_types[c] in known_types ]

    df_np = df.AsNumpy(col_to_print)
    for col in col_to_print:
        col_value = toString(df_np[col][0], column_types[col])
        print(f"{col} = {col_value}")
