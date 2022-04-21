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
        # assert that the instance of USBCamera is USBCamera type
        self.assertIsInstance(self.camera, VideoCapture)
        print(self.camera, "is type", type(self.camera))

    # def test_save_file(self):
    #     # init a ImageClassificationDataset
    #     test = ImageClassificationDataset("../data/camera_pictures/unittest", ["unittest"])
    #     # save a picture in /unittest/unittest/unittest_0.jpg
    #     test.save_entry(self.camera.value, "unittest", "unittest_0")

    #     # get the file path directory and add the stored location
    #     file_path = os.getcwd()[:-10]
    #     file_path += "data/camera_pictures/unittest/unittest/unittest_0.jpg"

    #     # assert a file is in the given file path
    #     self.assertTrue(os.path.isfile(file_path))

    #     # delete the test directory
    #     index = file_path.find("unittest")
    #     remove_dir = file_path[:index] + "unittest"
    #     shutil.rmtree(remove_dir)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
