import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from pathlib import Path
from scipy.stats import entropy
from parameters import get_single_265_data, get_second_265_data, get_triple_265_data, get_single_265_pkl, get_second_265_pkl, get_triple_265_pkl, FILE_NAME, QP1, QP2, QP3, CTU, PRESET 
from IPython.display import display, clear_output

plt.rcParams["font.size"]=10
plt.rcParams["figure.figsize"]=(15.0, 4.0)
plt.rcParams["figure.dpi"]= 300

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


SINGLE_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/SINGLE_sameQP_data/')
SECOND_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/SECOND_sameQP_data/')
TRIPLE_DATA_PATH = Path('/Prove/Yoshihisa/HEIF_ghost/KL_PLOT_WIDGETS/TRIPLE_sameQP_data/')

def single_histograms_by_index(root_path, QP1, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_single_265_data(file_name, QP1, CTU, PRESET)

def second_histograms_by_index(root_path, QP1, QP2, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_second_265_data(file_name, QP1, QP2, CTU, PRESET)
        
def triple_histograms_by_index(root_path, QP1, QP2, QP3, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_triple_265_data(file_name, QP1, QP2, QP3, CTU, PRESET)


        
def single_ghost_by_index(root_path, QP1, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_single_265_pkl(file_name, QP1, CTU, PRESET)

def second_ghost_by_index(root_path, QP1, QP2, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_second_265_pkl(file_name, QP1, QP2, CTU, PRESET)
        
def triple_ghost_by_index(root_path, QP1, QP2, QP3, CTU, PRESET):
    for file_name in FILE_NAME:
        yield root_path / get_triple_265_pkl(file_name, QP1, QP2, QP3, CTU, PRESET)
        
        
        
def subgop_bar_plot(DATA_PATH, data_type):
    array = np.load(DATA_PATH)[data_type]

    # 一意の値とその出現回数を取得
    unique_values, counts = np.unique(array, return_counts=True)

    # unique_valuesに0が含まれていない場合、手動で追加
    if 0 not in unique_values:
        unique_values = np.insert(unique_values, 0, 0)
        counts = np.insert(counts, 0, 0)

    # 0から最大値までの値が含まれていることを確認
    max_value = np.max(unique_values)
    full_range = np.arange(max_value + 1)

    # unique_valuesに含まれていない値に対応するcountsに0を追加
    missing_values = np.setdiff1d(full_range, unique_values)
    for missing_value in missing_values:
        unique_values = np.insert(unique_values, np.searchsorted(unique_values, missing_value), missing_value)
        counts = np.insert(counts, np.searchsorted(unique_values, missing_value), 0)

    # ヒストグラムを描画
    print(counts)
    plt.bar(unique_values, counts)

    # グラフのタイトルや軸ラベルの追加（任意）
    # plt.title(f'{data_type.capitalize()} counts Histogram')
    plt.xlabel('index')
    plt.ylabel('Frequency')

    # x軸の目盛りを0, 1, 2, 3に設定
    plt.xticks(unique_values)
    
    plt.ylim(0, 20000)

    # グラフの表示
    plt.savefig(f'{data_type}.pdf', bbox_inches="tight", pad_inches=0.0)
    plt.show()
    
    
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
        self.histograms3[file_path] = (counts, bins)
        
    elif data_type == "chroma":
        self.histograms4[file_path] = (counts, bins)


def calculate_kl_divergence(hist1, hist2):
    p = hist1[0] / np.sum(hist1[0])
    q = hist2[0] / np.sum(hist2[0])
    # print(p, q)
    kl_divergence = entropy(p, q)
    # kl_divergence2 = entropy(q, p)  # 対称性を考慮して追加
    return kl_divergence

def kl_output(histograms, histograms2, types):
    for filename1, hist1 in histograms.items():
        for filename2, hist2 in histograms2.items():
            
            min_len = min(len(hist1[0]), len(hist2[0]))
            # print(hist1[0][:min_len], hist1[1][:min_len])
            # print(hist2[0][:min_len], hist2[1][:min_len])
            kl_divergence = calculate_kl_divergence((hist1[0][:min_len], hist1[1][:min_len]), 
                                                    (hist2[0][:min_len], hist2[1][:min_len]))
            print(f"KL Divergence-{types}: {kl_divergence}")
            
            
def compare_depth_elements(file1, file2):
    # ファイルを読み込む
    data1 = np.load(file1)
    data2 = np.load(file2)

    # "depth" キーが存在するか確認
    if 'depth' not in data1 or 'depth' not in data2:
        print("One or both files do not have the 'depth' key.")
        return

    # "depth" キーの配列を取得
    depth_array1 = data1['depth']
    depth_array2 = data2['depth']

    # 配列の要素ごとに比較し、異なる要素のインデックスを取得
    diff_indices = np.where(depth_array1 != depth_array2)

    
    # 異なる要素がある場合は表示
    if len(diff_indices[0]) > 0:
        print("Differences in 'depth' elements:")
        i=0
        for index in zip(*diff_indices):
            print(f"Index {index}: {depth_array1[index]} vs {depth_array2[index]}")
            i+=1
    else:
        print("No differences in 'depth' elements.")
        
    result = (63232 - i)/63232*100
    rounded_result = round(result, 1)
    print(f'The {rounded_result}% CU-size in the two images were identical')


class Single_PlotVisualization:
    def __init__(self, bitrate_list, gop_list, sg_list):
        self.bitrate_selection = widgets.ToggleButtons(options=bitrate_list, description='QP:')
        self.gop_selection = widgets.ToggleButtons(options=gop_list, description='CTU:')
        self.sg_selection = widgets.ToggleButtons(options=sg_list, description='PRESET:')
        self.video_selection = widgets.Dropdown(options=[], description='IMAGEs:')
        self.plot_button = widgets.Button(description="Plot histogram")
        self.plot_output = widgets.Output()
        
        self.bitrate_selection.observe(self.on_change_encoding_settings)
        self.gop_selection.observe(self.on_change_encoding_settings)
        self.sg_selection.observe(self.on_change_encoding_settings)
        self.plot_button.on_click(self.on_plot_button_clicked)
                        
        display(self.bitrate_selection, self.gop_selection, self.sg_selection, 
                self.video_selection, self.plot_button, self.plot_output)
        
        self.on_change_encoding_settings(None)
        
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        
        
    def on_change_encoding_settings(self, _):
        hist_filenames = list(single_histograms_by_index(SINGLE_DATA_PATH,
                                                         self.bitrate_selection.value,
                                                         self.gop_selection.value,
                                                         self.sg_selection.value))
        self.video_selection.options = hist_filenames
        
            
    def on_plot_button_clicked(self, _):

        clear_output()
        with self.plot_output:
            clear_output()
            
#             pkl_path = str(self.video_selection.value).replace('.npz', '.pkl')
#             with open(pkl_path, mode="rb") as f:
#                 loaded_data = pickle.load(f)
            
#             ghost_results, ghost_results_shifted = loaded_data
#             original_mae = ghost_results
#             shifted_mae = ghost_results_shifted
            
#             mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
#             print("The maximum Ghost:", max(mae_differences))
#             print()
#             print()
            
            self.histograms = {}
            self.histograms2 = {}
            self.histograms3 = {}
            self.histograms4 = {}
            self.filenames = {}
            
            file_path = self.video_selection.value
            
            # ファイルが存在するか確認
            if file_path.exists():
                # ヒストグラムを描画
                subgop_bar_plot(file_path, "depth")
                subgop_bar_plot(file_path, "pu")
                subgop_bar_plot(file_path, "luminance")
                subgop_bar_plot(file_path, "chroma")
                                
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')

                
            else:
                print(f"File not found: {file_path}")
                
                
                
class Double_PlotVisualization:
    def __init__(self, bitrate1_list, bitrate2_list, gop2_list, sg_list):
        
        self.bitrate1_selection = widgets.ToggleButtons(options=bitrate1_list, description='QP1:')
        self.bitrate2_selection = widgets.ToggleButtons(options=bitrate2_list, description='QP2:')
        self.gop_selection = widgets.ToggleButtons(options=gop2_list, description='CTU:')
        self.sg_selection = widgets.ToggleButtons(options=sg_list, description='PRESET:')
        self.video_selection = widgets.Dropdown(options=[], description='IMAGEs:') 
        self.plot_button = widgets.Button(description="Plot histogram")
        self.plot_output = widgets.Output()

        self.bitrate1_selection.observe(self.on_change_encoding_settings)
        self.bitrate2_selection.observe(self.on_change_encoding_settings)
        self.gop_selection.observe(self.on_change_encoding_settings)
        self.sg_selection.observe(self.on_change_encoding_settings)
        self.plot_button.on_click(self.on_plot_button_clicked)
        
        display(self.bitrate1_selection, self.bitrate2_selection,  
                self.gop_selection,  self.sg_selection, self.video_selection, 
                self.plot_button, self.plot_output)
        
        self.on_change_encoding_settings(None)
        
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        
        
    def on_change_encoding_settings(self, _):
        hist_filenames = list(second_histograms_by_index(SECOND_DATA_PATH,
                                                         self.bitrate1_selection.value,
                                                         self.bitrate2_selection.value,
                                                         self.gop_selection.value,
                                                         self.sg_selection.value))
        self.video_selection.options = hist_filenames
        
            
    def on_plot_button_clicked(self, _):

        clear_output()
        with self.plot_output:
            clear_output()
            
#             pkl_path = str(self.video_selection.value).replace('.npz', '.pkl')
#             with open(pkl_path, mode="rb") as f:
#                 loaded_data = pickle.load(f)
                

            
#             ghost_results, ghost_results_shifted = loaded_data
#             original_mae = ghost_results
#             shifted_mae = ghost_results_shifted
            

#             mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
#             print("The maximum Ghost:", max(mae_differences))
#             print()
#             print()
            
            self.histograms = {}
            self.histograms2 = {}
            self.histograms3 = {}
            self.histograms4 = {}
            self.filenames = {}
            
            file_path = self.video_selection.value
            
            # ファイルが存在するか確認
            if file_path.exists():
                # ヒストグラムを描画
                subgop_bar_plot(file_path, "depth")
                subgop_bar_plot(file_path, "pu")
                subgop_bar_plot(file_path, "luminance")
                subgop_bar_plot(file_path, "chroma")
                                
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')
                           
            else:
                print(f"File not found: {file_path}")
                


                
class Triple_PlotVisualization:
    def __init__(self, bitrate1_list, bitrate2_list, bitrate3_list, gop3_list, sg_list):
        
        self.bitrate1_selection = widgets.ToggleButtons(options=bitrate1_list, description='QP1:')
        self.bitrate2_selection = widgets.ToggleButtons(options=bitrate2_list, description='QP2:')
        self.bitrate3_selection = widgets.ToggleButtons(options=bitrate3_list, description='QP3:')
        self.gop_selection = widgets.ToggleButtons(options=gop3_list, description='CTU:')
        self.sg_selection = widgets.ToggleButtons(options=sg_list, description='PRESET:')
        self.video_selection = widgets.Dropdown(options=[], description='IMAGEs:') 
        self.plot_button = widgets.Button(description="Plot histogram")
        self.plot_output = widgets.Output()

        self.bitrate1_selection.observe(self.on_change_encoding_settings)
        self.bitrate2_selection.observe(self.on_change_encoding_settings)
        self.bitrate3_selection.observe(self.on_change_encoding_settings)
        self.gop_selection.observe(self.on_change_encoding_settings)
        self.sg_selection.observe(self.on_change_encoding_settings)
        self.plot_button.on_click(self.on_plot_button_clicked)
        
        display(self.bitrate1_selection, self.bitrate2_selection, self.bitrate3_selection,  
                self.gop_selection,  self.sg_selection, self.video_selection, 
                self.plot_button, self.plot_output)
        
        self.on_change_encoding_settings(None)
        
        self.histograms = {}
        self.histograms2 = {}
        self.histograms3 = {}
        self.histograms4 = {}
        self.filenames = {}
        
        
    def on_change_encoding_settings(self, _):
        hist_filenames = list(triple_histograms_by_index(TRIPLE_DATA_PATH,
                                                         self.bitrate1_selection.value,
                                                         self.bitrate2_selection.value,
                                                         self.bitrate3_selection.value,
                                                         self.gop_selection.value,
                                                         self.sg_selection.value))
        self.video_selection.options = hist_filenames
        
            
    def on_plot_button_clicked(self, _):

        clear_output()
        with self.plot_output:
            clear_output()
            
#             pkl_path = str(self.video_selection.value).replace('.npz', '.pkl')
#             with open(pkl_path, mode="rb") as f:
#                 loaded_data = pickle.load(f)
                
            
            
#             ghost_results, ghost_results_shifted = loaded_data
#             original_mae = ghost_results
#             shifted_mae = ghost_results_shifted
            

#             mae_differences = [shifted - original for original, shifted in zip(original_mae, shifted_mae)]
#             print("The maximum Ghost:", max(mae_differences))
#             print()
#             print()
            
            self.histograms = {}
            self.histograms2 = {}
            self.histograms3 = {}
            self.histograms4 = {}
            self.filenames = {}
            
            file_path = self.video_selection.value
            
            # ファイルが存在するか確認
            if file_path.exists():
                # ヒストグラムを描画
                subgop_bar_plot(file_path, "depth")
                subgop_bar_plot(file_path, "pu")
                subgop_bar_plot(file_path, "luminance")
                subgop_bar_plot(file_path, "chroma")
                                
                generate_histogram(self, file_path, 'depth')
                generate_histogram(self, file_path, 'pu')
                generate_histogram(self, file_path, 'luminance')
                generate_histogram(self, file_path, 'chroma')
                           
            else:
                print(f"File not found: {file_path}")
                
                




        
    
            
