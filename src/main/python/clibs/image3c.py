# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QTemporaryDir
from PyQt5.QtGui import QImage
from PIL import Image
from clibs.color import Color
import numpy as np
import os


class Image3C(QThread):
    """
    Image transformations.
    """

    process = pyqtSignal(int)
    describe = pyqtSignal(str)
    ref_rgb = pyqtSignal(np.ndarray)
    finished = pyqtSignal(bool)

    def __init__(self):
        """
        Init image3c with default temp dir.
        """

        super().__init__()
        
        self._temp_dir = QTemporaryDir()
    
    def check_temp_dir(self):
        return self._temp_dir.isValid()
    
    def remove_temp_dir(self):
        self._temp_dir.remove()

    def import_image(self, image_file):
        """
        Import a image from file and detect the H, S, V value edges of imported image.
        Total steps: 4 + hsv_data.shape[0] + 1 + results_shape[0] + 1 + results_shape[0] + 1 + 1.

        Parameters:
          image_file - string. image file path.

        Returns:
          np.ndarray. referenced rgb color.
        """

        self._image_file = image_file
    
    def run(self):
        # import rgb data.
        self.describe.emit("Reading RGB data.")
        rgb_data = np.array(Image.open(self._image_file).convert("RGB"), dtype=np.uint8)
        self.ref_rgb.emit(rgb_data)
        self.process.emit(1)

        self.save_temp_data(rgb_data, "0")
        self.process.emit(2)

        # transform from rgb to hsv.
        self.describe.emit("Transforming RGB to HSV data.")
        hsv_data = np.zeros(rgb_data.shape, dtype=np.uint16) # = hsv * 65535 (/ 360)
        self.process.emit(3)

        for i in range(hsv_data.shape[0]):
            for j in range(hsv_data.shape[1]):
                hsv = Color.rgb_to_hsv(rgb_data[i][j])
                hsv = hsv / np.array((360.0, 1.0, 1.0)) * 65535
                hsv_data[i][j] = hsv.astype(np.uint16)
            self.process.emit(4 + i)
        
        next_process = 4 + hsv_data.shape[0]

        # Sobel edge detection.
        self.describe.emit("Detecting image edges.")
        results_shape = (hsv_data.shape[0] - 2, hsv_data.shape[1] - 2, 3)
        self.process.emit(next_process)

        next_process += 1

        # vertical.
        self.describe.emit("Generating vertical edges.")
        vtl_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i][j + 2][0] + hsv_data[i + 1][j + 2][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i + 1][j][0] * 2 - hsv_data[i + 2][j][0]
                s_result = hsv_data[i][j + 2][1] + hsv_data[i + 1][j + 2][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i + 1][j][1] * 2 - hsv_data[i + 2][j][1]
                v_result = hsv_data[i][j + 2][2] + hsv_data[i + 1][j + 2][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i + 1][j][2] * 2 - hsv_data[i + 2][j][2]
                vtl_results[i][j] = np.array((abs(h_result) / 1028, abs(s_result) / 1028, abs(v_result) / 1028), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_temp_data(vtl_results, "1")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1

        # horizontal.
        self.describe.emit("Generating horizontal edges.")
        hrz_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i + 2][j][0] + hsv_data[i + 2][j + 1][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i][j + 1][0] * 2 - hsv_data[i][j + 2][0]
                s_result = hsv_data[i + 2][j][1] + hsv_data[i + 2][j + 1][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i][j + 1][1] * 2 - hsv_data[i][j + 2][1]
                v_result = hsv_data[i + 2][j][2] + hsv_data[i + 2][j + 1][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i][j + 1][2] * 2 - hsv_data[i][j + 2][2]
                hrz_results[i][j] = np.array((abs(h_result) / 1028, abs(s_result) / 1028, abs(v_result) / 1028), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_temp_data(hrz_results, "2")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1

        # final.
        self.describe.emit("Integrating final edges.")
        fnl_results = vtl_results + hrz_results
        self.process.emit(next_process)
        self.save_temp_data(fnl_results, "3")
        self.process.emit(next_process + 1)
        
        self.describe.emit("Finishing.")
        self.finished.emit(True)

    def read_channels(self, rgb_data):
        """
        Read R, G, B part channels of rgb data.
        """

        r_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        g_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        b_channel = np.zeros(rgb_data.shape, dtype=np.uint8)

        for i in range(rgb_data.shape[0]):
            for j in range(rgb_data.shape[1]):
                r_channel[i][j][0] = rgb_data[i][j][0]
                g_channel[i][j][1] = rgb_data[i][j][1]
                b_channel[i][j][2] = rgb_data[i][j][2]
        
        return r_channel, g_channel, b_channel
    
    def save_temp_data(self, rgb_data, prefix):
        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._temp_dir.path() + os.sep + "{}_0.png".format(prefix))

        r_chl, g_chl, b_chl = self.read_channels(rgb_data)

        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))

        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))

        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))

    def load_image(self, graph_type, channel):
        """
        Load splited images.
        
        Parameters:
          graph type - int. 0: normal rgb data; 1: vertical edge data; 2: horizontal edge data; 3: final edge data.
          channel - int. 0: rgb full data. 1: r channel data; 2: g channel data; 3: b channel data.
        """

        img_name = "{}_{}.png".format(graph_type, channel)
        img = QImage(self._temp_dir.path() + os.sep + img_name)

        return img
