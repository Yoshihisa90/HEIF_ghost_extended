import subprocess
from PIL import Image
from pillow_heif import register_heif_opener
import numpy as np
import cv2
import pillow_heif
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

register_heif_opener()


class HEIC2HEVCRunner:
    def __init__(self, heic2hevc_path):
        self.heic2hevc_path = heic2hevc_path

    def run(self, input_path, output_path):
        command = [
            self.heic2hevc_path.absolute(),
            input_path,
            output_path,
        ]

        subprocess.run(command)
        
# class EXTRACT_Frequency:
#     def __init__(self, heic2hevc_path):
#         self.heic2hevc_path = heic2hevc_path

#     def run(self, input_path, output_csv_path):
#         register_heif_opener()
#         im = Image.open(input_path)
#         image = np.array(im)
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         # 2次元フーリエ変換を実行
#         f_transform = np.fft.fft2(gray_image)
#         f_transform_shifted = np.fft.fftshift(f_transform)

#         # パワースペクトルを計算
#         power_spectrum = np.abs(f_transform_shifted)**2

#         # パワースペクトルを対数スケールに変換
#         log_power_spectrum = np.log(power_spectrum + 1)

#         # 低周波成分を抽出する
#         center_x, center_y = gray_image.shape[1] // 2, gray_image.shape[0] // 2
#         size = 100  # 中心部分のサイズを調整
#         center_power_spectrum = log_power_spectrum[center_y - size:center_y + size, center_x - size:center_x + size]

#         # 高周波成分を抽出する（ラプラシアンフィルタを使用）
#         laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)

#         # 絶対値を取得して、正の値のみを保持
#         high_frequency = np.abs(laplacian)
        
#         with open(output_csv_path, 'w', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             writer.writerow(['LOW', 'HIGH'])
#             writer.writerow([center_power_spectrum.std(), high_frequency.std()])


class TAppDecRunner:
    def __init__(self, tappdec_path):
        self.tappdec_path = tappdec_path

    def run(self, input_path, output_path):
        command = [
            self.tappdec_path.absolute(),
            "-b", input_path,
            "-o", output_path,
        ]

        subprocess.run(command)
        

        
        


        
        
        

        
        
