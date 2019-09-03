import unittest
from hyperlapse import SemanticHyperlapse
from stabilizer import Stabilizer
from video import Video
from hyperlapseExceptions import InputError
import os

class TestHyperlapse(unittest.TestCase):
    
    def setUp(self):
        video = Video('/home/victorhugomoura/Documents/example.mp4')

        extractor = 'face'
        velocity = 10

        self.hyperlapse = SemanticHyperlapse(video, extractor, velocity)

    def testExtractor(self):
        self.hyperlapse.checkExtractor()
        self.hyperlapse.extractor = ''
        self.assertRaises(InputError, self.hyperlapse.checkExtractor)

    def testVelocity(self):
        self.hyperlapse.checkAndSetVelocity()
        self.hyperlapse.velocity = ''
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)
        self.hyperlapse.velocity = 'A'
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)
        self.hyperlapse.velocity = '1'
        self.assertRaises(InputError, self.hyperlapse.checkAndSetVelocity)

    def testOpticalFlowCommand(self):
        command = self.hyperlapse.opticalFlowCommand()
        expectedCommand = './optflow -v /home/victorhugomoura/Documents/example.mp4 ' + \
            '-c default-config.xml -o /home/victorhugomoura/Documents/example.csv'

        self.assertEqual(command, expectedCommand)

    def testOpticalFlowExists(self):
        self.assertTrue(self.hyperlapse.opticalFlowExists()) # works only if the file already exists

    def testCheckVideoInput(self):
        self.hyperlapse.checkVideoInput()
        self.hyperlapse.video = Video('')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)
        self.hyperlapse.video = Video('/home/victorhugomoura/Documents/example.csv')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)
    
    def testInputError(self):
        self.hyperlapse.checkVideoInput()
        self.hyperlapse.video = Video('')
        
        try:
            self.hyperlapse.checkVideoInput()
        except InputError as IE:
            self.assertEqual(IE.__str__(), 'Please insert input video first')

class TestVideo(unittest.TestCase):
    
    def setUp(self):
        self.video = Video('/home/victorhugomoura/Documents/example.mp4')

    def testFile(self):
        self.assertEqual(self.video.file(),
                        '/home/victorhugomoura/Documents/example.mp4')

    def testName(self):
        self.assertEqual(self.video.name(), 'example.mp4')

    def testPath(self):
        self.assertEqual(self.video.path(),
                        '/home/victorhugomoura/Documents')

    def testEmpty(self):
        self.assertFalse(self.video.isEmpty())
        self.video.videofile = ''
        self.assertTrue(self.video.isEmpty())

    def testInvalid(self):
        self.assertFalse(self.video.isInvalid())
        self.video.videofile = '/home/victorhugomoura/Documents/example.csv'
        self.assertTrue(self.video.isInvalid())

class TestStabilizer(unittest.TestCase):

    def setUp(self):
        originalVideo = Video('/home/victorhugomoura/Documents/example.mp4')
        acceleratedVideo = Video('/home/victorhugomoura/Documents/Folder With Spaces/example.avi')
        velocity = 10
        self.stabilizer = Stabilizer(originalVideo, acceleratedVideo, velocity)

    def testCorrectPath(self):
        original = self.stabilizer.originalVideo.file()
        expected = '"/home/victorhugomoura/Documents/example.mp4"'
        self.assertEqual(self.stabilizer.correctPath(original), expected)

        original = self.stabilizer.acceleratedVideo.file()
        expected = '"/home/victorhugomoura/Documents/Folder&#32;With&#32;Spaces/example.avi"'
        self.assertEqual(self.stabilizer.correctPath(original), expected)

if __name__ == '__main__':
    unittest.main()