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
        
        alpha = ['1', '2']
        beta = ['4', '3']
        gama = ['5', '6']
        eta = ['8', '7']

        self.hyperlapse = SemanticHyperlapse(video, extractor, velocity,
                                             alpha, beta, gama, eta)

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

    def testCheckWeights(self):
        self.hyperlapse.checkAndSetWeights()
        self.hyperlapse.alpha = ['', '']
        self.assertRaises(InputError, self.hyperlapse.checkAndSetWeights)
        self.hyperlapse.alpha = ['1', '1']
        self.hyperlapse.beta = ['a', '10']
        self.assertRaises(InputError, self.hyperlapse.checkAndSetWeights)

    def testOpticalFlowCommand(self):
        command = self.hyperlapse.opticalFlowCommand()
        expectedCommand = './optflow -v /home/victorhugomoura/Documents/example.mp4 ' + \
            '-c default-config.xml -o /home/victorhugomoura/Documents/example.csv'

        self.assertEqual(command, expectedCommand)

    def testOpticalFlowExists(self):
        self.assertTrue(self.hyperlapse.opticalFlowExists()) # works only on Verlab machines

    def testCheckVideoInput(self):
        self.hyperlapse.checkVideoInput()
        self.hyperlapse.video = Video('')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)
        self.hyperlapse.video = Video('/home/victorhugomoura/Documents/example.csv')
        self.assertRaises(InputError, self.hyperlapse.checkVideoInput)

    def testCheckParameters(self):
        self.hyperlapse.checkParameters()
    
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
        acceleratedVideo = Video('/home/victorhugomoura/Documents/out/example.mp4')
        self.stabilizer = Stabilizer(originalVideo, acceleratedVideo, '10')

    def testCheckParameters(self):
        self.stabilizer.checkParameters()

        self.stabilizer.originalVideo = Video('/home/victorhugomoura/Documents/example.csv')
        self.assertRaises(InputError, self.stabilizer.checkParameters)

        self.setUp()
        self.stabilizer.acceleratedVideo = Video('/home/victorhugomoura/Documents/out/example.csv')
        self.assertRaises(InputError, self.stabilizer.checkParameters)

        self.setUp()
        self.stabilizer.velocity = '1'
        self.assertRaises(InputError, self.stabilizer.checkParameters)

if __name__ == '__main__':
    unittest.main()