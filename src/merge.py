import pandas as pd

def merge_csvs(input_paths, output_path):
    dfs = [pd.read_csv(p) for p in input_paths]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(output_path, index=False)

paths = input("Enter CSV names (comma separated): ").split(",")
paths = [f"data/{p.strip()}.csv" for p in paths]

out = input("Enter output file name: ").strip()
out = f"data/{out}.csv"

merge_csvs(paths, out) 