# -*- coding: utf-8 -*-
"""
Read the txt files containing the raw design tables from Chen, Sun and Wu (1993), format them and store them
in a new excel file, with one sheet per run size.
Created on Wed Jan 19 15:57:58 2022

@author: Alexandre Bohyn - alexandre dot bohyn [at] kuleuven dot be
"""
# % Packages
import re
import os
import pandas as pd


# Function to format the file

def format_file(fname: str):
    # Create dictionary for the designs
    designs_dict = pd.DataFrame()
    # Run size is in filename
    n_runs = int(re.match(r"^\d+", fname).group(0))
    with open("tables/" + fname, "r") as f:
        text_by_lines = f.readlines()
    text = "".join(text_by_lines)

    # Line is split in index of the design and rest of the informations
    col_info = [c for c in re.split(r"\d+-\d+\.\d+", text) if len(c) > 0]
    design_names = re.findall(r"\d+-\d+\.\d+", text)

    # Loop through the names
    for num, name in enumerate(design_names):
        # Base info extracted from names
        info = col_info[num]
        n, p, i = list(map(int, re.findall(r"\d+", name)))
        # All numbers from information extracted from the raw text
        nums = list(map(int, re.findall(r"\d+", info)))
        cols = nums[:p]
        # Dynamic allocation of the WLP size
        wlp = nums[p: -1]
        # Only last number is the CFI
        c = nums[-1]
        design_dict = {
            "n.runs": n_runs,
            "index": name,
            "n.cols": n,
            "n.added": p,
            "design.rank": i,
            "cols": ",".join(map(str, cols)),
            "wlp": ",".join(map(str, wlp)),
            "clear.2fi": c,
        }
        designs_dict = designs_dict.append(design_dict, ignore_index=True)
        return designs_dict


# % Activation
if __name__ == "__main__":
    # Read file
    table_fnames = os.listdir("raw_data/")
    # Create dictionary for the designs
    designs = pd.DataFrame()
    # Generate new dict and append to intial one
    for table in table_fnames:
        temp_dict = format_file(table)
        designs = designs.append(temp_dict, ignore_index=True)
    designs.to_csv('tables.csv', index=False, float_format="%.0f")
