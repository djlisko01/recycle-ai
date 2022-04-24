# import libraries 
import unittest
import os
from VideoCapture import VideoCapture

# # Check device number
# !ls -ltrh /dev/video*


class Test_Camera_Unit_Test(unittest.TestCase):
    def setUp(self):
        # init camera
        self.camera = VideoCapture() # confirm the capture_device number if this errors out
        # self.camera.get_frame()
        self.camera.capture.read()

    def tearDown(self):
        # turn off camera
        self.camera.capture.release()

    def test_camera_connected_to_usb(self):
        '''Asserts that the a USB camera is connected to Jetson Nano and recognized from the command line terminal'''
        # check for device number in terminal
        cmd_line_camera = os.popen("echo ls -ltrh /dev/video*")
        cmd_line_camera = cmd_line_camera.read()

        # get the str command return
        video_text = cmd_line_camera[-7:-2]
        digit_text = cmd_line_camera[-2]

        # assert the terminal command returns a device connected
        self.assertTrue(digit_text.isdigit())
        self.assertEqual(video_text, "video")
        print("Expected: video{1} ||| Actual: {0}{1}".format(video_text, digit_text))

    def test_camera_initialized(self):
        '''Asserts that the a USB camera is connected and initialized in our Python scripts'''
        # assert that the instance of USBCamera is USBCamera type
        self.assertIsInstance(self.camera, VideoCapture)
        print(self.camera, "is type", type(self.camera))

    def test_save_file(self):
        '''Asserts that the save image method is properly creating the necessary files and directory paths'''
        test_path = "../data/camera_pictures/"
        test_img_name = "test_images"
        self.camera.save_img(test_path, test_img_name)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
