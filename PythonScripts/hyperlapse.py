import matlab.engine
import os
from subprocess import Popen, PIPE, STDOUT
from hyperlapseExceptions import InputError
from video import Video
from stabilizer import Stabilizer

class SemanticHyperlapse(object):
    def __init__(self, video, extractor, velocity):
        self.video = video
        self.path = os.getcwd()
        self.extractor = extractor
        self.velocity = velocity
        self.maxVel = 10 * velocity

        self.checkParameters()

    def checkExtractor(self):
        if self.isEmpty(self.extractor):
            raise InputError('Please select an extractor')

    def checkAndSetVelocity(self):
        if self.isEmpty(self.velocity):
            raise InputError('Please insert speedup')
        try:
            self.isVelocityValidNumber()
            self.velocity = float(int(self.velocity))
        except ValueError:
            raise InputError('Invalid speedup value')
    
    def checkVideoInput(self):
        self.video.checkInput('Input')

    def isVelocityValidNumber(self):
        velocity = int(self.velocity) #raises ValueError if it isn't a number
        if velocity <= 1:
            raise InputError('Error: speedup <= 1')

    def isEmpty(self, inputText):
        if inputText == '':
            return True
        return False

    def opticalFlowExists(self):
        videoFile = self.video.file()
        outputFile = videoFile[:-4] + '.csv'

        return os.path.isfile(outputFile)

    def opticalFlowCommand(self):
        videoFile = self.correctPath(self.video.file())
        command = './optflow'
        videoParam = ' -v ' + videoFile
        configParam = ' -c default-config.xml'
        outputParam = ' -o ' + videoFile[:-4] + '.csv'

        fullCommand = command + videoParam + configParam + outputParam
        
        return fullCommand

    def runOpticalFlow(self): # pragma: no cover
        os.chdir('Vid2OpticalFlowCSV')

        if not self.opticalFlowExists():
            os.system(self.opticalFlowCommand())
        else:
            print 'OpticalFlow already extracted.'
        
        os.chdir(self.path)

    def getSemanticInfo(self, eng): # pragma: no cover
        eng.cd('SemanticScripts')
        eng.addpath(self.video.path())
        eng.addpath(os.getcwd())

        videoFile = self.video.file()
        extractor = self.extractor
        
        eng.ExtractAndSave(videoFile, extractor, nargout=0)
        eng.cd(self.path)

    def speedUp(self, eng): # pragma: no cover
        eng.addpath(os.getcwd())
        eng.addpath('Util')
        
        videoName = eng.SpeedupVideo(
            self.video.path(), self.video.name(), self.extractor,
            'Speedup', self.velocity, nargout=1
        )
        return videoName

    def checkParameters(self):	
        self.checkVideoInput()
        self.checkExtractor()
        self.checkAndSetVelocity()

    def speedUpPart(self, writeFunction): # pragma: no cover
        write = writeFunction
        
        write('1/6 - Running Optical Flow\n', 'title')
        self.runOpticalFlow()
    
        write('2/6 - Starting Matlab\n', 'title')
        eng = matlab.engine.start_matlab('-nodisplay')
    
        write('3/6 - Getting Semantic Info\n', 'title')
        self.getSemanticInfo(eng)

        write('4/6 - Speeding-Up Video\n', 'title')
        videoName = self.speedUp(eng)
        eng.quit()
    
        return Video(videoName + '.avi')

    def stabilizePart(self, acceleratedVideo, writeFunction): # pragma: no cover
        stabilizer = Stabilizer(self.video, acceleratedVideo, self.velocity)
        stabilizer.run(writeFunction)
        os.chdir(self.path)

    def run(self, writeFunction): # pragma: no cover
        acceleratedVideo = self.speedUpPart(writeFunction)
        self.stabilizePart(acceleratedVideo, writeFunction)

    def correctPath(self, path):
        splittedPath = path.split(' ')
        finalPath = ''
        for i in splittedPath:
            finalPath += (i + '\ ')
        return finalPath[:-2]