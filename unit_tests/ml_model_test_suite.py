# import libraries 
import unittest
import os

from matplotlib import patheffects
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
from PIL import Image
import os
import time
import cv2
import sys

sys.path.insert(1, './Jetcam_Live')
from VideoCapture import VideoCapture
from Predictor import RecyclePredict


class ML_Model_Unit_Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        start = time.time()
        
        # init model and attributes
        print("LOADING MODEL COULD TAKE 5 PLUS MINUTES...FYI")
        self.test = RecyclePredict()
        self.classes = ["Cardbrd", "Glass", "Metal", "Paper", "Plastic", "Trash"]
        self.model_path = "data/resnet18_recycle_train.pth"
        self.img_path = "data/testing_data/test/cardboard/cardboard11.jpg"

        # prep model
        self.test.prep_model(self.classes)

        # Converts cardboard11.jpg to Tensor Format 
        self.test.load_trained_model(self.model_path)
        img = cv2.imread(self.img_path, cv2.IMREAD_ANYCOLOR)
        img = cv2.resize(img, (224, 224))
        img = Image.fromarray(img)
        img = self.test.preprocess_image(img)

        # calculate probabilties and prediction
        self.probabilities = self.test.get_probabilities(img)
        self.prediction = self.test.get_prediction()

        end = time.time()

        print("Set up took", end - start, "seconds to run")

    def test_model_returns_prediction(self):
        '''Asserts that the model returns a prediction that is of type np.int64 (integer)'''
        self.assertIsInstance(self.prediction, np.int64)

    def test_model_returns_probabilties(self):
        '''Asserts that the model returns a probabilities of np.ndarray (array) with 6 np.float32 (floats)'''
        self.assertIsInstance(self.probabilities, np.ndarray)
        self.assertEqual(len(self.probabilities), 6)
        for prob in self.probabilities:
            self.assertIsInstance(prob, np.float32)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
