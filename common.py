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
        

        
        


        
        
        

        
        
