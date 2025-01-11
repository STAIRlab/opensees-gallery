# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:31:32 2023

@author: Allen
"""
# import vfo.vfo as vfo
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
from pathlib import Path
from tqdm import tqdm
import math

nodes_df = pd.read_csv("ModifiedElemNodes.csv")

nodes_file = Path('', 'nodes.xlsx')
wb_obj = openpyxl.load_workbook(nodes_file, data_only=True)
ws = wb_obj['nodes_output']
data = ws.values
data = list(data)[1:]
original_nodes_df = pd.DataFrame(data, columns=["node_num", "x", "y", "z"])

node_numbers_list = []

for n in tqdm(original_nodes_df.index, desc="Fixing Beam-Column Connections"):
    joint_group = nodes_df[nodes_df["node_num"] % 1000 == original_nodes_df["node_num"][n]].copy()
    if joint_group.empty:
        print(f"joint_group is empty for node_num {original_nodes_df['node_num'][n]}")
        break
    elif len(joint_group) == 1:
        print(f"Joint group for node {original_nodes_df['node_num'][n]} only has one node.")
    else:
        master_col_node = min(joint_group["node_num"])
    
    # Append the node numbers to the list
    node_numbers_list.append(joint_group["node_num"].tolist())

    # Save the node numbers list as a row in a CSV file
    pd.DataFrame(node_numbers_list).to_csv('node_numbers.csv', index=False, header=False)

# Save the final node numbers list as a CSV file
# pd.DataFrame(node_numbers_list).to_csv('node_numbers.csv', index=False, header=False)

