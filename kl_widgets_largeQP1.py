import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from pathlib import Path
from scipy.stats import entropy
from parameters import get_single_265_data, get_second_265_data, get_triple_265_data, get_single_265_pkl, get_second_265_pkl, get_triple_265_pkl, QP1, QP2, QP3, CTU, PRESET 
from IPython.display import display, clear_output
import os
from scipy.stats import entropy

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

            
SINGLE_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/SINGLE_sameQP_data/')
SECOND_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/SECOND_QP_data/')
TRIPLE_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/TRIPLE_QP_data/')


FILE_NAME = [
   '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
   '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
   '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
   '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
   '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
   '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
   '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
   '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
   '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
   '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
   '111', '112', '113', '114', '115', '116', '117', '118', '119', '120',
   '121', '122', '123', '124', '125', '126', '127', '128', '129', '130',
   '131', '132', '133', '134', '135', '136', '137', '138', '139', '140',
   '141', '142', '143', '144', '145', '146', '147', '148', '149', '150'
]

def single_histograms_by_index(root_path, QP1, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_single_265_data(file_name, QP1, CTU, PRESET)

def second_histograms_by_index(root_path, QP1, QP2, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_second_265_data(file_name, QP1, QP2, CTU, PRESET)
        
def triple_histograms_by_index(root_path, QP1, QP2, QP3, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_triple_265_data(file_name, QP1, QP2, QP3, CTU, PRESET)
        

        
def generate_histogram(self, file_path, data_type):
    array = np.load(file_path)[data_type]
    unique_values, counts = np.unique(array, return_counts=True)
    bins = np.arange(len(unique_values) + 1)
    if data_type == "depth":
        self.histograms[file_path] = (counts, bins)
        self.filenames[file_path] = file_path
        
    elif data_type == "pu":
        self.histograms2[file_path] = (counts, bins)
        
    elif data_type == "luminance":        
        indices = np.where(np.isin(unique_values, [0, 1, 9, 10, 11, 25, 26, 27]))[0]
        desired_values = unique_values[indices]
        corresponding_counts = counts[indices]
        self.histograms3[file_path] = (corresponding_counts, desired_values)
        
    elif data_type == "chroma":
        self.histograms4[file_path] = (counts, bins)
        

def laplace_smoothing(counts, alpha=1):
    """
    Apply Laplace smoothing to the given counts.
    
    Args:
    counts (list): The list of counts to smooth.
    alpha (float): The smoothing parameter.
    
    Returns:
    smoothed_probabilities (list): The smoothed probabilities.
    """
    total_count = sum(counts)
    num_elements = len(counts)
    smoothed_probabilities = [(count + alpha) / (total_count + alpha * num_elements) for count in counts]
    return smoothed_probabilities
        

def calculate_kl_divergence(hist1, hist2, alpha=1):
    p_counts = hist1[0]
    q_counts = hist2[0]
    
    # Apply Laplace smoothing
    p_smoothed = laplace_smoothing(p_counts, alpha)
    q_smoothed = laplace_smoothing(q_counts, alpha)
    
    # Calculate KL divergence
    kl_divergence = entropy(p_smoothed, q_smoothed)
    return kl_divergence


# def kl_output(histograms, histograms2, types, alpha=1):
#     kl_divergences = []
    
#     for filename1, hist1 in histograms.items():
#         for filename2, hist2 in histograms2.items():
#             f1 = os.path.basename(filename1)
#             f2 = os.path.basename(filename2)

#             # Extract the relevant part (1_...)
#             part1 = f1.split('_')[0]
#             part2 = f2.split('_')[0]
            
#             if part1 == part2:
#                 min_len = min(len(hist1[0]), len(hist2[0]))
#                 kl_divergence = calculate_kl_divergence((hist1[0][:min_len], hist1[1][:min_len]), 
#                                                         (hist2[0][:min_len], hist2[1][:min_len]), 
#                                                         alpha=alpha)
#                 kl_divergences.append(kl_divergence)
#                 print(kl_divergences)

#     if kl_divergences:
#         average_kl_divergence = np.mean(kl_divergences)
#         kl_divergences_sorted = sorted(kl_divergences)

#         min_val = np.min(kl_divergences_sorted)
#         max_val = np.max(kl_divergences_sorted)
#         median_val = np.median(kl_divergences_sorted)
#         q1 = np.percentile(kl_divergences_sorted, 25)
#         q3 = np.percentile(kl_divergences_sorted, 75)

#         a = [min_val, q1, median_val, q3, max_val]
#     return a

def kl_output(histograms, histograms2, types, alpha=1):
    kl_divergences = []
    
    for filename1, hist1 in histograms.items():
        for filename2, hist2 in histograms2.items():
            f1 = os.path.basename(filename1)
            f2 = os.path.basename(filename2)

            # ファイル名の関連部分を抽出 (1_...)
            part1 = f1.split('_')[0]
            part2 = f2.split('_')[0]
            
            if part1 == part2:
                min_len = min(len(hist1[0]), len(hist2[0]))
                kl_divergence = calculate_kl_divergence((hist1[0][:min_len], hist1[1][:min_len]), 
                                                        (hist2[0][:min_len], hist2[1][:min_len]), 
                                                        alpha=alpha)
                kl_divergences.append(kl_divergence)
                # print(kl_divergences)
    
    return kl_divergences



class Single_PlotVisualization:
    def __init__(self):
        
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        self.max_ghost_values = []
        
    def extract_histograms(self, QP1, CTU, PRESET):
        hist_filenames = []
        hist_filenames.extend(list(single_histograms_by_index(SINGLE_DATA_PATH, QP1, CTU, PRESET)))
            
        for file_path in hist_filenames:
            if file_path.exists():
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')

            else:
                print(f"File not found: {file_path}")
                
            pkl_path = str(file_path).replace('.npz', '.pkl')
            with open(pkl_path, mode="rb") as f:
                loaded_data = pickle.load(f)
            
            ghost_results, ghost_results_shifted = loaded_data
            original_mae = ghost_results
            shifted_mae = ghost_results_shifted
            mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
            max_ghost_value = max(mae_differences)
            self.max_ghost_values.append(max_ghost_value)
        
        if self.max_ghost_values:
            average_max_ghost = sum(self.max_ghost_values) / len(self.max_ghost_values)
            # print("Average of The maximum Ghost values:", average_max_ghost)
            
        
class Double_PlotVisualization:
    def __init__(self):
                
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        self.max_ghost_values = []
        
    def extract_histograms(self, QP1, QP2, CTU, PRESET):
        hist_filenames = []
        hist_filenames.extend(list(second_histograms_by_index(SECOND_DATA_PATH, QP1, QP2, CTU, PRESET)))
            
        for file_path in hist_filenames:
            if file_path.exists():                
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')

            else:
                print(f"File not found: {file_path}")
                
            pkl_path = str(file_path).replace('.npz', '.pkl')
            with open(pkl_path, mode="rb") as f:
                loaded_data = pickle.load(f)
            
            ghost_results, ghost_results_shifted = loaded_data
            original_mae = ghost_results
            shifted_mae = ghost_results_shifted
            mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
            max_ghost_value = max(mae_differences)
            self.max_ghost_values.append(max_ghost_value)
        
        if self.max_ghost_values:
            average_max_ghost = sum(self.max_ghost_values) / len(self.max_ghost_values)
            # print("Average of The maximum Ghost values:", average_max_ghost)
        
                
class Triple_PlotVisualization:
    def __init__(self):
        
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        self.max_ghost_values = []
        
    def extract_histograms(self, QP1, QP2, QP3, CTU, PRESET):
        hist_filenames = []
        hist_filenames.extend(list(triple_histograms_by_index(TRIPLE_DATA_PATH, QP1, QP2, QP3, CTU, PRESET)))
            
        for file_path in hist_filenames:
            if file_path.exists():                
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')

            else:
                print(f"File not found: {file_path}")
                
            pkl_path = str(file_path).replace('.npz', '.pkl')
            with open(pkl_path, mode="rb") as f:
                loaded_data = pickle.load(f)
            
            ghost_results, ghost_results_shifted = loaded_data
            original_mae = ghost_results
            shifted_mae = ghost_results_shifted
            mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
            max_ghost_value = max(mae_differences)
            self.max_ghost_values.append(max_ghost_value)
        
        if self.max_ghost_values:
            average_max_ghost = sum(self.max_ghost_values) / len(self.max_ghost_values)
            # print("Average of The maximum Ghost values:", average_max_ghost)